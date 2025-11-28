# 🏥 FindDoctor Bot - Assistente Inteligente para Busca de Profissionais de Saúde e Agendamento de Consultas

Um bot inteligente desenvolvido com **LangGraph** e **OpenAI GPT** para ajudar usuários a encontrar profissionais de saúde, estabelecimentos médicos e **agendar consultas** no Brasil. O projeto oferece tanto uma interface de linha de comando quanto um bot do Telegram.

## 📋 Índice

- [Características](#-características)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Como Usar](#-como-usar)
- [API Endpoints](#-api-endpoints)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Troubleshooting](#-troubleshooting)
- [Contribuindo](#-contribuindo)

## ✨ Características

### 🔍 **Funcionalidades Principais**
- **Busca por Localização**: Encontre médicos próximos a um endereço específico
- **Filtro por Especialidade**: Mais de 80 especialidades médicas disponíveis
- **Busca por Nome**: Procure médicos específicos por nome
- **Detalhes Completos**: Informações detalhadas sobre estabelecimentos (CNES, telefone, endereço)
- **Geolocalização**: Suporte a coordenadas geográficas para buscas precisas

### 📅 **Agendamento de Consultas** (NOVO!)
- **Agendar Consultas**: Marque consultas com médicos disponíveis de forma conversacional
- **Consultar Agendamentos**: Veja todos os seus agendamentos usando seu email
- **Cancelar Agendamentos**: Cancele consultas de forma simples e rápida
- **Confirmação Automática**: Receba número de confirmação e detalhes do agendamento
- **Validação Inteligente**: Sistema verifica disponibilidade e previne conflitos

### 🤖 **Tecnologias**
- **LangGraph**: Framework para criação de agentes conversacionais
- **OpenAI GPT-4**: Modelo de linguagem para processamento de linguagem natural
- **Telegram Bot API**: Interface de chat via Telegram
- **Pydantic**: Validação e modelagem de dados
- **Requests**: Cliente HTTP para APIs externas

### 💬 **Interfaces Disponíveis**
- **Terminal/CLI**: Interface de linha de comando para teste e desenvolvimento
- **Telegram Bot**: Bot completo com comandos e teclados inline
- **API REST**: Integração com API FindDoctor externa

## 🏗️ Arquitetura

O projeto segue uma arquitetura modular baseada em **LangGraph**:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Telegram Bot  │───▶│   FindDoctor     │───▶│   API Externa   │
│   Interface     │    │   Agent          │    │   FindDoctor    │
└─────────────────┘    │   (LangGraph)    │    └─────────────────┘
                       └──────────────────┘
                                │
                       ┌──────────────────┐
                       │   Ferramentas    │
                       │   - search_address
                       │   - get_specialties
                       │   - search_establishments
                       │   - get_establishment_details
                       └──────────────────┘
```

### 📊 **Fluxo de Processamento**

1. **Entrada do Usuário**: Recebe mensagem via Telegram ou terminal
2. **Análise de Intenção**: LLM analisa o que o usuário deseja
3. **Seleção de Ferramentas**: Escolhe as ferramentas necessárias
4. **Execução**: Chama APIs externas ou consulta dados locais
5. **Formatação**: Formata resposta de forma legível
6. **Resposta**: Envia resultado final ao usuário

## 📋 Pré-requisitos

- **Python 3.8+**
- **API Key do OpenAI** (GPT-4)
- **Token do Bot Telegram** (opcional, apenas para interface Telegram)
- **API FindDoctor** rodando em `http://localhost:5210`

## 🚀 Instalação

### 1. Clone o Repositório
```bash
git clone <url-do-repositorio>
cd LangGraph\ FindDoctor
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 3. Configuração das Variáveis de Ambiente

Crie um arquivo `.env` ou configure diretamente no código:

```bash
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Telegram Bot Token (opcional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

## ⚙️ Configuração

### 1. Configure a API Key do OpenAI

No arquivo `finddoctor_agent.py`, linha 170:
```python
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key="SUA_API_KEY_AQUI")
```

### 2. Configure o Token do Telegram (Opcional)

No arquivo `config.py`:
```python
TELEGRAM_BOT_TOKEN = "SEU_TOKEN_DO_TELEGRAM_AQUI"
```

### 3. Verifique a API Externa

Certifique-se de que a API FindDoctor está rodando em:
```
http://localhost:5210
```

## 🖥️ Como Usar

### 💻 **Interface de Terminal**

Execute o script principal:
```bash
python main.py
```

Exemplos de comandos:
```
Você: Quero encontrar um cardiologista em São Paulo
Você: Buscar pediatras próximos à Rua Augusta, 123
Você: Mostre todas as especialidades disponíveis
Você: sair
```

### 📱 **Bot do Telegram**

1. Inicie o bot:
```bash
python telegram_bot.py
```

2. No Telegram, use os comandos:
- `/start` - Iniciar bot e ver menu principal
- `/help` - Ajuda detalhada
- `/especialidades` - Listar especialidades médicas
- `/reset` - Limpar histórico da conversa

3. Ou envie mensagens naturais:
- "Preciso de um dermatologista em Copacabana"
- "Médicos próximos ao CEP 01310-100"

## 🔌 API Endpoints

O projeto consome uma API externa com os seguintes endpoints:

### 📍 **Busca de Endereços**
```
GET /api/Address/buscar?endereco={endereco}
```

### 🏥 **Estabelecimentos Próximos**
```
GET /api/Estabelecimento/proximos?latitude={lat}&longitude={lon}&raioKm={raio}&especialidadeId={id}&nomeMedico={nome}
```

### 🆔 **Detalhes do Estabelecimento**
```
GET /api/Estabelecimento/{cnes_code}
```

### 🩺 **Especialidades Médicas**
```
GET /api/Especialidade
```

## 📁 Estrutura do Projeto

```
LangGraph FindDoctor/
├── 📄 main.py                      # Interface CLI principal
├── 📄 telegram_bot.py              # Bot do Telegram
├── 📄 finddoctor_agent.py          # Agente LangGraph principal
├── 📄 finddoctor_api_client.py     # Cliente da API externa
├── 📄 formatters.py                # Formatadores de resposta
├── 📄 models.py                    # Modelos Pydantic
├── 📄 config.py                    # Configurações do bot
├── 📄 requirements.txt             # Dependências Python
├── 📄 medical_specialties.json     # Base de especialidades médicas
└── 📄 README.md                    # Documentação (este arquivo)
```

### 📋 **Descrição dos Arquivos**

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | Interface de linha de comando para testar o agente |
| `telegram_bot.py` | Implementação completa do bot Telegram |
| `finddoctor_agent.py` | Core do agente com LangGraph e ferramentas |
| `finddoctor_api_client.py` | Cliente HTTP para consumir API externa |
| `formatters.py` | Funções para formatar respostas JSON em texto legível |
| `models.py` | Modelos de dados usando Pydantic |
| `config.py` | Constantes e configurações do bot |
| `medical_specialties.json` | Base local de especialidades médicas (performance) |

## 💡 Exemplos de Uso

### 🔍 **Busca por Especialidade e Local**
```
Usuário: "Quero um cardiologista em Ipanema"

Bot: 🏥 Estabelecimentos encontrados:

1. **Clínica Cardiológica Ipanema**
📍 Rua Visconde de Pirajá, 550 - Ipanema
📏 Distância: 0.3 km
📞 (21) 2512-3456
🆔 CNES: 2269941

2. **Hospital Copa D'Or**
📍 Rua Figueiredo de Magalhães, 875
📏 Distância: 1.2 km
📞 (21) 2545-3600
🆔 CNES: 2270000
```

### 📍 **Busca por Endereço Específico**
```
Usuário: "Pediatra próximo à Av. Paulista, 1000"

Bot: 🏥 Estabelecimentos encontrados:

1. **Hospital Albert Einstein - Unidade Paulista**
📍 Av. Paulista, 2001 - Bela Vista
📏 Distância: 0.5 km
📞 (11) 2151-1233
```

### 📅 **Agendamento de Consulta** (NOVO!)
```
Usuário: "Quero agendar uma consulta"

Bot: Claro! Vou te ajudar a agendar. Primeiro, me diga:
- Qual especialidade você precisa?
- Qual sua localização?

Usuário: "Cardiologista em Marília"

Bot: Encontrei os seguintes médicos disponíveis para agendamento:

1. **Dr. João Silva** - Cardiologia
   🏥 Clínica Saúde Total
   📋 CRM: 123456-SP

2. **Dra. Maria Santos** - Pediatria
   🏥 Clínica Saúde Total
   📋 CRM: 234567-SP

Qual médico você prefere? (Digite o número ou nome)

Usuário: "Dr. João Silva"

Bot: Perfeito! Agora preciso de algumas informações:
- Seu nome completo
- Seu email
- Seu telefone com DDD
- Data desejada (ex: 2025-12-15)
- Horário desejado (ex: 14:30)

Usuário: "João da Silva, joao@email.com, (14) 98765-4321, 2025-12-10, 14:30"

Bot: ✅ Consulta agendada com sucesso!

📋 **Detalhes do Agendamento:**
🆔 Número: #123
👤 Paciente: João da Silva
👨‍⚕️ Médico: Dr. João Silva - Cardiologia
📅 Data: 10/12/2025
⏰ Horário: 14:30
🏥 Local: Clínica Saúde Total

📧 Um email de confirmação foi enviado para joao@email.com
💡 Para consultar ou cancelar, use seu email.
```

### 📋 **Consultar Meus Agendamentos**
```
Usuário: "Quero ver meus agendamentos"

Bot: Por favor, me informe seu email para consultar.

Usuário: "joao@email.com"

Bot: 📋 **Seus Agendamentos:**

1. **Agendamento #123** ✅ Agendada
   👨‍⚕️ Dr. João Silva - Cardiologia
   🏥 Clínica Saúde Total
   📅 10/12/2025 às 14:30

2. **Agendamento #456** ✅ Confirmada
   👨‍⚕️ Dra. Ana Costa - Oftalmologia
   🏥 Hospital São Lucas
   📅 15/12/2025 às 10:00

Deseja cancelar alguma consulta?
```

### ❌ **Cancelar Agendamento**
```
Usuário: "Quero cancelar a consulta #123"

Bot: Para confirmar o cancelamento, preciso do seu email.

Usuário: "joao@email.com"

Bot: ✅ Agendamento #123 cancelado com sucesso!

📋 **Consulta Cancelada:**
📅 Data: 10/12/2025
⏰ Horário: 14:30
👨‍⚕️ Médico: Dr. João Silva

Se precisar reagendar, é só me avisar!
```

### 👨‍⚕️ **Busca por Médico Específico**
```
Usuário: "Dr. João Silva cardiologista"

Bot: 🏥 Estabelecimentos com Dr. João Silva:

1. **Clínica São Lucas**
📍 Rua das Flores, 123 - Centro
👨‍⚕️ Dr. João Silva - Cardiologista
📞 (11) 3456-7890
```

### 🩺 **Listar Especialidades**
```
Usuário: "/especialidades"

Bot: 🏥 Especialidades Médicas Disponíveis:

1. Cardiologista
2. Pediatra
3. Ginecologista E Obstetra
4. Ortopedista E Traumatologista
5. Dermatologista
...

**Total:** 80+ especialidades médicas
```

## 🛠️ Troubleshooting

### ❌ **Problemas Comuns**

#### 🔑 **API Key não configurada**
```
Erro: OpenAI API key not configured
Solução: Configure a API key no arquivo finddoctor_agent.py
```

#### 🌐 **API Externa indisponível**
```
Erro: Connection refused to localhost:5210
Solução: Verifique se a API FindDoctor está rodando na porta 5210
```

#### 📱 **Token do Telegram inválido**
```
Erro: Unauthorized (401)
Solução: Verifique o token no arquivo config.py
```

#### 📦 **Dependências faltando**
```
Erro: ModuleNotFoundError
Solução: Execute pip install -r requirements.txt
```

### 🔧 **Logs e Debug**

Para ativar logs detalhados, execute:
```bash
python telegram_bot.py  # Logs automáticos ativados
```

Os logs mostram:
- 🤖 Processamento de mensagens
- 🔧 Ferramentas executadas
- 📊 Resultados das APIs
- ❌ Erros e exceções

## 🤝 Contribuindo

### 📝 **Como Contribuir**

1. **Fork** o projeto
2. Crie uma **branch** para sua feature: `git checkout -b feature/nova-funcionalidade`
3. **Commit** suas mudanças: `git commit -am 'Adiciona nova funcionalidade'`
4. **Push** para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um **Pull Request**

### 🧪 **Testes**

Para testar o projeto:

1. **Teste CLI**:
```bash
python main.py
```

2. **Teste Telegram Bot**:
```bash
python telegram_bot.py
```

3. **Teste Ferramentas Individuais**:
```python
from finddoctor_agent import search_address, get_specialties
print(search_address("São Paulo"))
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Desenvolvedor Principal** - [Seu Nome]
- **Colaboradores** - Lista de colaboradores

---

## 🔗 Links Úteis

- [Documentação LangGraph](https://langchain-ai.github.io/langgraph/)
- [OpenAI API](https://platform.openai.com/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

*Desenvolvido com ❤️ para facilitar o acesso a informações de saúde no Brasil*
