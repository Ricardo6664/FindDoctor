"""
Configurações do bot Telegram FindDoctor
"""

# Token do bot Telegram (substitua pelo seu token do @BotFather)
TELEGRAM_BOT_TOKEN = ""

# Configurações do agente
DEFAULT_RADIUS_KM = 1
MAX_MESSAGE_LENGTH = 4096
MAX_RESULTS_PER_MESSAGE = 5

# Mensagens do bot
WELCOME_MESSAGE = """
🏥 **Bem-vindo ao FindDoctor Bot!**

Sou seu assistente para encontrar profissionais de saúde e estabelecimentos médicos no Brasil.

**Como posso ajudar:**
• 📍 Buscar médicos por localização
• 🩺 Filtrar por especialidade médica
• 👨‍⚕️ Encontrar médicos específicos
• 🏥 Obter detalhes de estabelecimentos

**Comandos disponíveis:**
/start - Mostrar esta mensagem
/help - Ajuda detalhada
/especialidades - Ver especialidades disponíveis
/reset - Limpar histórico da conversa

**Exemplo de uso:**
"Quero encontrar um cardiologista em São Paulo"
"Buscar pediatras próximos à Rua Augusta, 123"

Digite sua solicitação para começar!
"""

HELP_MESSAGE = """
🆘 **Ajuda - Como usar o FindDoctor Bot**

**Tipos de busca:**
1️⃣ **Por especialidade e local:**
   "Quero um cardiologista em Copacabana"
   
2️⃣ **Por endereço específico:**
   "Pediatra próximo à Av. Paulista, 1000"
   
3️⃣ **Por médico específico:**
   "Dr. João Silva cardiologista"

**Comandos:**
• `/especialidades` - Lista todas as especialidades
• `/reset` - Limpa seu histórico de conversa
• `/help` - Mostra esta ajuda

**Dicas:**
• Seja específico com a localização
• Pode usar nomes de bairros, ruas ou cidades
• O bot lembra da conversa anterior
• Use /reset se quiser começar do zero

Precisa de mais alguma coisa? É só perguntar! 😊
"""

ERROR_MESSAGE = "❌ Desculpe, ocorreu um erro. Tente novamente em alguns instantes."
PROCESSING_MESSAGE = "🔄 Processando sua solicitação..."
NO_RESULTS_MESSAGE = "😔 Não encontrei resultados para sua busca. Tente refinar os critérios."
