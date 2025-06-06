from finddoctor_agent import ask_agent

def main():
    print("Agente FindDoctor - Encontre Profissionais de Saúde")
    print("Digite 'sair' ou 'exit' para encerrar")
    print("-" * 50)
    
    while True:
        user_input = input("Você: ")
        
        if user_input.lower() in ["exit", "quit", "sair", "sair()"]:
            print("Encerrando o programa. Até logo!")
            break
        
        # Processa com o agente (sem histórico complexo)
        result = ask_agent(user_input)
        
        print(f"\nAssistente: {result['response']}")
        print("-" * 50)

if __name__ == "__main__":
    main()