"""
Script de teste para as funcionalidades de agendamento
"""

from finddoctor_agent import ask_agent

def test_list_doctors():
    """Testa a listagem de médicos disponíveis"""
    print("\n" + "="*60)
    print("TESTE 1: Listar médicos disponíveis")
    print("="*60)
    
    response = ask_agent("Mostre os médicos disponíveis para agendamento, não tenho preferências por médicos", thread_id="test_01")
    print(f"\n📝 Resposta:\n{response['response']}")

def test_schedule_appointment():
    """Testa o agendamento de consulta"""
    print("\n" + "="*60)
    print("TESTE 2: Agendar uma consulta")
    print("="*60)
    
    # Primeiro, lista os médicos
    response1 = ask_agent("Liste os médicos disponíveis", thread_id="test_02")
    print(f"\n📝 Médicos disponíveis:\n{response1['response']}")
    
    # Depois, tenta agendar
    response2 = ask_agent(
        "Quero agendar com o médico ID 5 para o paciente Teste Silva, "
        "email teste@email.com, telefone (11) 98765-4321, "
        "data 2025-12-15, horário 14:30",
        thread_id="test_02"
    )
    print(f"\n📝 Resultado do agendamento:\n{response2['response']}")

def test_list_appointments():
    """Testa a consulta de agendamentos"""
    print("\n" + "="*60)
    print("TESTE 3: Consultar agendamentos")
    print("="*60)
    
    response = ask_agent(
        "Quero ver meus agendamentos. Meu email é joao@email.com",
        thread_id="test_03"
    )
    print(f"\n📝 Agendamentos encontrados:\n{response['response']}")

def test_cancel_appointment():
    """Testa o cancelamento de agendamento"""
    print("\n" + "="*60)
    print("TESTE 4: Cancelar agendamento")
    print("="*60)
    
    # Primeiro lista para ver os IDs
    response1 = ask_agent(
        "Liste meus agendamentos, email: joao@email.com",
        thread_id="test_04"
    )
    print(f"\n📝 Agendamentos atuais:\n{response1['response']}")
    
    # Depois tenta cancelar (ajuste o ID conforme necessário)
    # response2 = ask_agent(
    #     "Cancele o agendamento #6 para o email joao@email.com",
    #     thread_id="test_04"
    # )
    # print(f"\n📝 Resultado do cancelamento:\n{response2['response']}")

def test_full_flow():
    """Testa o fluxo completo de conversa"""
    print("\n" + "="*60)
    print("TESTE 5: Fluxo conversacional completo")
    print("="*60)
    
    thread_id = "test_05"
    
    # Conversa natural
    mensagens = [
        "Olá! Quero agendar uma consulta",
        "Preciso de um cardiologista",
        "Pode mostrar os médicos disponíveis?",
    ]
    
    for msg in mensagens:
        print(f"\n👤 Usuário: {msg}")
        response = ask_agent(msg, thread_id=thread_id)
        print(f"🤖 Bot: {response['response']}")

if __name__ == "__main__":
    print("\n🧪 INICIANDO TESTES DE AGENDAMENTO")
    print("="*60)
    
    # Escolha qual teste executar:
    
    # test_list_doctors()
    # test_schedule_appointment()
    # test_list_appointments()
    # test_cancel_appointment()
    test_full_flow()
    
    print("\n" + "="*60)
    print("✅ TESTES CONCLUÍDOS")
    print("="*60)
