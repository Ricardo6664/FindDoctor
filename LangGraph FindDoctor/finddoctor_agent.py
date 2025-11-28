from typing import List, Dict, Any, Optional, TypedDict
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
import json
import os

from finddoctor_api_client import FindDoctorApiClient

# Inicializa o cliente da API
client = FindDoctorApiClient("http://localhost:5210", "http://localhost:8000")

# Define o estado do agente usando MessagesState padrão
# MessagesState já inclui a lista de mensagens com add_messages

# Define as ferramentas
@tool
def search_address(query: str) -> str:
    """Busca por um endereço e retorna informações de geolocalização."""
    print(f"🔍 EXECUTANDO: search_address com query='{query}'")
    try:
        results = client.search_address(query)
        if not results:
            print("   ❌ Nenhum endereço encontrado")
            return "Nenhum endereço encontrado para esta consulta."
        print(f"   ✅ {len(results)} endereço(s) encontrado(s)")
        return json.dumps(results[:3], ensure_ascii=False)
    except Exception as e:
        return f"Erro ao buscar endereço: {str(e)}"

@tool
def get_specialties() -> str:
    """Obtém a lista de todas as especialidades médicas disponíveis do arquivo local filtrado."""
    print(f"🏥 EXECUTANDO: get_specialties (arquivo médico filtrado)")
    try:
        # Caminho para o arquivo JSON de especialidades médicas filtrado
        json_file_path = os.path.join(os.path.dirname(__file__), "medical_specialties.json")
        
        # Verifica se o arquivo existe
        if not os.path.exists(json_file_path):
            print(f"   ❌ Arquivo {json_file_path} não encontrado")
            return "Erro: Arquivo de especialidades médicas não encontrado."
        
        # Lê o arquivo JSON local filtrado
        with open(json_file_path, 'r', encoding='utf-8') as file:
            specialties = json.load(file)
        
        print(f"   ✅ {len(specialties)} especialidade(s) médica(s) carregada(s) do arquivo filtrado")
        return json.dumps(specialties, ensure_ascii=False)
        
    except Exception as e:
        print(f"   ❌ Erro ao ler arquivo de especialidades médicas: {str(e)}")
        return f"Erro ao buscar especialidades médicas: {str(e)}"

@tool
def search_establishments(
    latitude: float,
    longitude: float,
    radius_km: float = 2.0,
    specialty_name: Optional[str] = None,
    doctor_name: Optional[str] = None
) -> str:
    """
    Busca estabelecimentos de saúde próximos às coordenadas especificadas.
    
    Argumentos:
        latitude: Coordenada de latitude
        longitude: Coordenada de longitude
        radius_km: Raio de busca em quilômetros
        specialty_name: Nome da especialidade médica (ex: "cardiologista", "pediatra")
        doctor_name: Nome opcional do médico para filtrar resultados    """
    print(f"🏢 EXECUTANDO: search_establishments")
    print(f"   📍 Localização: ({latitude}, {longitude})")
    print(f"   📏 Raio: {radius_km}km")
    if specialty_name:
        print(f"   🩺 Especialidade solicitada: {specialty_name}")
    if doctor_name:
        print(f"   👨‍⚕️ Nome do médico: {doctor_name}")
    
    specialty_id = None
    # Se uma especialidade foi especificada, busca o ID correspondente
    if specialty_name:
        print(f"   🔍 Buscando ID da especialidade para: {specialty_name}")
        try:
            # Carrega especialidades médicas do arquivo filtrado
            json_file_path = os.path.join(os.path.dirname(__file__), "medical_specialties.json")
            
            if os.path.exists(json_file_path):
                print("   📁 Carregando especialidades médicas do arquivo filtrado...")
                with open(json_file_path, 'r', encoding='utf-8') as file:
                    specialties = json.load(file)
                print(f"   ✅ {len(specialties)} especialidades médicas carregadas do arquivo filtrado")
            else:
                print("   ❌ Arquivo de especialidades médicas não encontrado")
                return "Erro: Arquivo de especialidades médicas não encontrado."
            
            specialty_name_lower = specialty_name.lower().strip()
            
            # Busca direta por correspondência (já que o arquivo só tem especialidades médicas)
            print(f"   🔍 Procurando por: {specialty_name_lower}")
            
            matched_specialty = None
            best_match_score = 0
            
            for specialty in specialties:
                specialty_nome_upper = specialty['nome'].upper().strip()
                specialty_nome_lower = specialty['nome'].lower().strip()
                
                # Score de correspondência
                score = 0
                
                # Correspondência exata (ignora case)
                if specialty_name_lower == specialty_nome_lower:
                    score = 100
                # Contém o termo completo
                elif specialty_name_lower in specialty_nome_lower:
                    score = 90
                elif specialty_nome_lower in specialty_name_lower:
                    score = 85
                # Busca por palavras-chave parciais
                elif any(word in specialty_nome_lower for word in specialty_name_lower.split() if len(word) > 3):
                    score = 75
                # Busca por início do nome
                elif specialty_nome_lower.startswith(specialty_name_lower[:6]):
                    score = 70
                
                # Atualiza melhor correspondência
                if score > best_match_score:
                    best_match_score = score
                    matched_specialty = specialty
            
            if matched_specialty and best_match_score >= 70:
                specialty_id = matched_specialty['id']
                print(f"   ✅ Especialidade encontrada: {matched_specialty['nome']} (ID: {specialty_id}) - Score: {best_match_score}")
            else:
                print(f"   ⚠️ Especialidade '{specialty_name}' não encontrada com confiança suficiente, buscando sem filtro de especialidade")
                
        except Exception as e:
            print(f"   ❌ Erro ao buscar especialidades: {str(e)}")
            print("   ⚠️ Continuando busca sem filtro de especialidade")
    
    try:
        results = client.search_establishments(
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            specialty_id=specialty_id,
            doctor_name=doctor_name
        )
        if not results:
            print("   ❌ Nenhum estabelecimento encontrado")
            return "Nenhum estabelecimento encontrado que atenda aos seus critérios."
        print(f"   ✅ {len(results)} estabelecimento(s) encontrado(s)")
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        return f"Erro ao buscar estabelecimentos: {str(e)}"

