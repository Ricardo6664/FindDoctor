"""
Formatadores para converter respostas JSON em mensagens legíveis do Telegram
"""

import json
from typing import List, Dict, Any

def format_address_results(addresses_json: str) -> str:
    """Formata resultados de busca de endereço."""
    try:
        addresses = json.loads(addresses_json)
        if not addresses:
            return "📍 Nenhum endereço encontrado."
        
        message = "📍 **Endereços encontrados:**\n\n"
        for i, addr in enumerate(addresses[:3], 1):
            message += f"{i}. **{addr.get('display_name', 'Endereço')}**\n"
            if addr.get('lat') and addr.get('lon'):
                message += f"   📌 Coordenadas: {float(addr['lat']):.6f}, {float(addr['lon']):.6f}\n"
            message += "\n"
        
        return message
    except Exception as e:
        return f"❌ Erro ao formatar endereços: {str(e)}"

def format_specialties_results(specialties_json: str) -> str:
    """Formata lista de especialidades médicas."""
    try:
        specialties = json.loads(specialties_json)
        if not specialties:
            return "🏥 Nenhuma especialidade encontrada."
        
        # Agrupa especialidades por categoria/letra inicial
        message = "🏥 **Especialidades Médicas Disponíveis:**\n\n"
        
        # Mostra as 20 primeiras especialidades
        for i, spec in enumerate(specialties[:20], 1):
            name = spec.get('nome', 'Especialidade')
            # Remove "MEDICO" do início se estiver presente
            clean_name = name.replace('MEDICO ', '').title()
            message += f"{i}. {clean_name}\n"
        
        total = len(specialties)
        if total > 20:
            message += f"\n... e mais {total - 20} especialidades\n"
        
        message += f"\n**Total:** {total} especialidades médicas\n"
        message += "\n💡 **Dica:** Digite o nome da especialidade que procura!"
        
        return message
    except Exception as e:
        return f"❌ Erro ao formatar especialidades: {str(e)}"

def format_establishments_results(establishments_json: str) -> str:
    """Formata resultados de estabelecimentos de saúde."""
    try:
        establishments = json.loads(establishments_json)
        if not establishments:
            return "🏥 Nenhum estabelecimento encontrado."
        
        message = "🏥 **Estabelecimentos encontrados:**\n\n"
        
        for i, est in enumerate(establishments[:5], 1):  # Mostra até 5 resultados
            name = est.get('name', 'Nome não informado')
            address = est.get('address', 'Endereço não informado')
            distance = est.get('distance_km', 0)
            phone = est.get('phone', '')
            cnes = est.get('cnes_code', '')
            
            message += f"**{i}. {name}**\n"
            message += f"📍 {address}\n"
            message += f"📏 Distância: {distance:.1f} km\n"
            
            if phone:
                message += f"📞 {phone}\n"
            if cnes:
                message += f"🆔 CNES: {cnes}\n"
            
            message += "\n"
        
        total = len(establishments)
        if total > 5:
            message += f"... e mais {total - 5} estabelecimentos\n\n"
        
        message += "💡 **Para mais detalhes** de um estabelecimento, me informe o código CNES!"
        
        return message
    except Exception as e:
        return f"❌ Erro ao formatar estabelecimentos: {str(e)}"

def format_establishment_details(details_json: str) -> str:
    """Formata detalhes de um estabelecimento específico."""
    try:
        details = json.loads(details_json)
        if not details:
            return "🏥 Detalhes não encontrados."
        
        name = details.get('name', 'Nome não informado')
        address = details.get('address', 'Endereço não informado')
        phone = details.get('phone', 'Não informado')
        cnes = details.get('cnes_code', 'Não informado')
        type_desc = details.get('type_description', 'Não informado')
        
        message = f"🏥 **{name}**\n\n"
        message += f"📍 **Endereço:** {address}\n"
        message += f"📞 **Telefone:** {phone}\n"
        message += f"🆔 **CNES:** {cnes}\n"
        message += f"🏥 **Tipo:** {type_desc}\n"
        
        # Adiciona especialidades se disponível
        if details.get('specialties'):
            message += f"\n🩺 **Especialidades:**\n"
            for spec in details['specialties'][:10]:  # Máximo 10 especialidades
                spec_name = spec.get('name', '').replace('MEDICO ', '').title()
                message += f"• {spec_name}\n"
        
        # Adiciona profissionais se disponível
        if details.get('professionals'):
            message += f"\n👨‍⚕️ **Profissionais:**\n"
            for prof in details['professionals'][:5]:  # Máximo 5 profissionais
                prof_name = prof.get('name', 'Nome não informado')
                prof_spec = prof.get('specialty', '').replace('MEDICO ', '').title()
                message += f"• {prof_name}"
                if prof_spec:
                    message += f" - {prof_spec}"
                message += "\n"
        
        return message
    except Exception as e:
        return f"❌ Erro ao formatar detalhes: {str(e)}"

def split_long_message(message: str, max_length: int = 4096) -> List[str]:
    """Divide mensagens longas em múltiplas mensagens."""
    if len(message) <= max_length:
        return [message]
    
    messages = []
    current_message = ""
    
    lines = message.split('\n')
    for line in lines:
        if len(current_message + line + '\n') <= max_length:
            current_message += line + '\n'
        else:
            if current_message:
                messages.append(current_message.strip())
                current_message = line + '\n'
            else:
                # Linha muito longa, força divisão
                messages.append(line[:max_length])
                current_message = line[max_length:] + '\n'
    
    if current_message:
        messages.append(current_message.strip())
    
    return messages

def format_agent_response(response_content: str) -> str:
    """Formata resposta geral do agente."""
    if not response_content:
        return "❓ Não entendi sua solicitação. Pode reformular?"
    
    # Limpa possíveis artefatos JSON
    if response_content.startswith('[') or response_content.startswith('{'):
        return "📋 Recebi os dados, mas preciso de mais informações para processá-los adequadamente."
    
    return response_content
