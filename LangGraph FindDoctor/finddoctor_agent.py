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
client = FindDoctorApiClient("http://localhost:5210")

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
    radius_km: float = 5,
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

# Cria os nós do grafo
def chatbot(state: MessagesState) -> MessagesState:
    """Nó principal do chatbot que processa mensagens e decide se precisa usar ferramentas."""
    messages = state["messages"]
    
    # Adiciona a mensagem do sistema se ainda não existir
    if not messages or not isinstance(messages[0], SystemMessage):
        system_message = SystemMessage(
            content="""Você é um assistente especializado em ajudar usuários a encontrar profissionais de saúde e estabelecimentos médicos no Brasil.

Você pode ajudar os usuários a buscar médicos e estabelecimentos de saúde baseado em:
1. Localização/endereço
2. Especialidade médica
3. Nome do médico
4. Distância (raio em km)

Siga estes passos para ajudar o usuário:
1. Primeiro, determine o que o usuário está procurando - busca de endereço ou busca de profissional de saúde
2. Se necessário, pergunte por qualquer informação que esteja faltando, como localização ou especialidade
3. Use a ferramenta apropriada para buscar as informações
4. Apresente os resultados de forma clara e estruturada
5. Ofereça-se para refinar a busca ou obter mais detalhes se necessário

Lembre-se de que todos os endereços e dados de saúde são do Brasil. Sempre responda em português brasileiro.
Quando apresentar resultados, seja claro e organize as informações de forma fácil de entender.
Se houver muitos resultados, mostre os mais relevantes primeiro e ofereça para mostrar mais se o usuário quiser.

Ferramentas disponíveis:
- search_address: Para buscar endereços e obter coordenadas
- get_specialties: Para listar especialidades médicas disponíveis (carregadas do arquivo filtrado para performance otimizada)
- search_establishments: Para buscar estabelecimentos de saúde próximos (busca automaticamente o ID da especialidade do arquivo filtrado)
- get_establishment_details: Para obter detalhes de um estabelecimento específico"""
        )
        messages = [system_message] + messages    # Inicializa o modelo de linguagem com ferramentas
    tools = [search_address, get_specialties, search_establishments, get_establishment_details]
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key="")
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
    workflow = StateGraph(MessagesState)    # Cria as ferramentas disponíveis
    tools = [search_address, get_specialties, search_establishments, get_establishment_details]
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