@tool
def get_establishment_details(cnes_code: str) -> str:
    """Obtém informações detalhadas sobre um estabelecimento de saúde específico."""
    print(f"🏥 EXECUTANDO: get_establishment_details com CNES='{cnes_code}'")
    try:
        details = client.get_establishment_details(cnes_code)
        print(f"   ✅ Detalhes obtidos para estabelecimento {cnes_code}")
        return json.dumps(details, ensure_ascii=False)
    except Exception as e:
        return f"Erro ao buscar detalhes do estabelecimento: {str(e)}"

# ========== FERRAMENTAS DE AGENDAMENTO ==========

@tool
def list_available_doctors(establishment_id: Optional[str] = None, specialty: Optional[str] = None) -> str:
    """
    Lista médicos cadastrados no sistema de agendamento que estão disponíveis para marcar consultas.
    
    IMPORTANTE: Use esta ferramenta quando o usuário:
    - Perguntar "quais médicos disponíveis para agendamento"
    - Quiser "agendar uma consulta"
    - Perguntar "com quais médicos posso agendar"
    - Mencionar "marcar consulta" ou "agendar"
    
    NÃO use esta ferramenta para buscas por localização geográfica.
    Para buscar médicos próximos a um endereço, use search_establishments.
    
    Argumentos:
        establishment_id: ID do estabelecimento (opcional)
        specialty: Especialidade médica para filtrar (opcional, ex: "cardiologia", "pediatria")
    """
    print(f"👨‍⚕️ EXECUTANDO: list_available_doctors")
    if establishment_id:
        print(f"   🏥 Estabelecimento: {establishment_id}")
    if specialty:
        print(f"   🩺 Especialidade: {specialty}")
    
    try:
        doctors = client.list_doctors(establishment_id)
        
        # Filtra por especialidade se fornecida
        if specialty:
            specialty_lower = specialty.lower().strip()
            doctors = [
                d for d in doctors 
                if d.get('specialty', '').lower().find(specialty_lower) != -1
            ]
        
        # Filtra apenas médicos ativos
        doctors = [d for d in doctors if d.get('is_active', True)]
        
        if not doctors:
            print("   ❌ Nenhum médico disponível encontrado")
            return "Nenhum médico disponível para agendamento no momento."
        
        print(f"   ✅ {len(doctors)} médico(s) disponível(is)")
        
        # Formata resposta com informações essenciais
        doctors_info = []
        for doc in doctors:
            info = {
                "id": doc.get("id"),
                "nome": doc.get("name"),
                "especialidade": doc.get("specialty"),
                "crm": doc.get("crm"),
                "estabelecimento": doc.get("establishment_name")
            }
            doctors_info.append(info)
        
        return json.dumps(doctors_info, ensure_ascii=False)
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return f"Erro ao buscar médicos disponíveis: {str(e)}"

