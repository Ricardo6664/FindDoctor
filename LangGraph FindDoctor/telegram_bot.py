"""
Bot Telegram para o FindDoctor Agent
Implementação local que conecta ao agente LangGraph existente
"""

import logging
import json
import threading
from typing import Dict, Any
import telebot
from telebot import types

# Imports locais
from finddoctor_agent import ask_agent
from formatters import (
    format_address_results, 
    format_specialties_results, 
    format_establishments_results,
    format_establishment_details,
    split_long_message,
    format_agent_response
)
from config import (
    TELEGRAM_BOT_TOKEN, 
    WELCOME_MESSAGE, 
    HELP_MESSAGE, 
    ERROR_MESSAGE,
    PROCESSING_MESSAGE,
    NO_RESULTS_MESSAGE,
    MAX_MESSAGE_LENGTH
)

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class FindDoctorTelegramBot:
    def __init__(self):
        # Verifica se o token foi configurado
        if TELEGRAM_BOT_TOKEN == "SEU_TOKEN_AQUI":
            print("❌ ERRO: Configure seu token do Telegram no arquivo config.py!")
            print("   1. Abra config.py")
            print("   2. Substitua 'SEU_TOKEN_AQUI' pelo token do @BotFather")
            return
        
        self.bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
        self.user_reset_counts = {}  # Para gerenciar resets por usuário
        self.setup_handlers()
    
    def get_thread_id(self, user_id: int) -> str:
        """Gera thread_id único por usuário, considerando resets"""
        reset_count = self.user_reset_counts.get(user_id, 0)
        return f"{user_id}_{reset_count}"
    
    def create_main_keyboard(self):
        """Cria teclado principal com comandos"""
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton("🩺 Ver Especialidades", callback_data="especialidades")
        )
        keyboard.row(
            types.InlineKeyboardButton("ℹ️ Ajuda", callback_data="help"),
            types.InlineKeyboardButton("🔄 Reset Conversa", callback_data="reset")
        )
        return keyboard
    
    def setup_handlers(self):
        """Configura todos os handlers do bot"""
        
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            """Comando /start - Boas-vindas"""
            user_id = message.from_user.id
            user_name = message.from_user.first_name
            
            logger.info(f"Usuário {user_name} (ID: {user_id}) iniciou o bot")
            
            keyboard = self.create_main_keyboard()
            
            self.bot.reply_to(
                message,
                WELCOME_MESSAGE,
                parse_mode='Markdown',
                reply_markup=keyboard
            )
        
        @self.bot.message_handler(commands=['help'])
        def help_command(message):
            """Comando /help - Ajuda"""
            self.bot.reply_to(message, HELP_MESSAGE, parse_mode='Markdown')
        
        @self.bot.message_handler(commands=['reset'])
        def reset_command(message):
            """Comando /reset - Limpar conversa"""
            user_id = message.from_user.id
            
            # Incrementa contador de reset
            if user_id not in self.user_reset_counts:
                self.user_reset_counts[user_id] = 0
            self.user_reset_counts[user_id] += 1
            
            self.bot.reply_to(
                message,
                "🔄 **Conversa reiniciada!**\n\n"
                "Seu histórico foi limpo. Como posso ajudar você agora?",
                parse_mode='Markdown'
            )
        
        @self.bot.message_handler(commands=['especialidades'])
        def specialties_command(message):
            """Comando /especialidades - Mostrar especialidades"""
            processing_msg = self.bot.reply_to(message, PROCESSING_MESSAGE)
            
            try:
                user_id = self.get_thread_id(message.from_user.id)
                
                # Chama o agente para obter especialidades
                result = ask_agent("Mostre todas as especialidades médicas disponíveis", thread_id=user_id)
                response = result.get('response', '')
                
                # Deleta mensagem de processamento
                self.bot.delete_message(message.chat.id, processing_msg.message_id)
                
                # Formata resposta
                formatted_response = self.format_response_by_content(response)
                
                # Divide mensagem se muito longa
                messages = split_long_message(formatted_response, MAX_MESSAGE_LENGTH)
                for msg in messages:
                    self.bot.send_message(message.chat.id, msg, parse_mode='Markdown')
                    
            except Exception as e:
                logger.error(f"Erro ao buscar especialidades: {e}")
                self.bot.delete_message(message.chat.id, processing_msg.message_id)
                self.bot.reply_to(message, ERROR_MESSAGE)
        
        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            """Manipula mensagens de texto do usuário"""
            user_message = message.text
            user_id = self.get_thread_id(message.from_user.id)
            user_name = message.from_user.first_name
            
            logger.info(f"Mensagem de {user_name} (ID: {user_id}): {user_message}")
            
            # Mostra indicador de "digitando"
            self.bot.send_chat_action(message.chat.id, 'typing')
            
            # Envia mensagem de processamento
            processing_msg = self.bot.reply_to(message, PROCESSING_MESSAGE)
            
            try:
                # Chama o agente FindDoctor
                result = ask_agent(user_message, thread_id=user_id)
                response = result.get('response', '')
                
                # Deleta mensagem de processamento
                self.bot.delete_message(message.chat.id, processing_msg.message_id)
                
                if not response:
                    self.bot.reply_to(message, NO_RESULTS_MESSAGE)
                    return
                
                # Formata resposta baseada no tipo de conteúdo
                formatted_response = self.format_response_by_content(response)
                
                # Divide mensagem se muito longa
                messages = split_long_message(formatted_response, MAX_MESSAGE_LENGTH)
                for msg in messages:
                    self.bot.send_message(message.chat.id, msg, parse_mode='Markdown')
                
            except Exception as e:
                logger.error(f"Erro ao processar mensagem: {e}")
                try:
                    self.bot.delete_message(message.chat.id, processing_msg.message_id)
                except:
                    pass
                self.bot.reply_to(message, ERROR_MESSAGE)
        
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callback(call):
            """Manipula cliques em botões inline"""
            try:
                self.bot.answer_callback_query(call.id)
                
                if call.data == "especialidades":
                    # Simula comando de especialidades
                    message = call.message
                    message.from_user = call.from_user
                    specialties_command(message)
                    
                elif call.data == "help":
                    self.bot.edit_message_text(
                        HELP_MESSAGE,
                        call.message.chat.id,
                        call.message.message_id,
                        parse_mode='Markdown'
                    )
                    
                elif call.data == "reset":
                    user_id = call.from_user.id
                    
                    # Incrementa contador de reset
                    if user_id not in self.user_reset_counts:
                        self.user_reset_counts[user_id] = 0
                    self.user_reset_counts[user_id] += 1
                    
                    self.bot.edit_message_text(
                        "🔄 **Conversa reiniciada!**\n\n"
                        "Seu histórico foi limpo. Como posso ajudar você agora?",
                        call.message.chat.id,
                        call.message.message_id,
                        parse_mode='Markdown'
                    )
                    
            except Exception as e:
                logger.error(f"Erro ao processar callback: {e}")
    
    def format_response_by_content(self, response: str) -> str:
        """Formata resposta baseada no conteúdo"""
        try:
            # Tenta detectar se há JSON na resposta e formatar adequadamente
            if '[' in response and ']' in response:
                # Procura por padrões JSON específicos
                if '"lat"' in response and '"lon"' in response:
                    # É resultado de endereço
                    json_start = response.find('[')
                    json_end = response.rfind(']') + 1
                    json_content = response[json_start:json_end]
                    return format_address_results(json_content)
                
                elif '"cnes_code"' in response or '"name"' in response:
                    # É resultado de estabelecimentos
                    json_start = response.find('[')
                    json_end = response.rfind(']') + 1
                    json_content = response[json_start:json_end]
                    return format_establishments_results(json_content)
                
                elif '"id"' in response and '"nome"' in response:
                    # É lista de especialidades
                    json_start = response.find('[')
                    json_end = response.rfind(']') + 1
                    json_content = response[json_start:json_end]
                    return format_specialties_results(json_content)
            
            elif '{' in response and '}' in response:
                # Pode ser detalhes de um estabelecimento
                if '"cnes_code"' in response:
                    json_start = response.find('{')
                    json_end = response.rfind('}') + 1
                    json_content = response[json_start:json_end]
                    return format_establishment_details(json_content)
            
            # Se não é JSON, retorna formatação padrão
            return format_agent_response(response)
            
        except Exception as e:
            logger.error(f"Erro ao formatar resposta: {e}")
            return format_agent_response(response)
    
    def start_bot(self):
        """Inicia o bot"""
        print("🤖 FindDoctor Telegram Bot iniciando...")
        print("📱 Aguardando mensagens...")
        print("🛑 Pressione Ctrl+C para parar")
        
        try:
            # Inicia o bot
            self.bot.polling(none_stop=True)
        except Exception as e:
            logger.error(f"Erro no bot: {e}")
            raise

def main():
    """Função principal"""
    bot = FindDoctorTelegramBot()
    try:
        bot.start_bot()
    except KeyboardInterrupt:
        print("\n🛑 Bot parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar bot: {e}")

if __name__ == "__main__":
    main()