@tool
def schedule_appointment(
    doctor_id: int,
    patient_name: str,
    patient_email: str,
    patient_phone: str,
    appointment_date: str,
    appointment_time: str,
    notes: Optional[str] = None
) -> str:
    """
    Agenda uma consulta médica.
    
    Argumentos:
        doctor_id: ID do médico (obtido da lista de médicos)
        patient_name: Nome completo do paciente
        patient_email: Email do paciente
        patient_phone: Telefone do paciente com DDD
        appointment_date: Data da consulta no formato YYYY-MM-DD (ex: 2025-12-15)
        appointment_time: Horário da consulta no formato HH:MM (ex: 14:30)
        notes: Observações adicionais (opcional)
    """
    print(f"📅 EXECUTANDO: schedule_appointment")
    print(f"   👨‍⚕️ Médico ID: {doctor_id}")
    print(f"   👤 Paciente: {patient_name}")
    print(f"   📧 Email: {patient_email}")
    print(f"   📱 Telefone: {patient_phone}")
    print(f"   📆 Data: {appointment_date}")
    print(f"   ⏰ Horário: {appointment_time}")
    if notes:
        print(f"   📝 Observações: {notes}")
    
    try:
        # Validações básicas
        if not all([doctor_id, patient_name, patient_email, patient_phone, appointment_date, appointment_time]):
            return "Erro: Todos os campos obrigatórios devem ser preenchidos (médico, nome, email, telefone, data e horário)."
        
        # Cria o agendamento
        appointment = client.create_appointment(
            doctor_id=doctor_id,
            patient_name=patient_name,
            patient_email=patient_email,
            patient_phone=patient_phone,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            notes=notes
        )
        
        print(f"   ✅ Agendamento criado com sucesso! ID: {appointment.get('id')}")
        
        # Formata resposta de confirmação
        result = {
            "sucesso": True,
            "agendamento_id": appointment.get("id"),
            "paciente": patient_name,
            "medico_id": doctor_id,
            "data": appointment_date,
            "horario": appointment_time,
            "status": appointment.get("status", "scheduled"),
            "mensagem": f"Consulta agendada com sucesso! Número do agendamento: {appointment.get('id')}"
        }
        
        return json.dumps(result, ensure_ascii=False)
    
    except Exception as e:
        error_msg = str(e)
        print(f"   ❌ Erro ao agendar: {error_msg}")
        
        # Trata erros específicos
        if "already exists" in error_msg.lower() or "já existe" in error_msg.lower():
            return "Este horário já está ocupado. Por favor, escolha outro horário disponível."
        elif "not found" in error_msg.lower() or "não encontrado" in error_msg.lower():
            return "Médico não encontrado. Verifique o ID do médico e tente novamente."
        elif "passadas" in error_msg.lower() or "past" in error_msg.lower():
            return "Não é possível agendar consultas para datas passadas."
        else:
            return f"Erro ao agendar consulta: {error_msg}"

@tool
def list_patient_appointments(patient_email: str) -> str:
    """
    Lista todos os agendamentos de um paciente pelo email.
    
    Argumentos:
        patient_email: Email do paciente para buscar os agendamentos
    """
    print(f"📋 EXECUTANDO: list_patient_appointments")
    print(f"   📧 Email do paciente: {patient_email}")
    
    try:
        appointments = client.list_appointments(patient_email=patient_email)
        
        if not appointments:
            print("   ℹ️ Nenhum agendamento encontrado")
            return "Você não possui agendamentos no momento."
        
        print(f"   ✅ {len(appointments)} agendamento(s) encontrado(s)")
        
        # Formata as informações dos agendamentos
        appointments_info = []
        for apt in appointments:
            doctor_info = apt.get('doctor', {})
            info = {
                "agendamento_id": apt.get("id"),
                "paciente": apt.get("patient_name"),
                "medico": doctor_info.get("name", "N/A"),
                "especialidade": doctor_info.get("specialty", "N/A"),
                "estabelecimento": doctor_info.get("establishment_name", "N/A"),
                "data": apt.get("appointment_date"),
                "horario": apt.get("appointment_time"),
                "status": apt.get("status"),
                "observacoes": apt.get("notes")
            }
            appointments_info.append(info)
        
        return json.dumps(appointments_info, ensure_ascii=False)
    
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return f"Erro ao buscar agendamentos: {str(e)}"

@tool
def cancel_patient_appointment(appointment_id: int, patient_email: str) -> str:
    """
    Cancela um agendamento específico do paciente.
    
    Argumentos:
        appointment_id: ID do agendamento a ser cancelado
        patient_email: Email do paciente (para validação)
    """
    print(f"❌ EXECUTANDO: cancel_patient_appointment")
    print(f"   🆔 Agendamento ID: {appointment_id}")
    print(f"   📧 Email do paciente: {patient_email}")
    
    try:
        # Verifica se o agendamento existe e pertence ao paciente
        appointment = client.get_appointment(appointment_id)
        
        if appointment.get("patient_email") != patient_email:
            print("   ⚠️ Email não corresponde ao agendamento")
            return "Erro: Este agendamento não pertence a este email."
        
        if appointment.get("status") == "cancelled":
            print("   ℹ️ Agendamento já estava cancelado")
            return "Este agendamento já foi cancelado anteriormente."
        
        # Cancela o agendamento
        client.cancel_appointment(appointment_id)
        
        print(f"   ✅ Agendamento {appointment_id} cancelado com sucesso")
        
        result = {
            "sucesso": True,
            "agendamento_id": appointment_id,
            "mensagem": f"Agendamento #{appointment_id} cancelado com sucesso.",
            "data_cancelamento": appointment.get("appointment_date"),
            "horario_cancelamento": appointment.get("appointment_time")
        }
        
        return json.dumps(result, ensure_ascii=False)
    
    except Exception as e:
        error_msg = str(e)
        print(f"   ❌ Erro ao cancelar: {error_msg}")
        
        if "404" in error_msg or "not found" in error_msg.lower():
            return f"Agendamento #{appointment_id} não encontrado."
        else:
            return f"Erro ao cancelar agendamento: {error_msg}"

# Cria os nós do grafo
def chatbot(state: MessagesState) -> MessagesState:
    """Nó principal do chatbot que processa mensagens e decide se precisa usar ferramentas."""
    messages = state["messages"]
    
    # Adiciona a mensagem do sistema se ainda não existir
    if not messages or not isinstance(messages[0], SystemMessage):
        system_message = SystemMessage(
            content="""Você é um assistente especializado em ajudar usuários a encontrar profissionais de saúde, estabelecimentos médicos e agendar consultas no Brasil.

CAPACIDADES PRINCIPAIS:

1. 🔍 BUSCA DE PROFISSIONAIS E ESTABELECIMENTOS (POR LOCALIZAÇÃO):
   - Use search_establishments quando o usuário mencionar localização/endereço/proximidade
   - Especialidade médica em determinada região
   - Nome do médico em determinado local
   - Distância (use sempre 2 km como padrão se não especificado)

2. 📅 AGENDAMENTO DE CONSULTAS (SEM LOCALIZAÇÃO):
   - Use list_available_doctors quando o usuário quiser agendar ou ver médicos para agendamento
   - NÃO peça localização para agendamento
   - Agendar consultas com médicos específicos
   - Consultar agendamentos existentes do paciente
   - Cancelar agendamentos

IMPORTANTE - DIFERENCIAR BUSCA DE AGENDAMENTO:
- Se o usuário mencionar "agendar", "disponíveis para agendamento", "marcar consulta" → Use list_available_doctors (NÃO peça localização)
- Se o usuário mencionar "próximo", "perto de", endereço específico → Use search_establishments (peça localização se necessário)

FLUXO RECOMENDADO PARA AGENDAMENTO:

1. Pergunte ao usuário o que ele precisa (busca ou agendamento)
2. Para AGENDAR:
   a. Liste os médicos disponíveis (use list_available_doctors)
   b. Colete informações necessárias:
      - Nome completo do paciente
      - Email (será usado para consultar agendamentos futuros)
      - Telefone com DDD (ex: (11) 98765-4321)
      - Data desejada (formato: YYYY-MM-DD)
      - Horário desejado (formato: HH:MM, ex: 14:30)
      - Observações (opcional)
   c. Confirme os dados antes de agendar
   d. Use schedule_appointment para criar o agendamento
   e. Forneça o número do agendamento e orientações

3. Para CONSULTAR AGENDAMENTOS:
   - Peça o email do paciente
   - Use list_patient_appointments para listar
   - Mostre os agendamentos de forma clara

4. Para CANCELAR:
   - Primeiro liste os agendamentos do paciente
   - Confirme qual agendamento cancelar (ID)
   - Use cancel_patient_appointment

IMPORTANTE:
- Sempre responda em português brasileiro
- Seja cordial e empático
- Confirme informações importantes antes de executar ações
- Forneça números de confirmação de agendamentos
- Oriente sobre como consultar/cancelar agendamentos futuros
- Para datas, use sempre o formato YYYY-MM-DD (ex: 2025-12-15)
- Para horários, use sempre o formato HH:MM (ex: 14:30)

Ferramentas disponíveis:

BUSCA POR LOCALIZAÇÃO (quando usuário menciona endereço/proximidade):
- search_address: Buscar endereços e obter coordenadas geográficas
- get_specialties: Listar todas as especialidades médicas cadastradas
- search_establishments: Buscar estabelecimentos próximos a uma localização específica
- get_establishment_details: Obter detalhes completos de um estabelecimento por CNES

AGENDAMENTO (quando usuário quer marcar consulta - NÃO peça localização):
- list_available_doctors: Listar TODOS os médicos cadastrados no sistema de agendamento (use quando perguntarem sobre médicos para agendar)
- schedule_appointment: Criar um novo agendamento de consulta com médico específico
- list_patient_appointments: Consultar todos os agendamentos de um paciente por email
- cancel_patient_appointment: Cancelar um agendamento específico do paciente"""
        )
    messages = [system_message] + messages
    
    # Inicializa o modelo de linguagem com ferramentas
    tools = [
        search_address, 
        get_specialties, 
        search_establishments, 
        get_establishment_details,
        list_available_doctors,
        schedule_appointment,
        list_patient_appointments,
        cancel_patient_appointment
    ]
    llm = ChatOpenAI(temperature=0.1, model="gpt-4o-mini", api_key="")
    llm_with_tools = llm.bind_tools(tools)    # Invoca o modelo com as mensagens
    response = llm_with_tools.invoke(messages)
    
    # Verifica se o modelo quer usar ferramentas e exibe informações detalhadas
    if hasattr(response, 'tool_calls') and response.tool_calls:
        print(f"🔧 FERRAMENTAS CHAMADAS: {len(response.tool_calls)} ferramenta(s)")
        for i, tool_call in enumerate(response.tool_calls, 1):
            tool_name = tool_call['name']
            tool_args = tool_call.get('args', {})
            print(f"   {i}. 📋 {tool_name}")
            if tool_args:
                for key, value in tool_args.items():
                    print(f"      - {key}: {value}")
        print("➡️ DIRECIONANDO para execução das ferramentas...")
    else:
        print("🏁 FINALIZANDO resposta (sem ferramentas necessárias)")
    
    # Atualiza as mensagens
    updated_messages = messages + [response]
    
    return {"messages": updated_messages}

def should_continue(state: MessagesState) -> str:
    """Decide se deve continuar para as ferramentas ou finalizar."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # Se a última mensagem tem tool_calls, vai para as ferramentas
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    # Senão, finaliza
    return END

# Cria o grafo
def create_agent_graph() -> StateGraph:
    """Cria o grafo do agente LangGraph."""
    workflow = StateGraph(MessagesState)
    
    # Cria as ferramentas disponíveis
    tools = [
        search_address, 
        get_specialties, 
        search_establishments, 
        get_establishment_details,
        list_available_doctors,
        schedule_appointment,
        list_patient_appointments,
        cancel_patient_appointment
    ]
    tool_node = ToolNode(tools)
    
    # Adiciona nós
    workflow.add_node("chatbot", chatbot)
    workflow.add_node("tools", tool_node)
    
    # Define o ponto de entrada
    workflow.set_entry_point("chatbot")
    
    # Adiciona arestas condicionais
    workflow.add_conditional_edges(
        "chatbot",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )
    
    # Após usar ferramentas, volta para o chatbot
    workflow.add_edge("tools", "chatbot")
    
    return workflow

# Inicializa o agente com MemorySaver
memory = MemorySaver()
agent_graph = create_agent_graph()
agent = agent_graph.compile(checkpointer=memory)

def ask_agent(user_input: str, thread_id: str = "02") -> Dict[str, Any]:
    """Função para interagir com o agente."""
    
    print(f"\n🤖 INICIANDO PROCESSAMENTO: '{user_input}'")
    print(f"📱 Thread ID: {thread_id}")
    
    # Configuração da thread para persistência
    config = {"configurable": {"thread_id": thread_id}}
    
    # Cria a mensagem do usuário
    user_message = HumanMessage(content=user_input)
      # Executa o agente com configuração de thread
    result = agent.invoke({"messages": [user_message]}, config=config)
    
    # Extrai a resposta final (última mensagem AI)
    final_messages = result["messages"]
    response_content = ""
    
    # Busca pela última mensagem AI que não seja de ferramenta
    for msg in reversed(final_messages):
        if isinstance(msg, AIMessage):
            # Se não tem tool_calls ou se tem conteúdo
            if not hasattr(msg, 'tool_calls') or not msg.tool_calls or msg.content:
                response_content = msg.content
                break
    
    print(f"✅ PROCESSAMENTO CONCLUÍDO - Resposta pronta!")
    print("-" * 50)
    
    return {
        "response": response_content,
        "thread_id": thread_id
    }