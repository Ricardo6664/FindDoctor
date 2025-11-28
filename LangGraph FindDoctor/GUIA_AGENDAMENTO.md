# 📅 Guia Rápido - Funcionalidades de Agendamento

## 🎯 Visão Geral

O FindDoctor Agent agora possui **funcionalidades completas de agendamento de consultas**, permitindo que os usuários:

1. ✅ **Listem médicos disponíveis** para agendamento
2. ✅ **Agendem consultas** de forma conversacional
3. ✅ **Consultem seus agendamentos** usando email
4. ✅ **Cancelem agendamentos** quando necessário

---

## 🔧 Configuração

### 1. APIs Necessárias

Certifique-se de que as seguintes APIs estão rodando:

```bash
# API de Busca de Estabelecimentos (C#)
http://localhost:5210

# API de Agendamentos (Python FastAPI)
http://localhost:8000
```

### 2. Verificar Conexão

```python
# Teste rápido de conexão
import requests

# Testa API de agendamentos
response = requests.get("http://localhost:8000/api/doctors/")
print(f"Status: {response.status_code}")
print(f"Médicos disponíveis: {len(response.json())}")
```

---

## 🚀 Exemplos de Uso

> **⚠️ IMPORTANTE - Diferença entre Busca e Agendamento:**
> 
> - **Para AGENDAR**: Use frases como "médicos disponíveis para agendamento", "quero agendar", "marcar consulta"
>   - O sistema lista os médicos cadastrados **SEM pedir localização**
> 
> - **Para BUSCAR por localização**: Use frases como "cardiologista perto de mim", "médico próximo à Av. Paulista"
>   - O sistema pede endereço e busca estabelecimentos próximos

### 📋 Exemplo 1: Listar Médicos Disponíveis

**Entrada do usuário:**
```
"Quais médicos estão disponíveis para agendamento?"
OU
"Mostre os médicos para agendar consulta"
OU
"Com quais médicos posso marcar consulta?"
```

**O que acontece:**
- O agente **NÃO** pede localização
- Lista **TODOS** os médicos cadastrados no sistema de agendamento
- Mostra informações: nome, especialidade, CRM, estabelecimento

**Resposta esperada:**
```
Encontrei os seguintes médicos disponíveis:

1. Dr. João Silva - Cardiologia
   CRM: 123456-SP
   Estabelecimento: Clínica Saúde Total

2. Dra. Maria Santos - Pediatria
   CRM: 234567-SP
   Estabelecimento: Clínica Saúde Total

Gostaria de agendar com algum deles?
```

---

### 📅 Exemplo 2: Agendar Consulta

**Conversação:**

```
Usuário: "Quero agendar uma consulta com o Dr. João Silva"

Bot: "Ótimo! Para agendar sua consulta com o Dr. João Silva, preciso de algumas informações:

1. Seu nome completo
2. Seu email (para confirmação e consultas futuras)
3. Seu telefone com DDD
4. Data desejada (formato: YYYY-MM-DD, ex: 2025-12-15)
5. Horário desejado (formato: HH:MM, ex: 14:30)

Por favor, me informe esses dados."

Usuário: "João da Silva, joao@email.com, (14) 98765-4321, 2025-12-10, 14:30"

Bot: "✅ Consulta agendada com sucesso!

📋 Detalhes do Agendamento:
🆔 Número: #8
👤 Paciente: João da Silva
📧 Email: joao@email.com
👨‍⚕️ Médico: Dr. João Silva - Cardiologia
📅 Data: 2025-12-10
⏰ Horário: 14:30
✅ Status: Agendada

💡 Importante:
- Guarde o número do agendamento (#8)
- Use seu email (joao@email.com) para consultar ou cancelar
- Você pode verificar seus agendamentos a qualquer momento dizendo 'meus agendamentos'"
```

---

### 🔍 Exemplo 3: Consultar Agendamentos

**Entrada do usuário:**
```
"Quero ver meus agendamentos. Meu email é joao@email.com"
```

**Resposta esperada:**
```
📋 Seus Agendamentos:

1. Agendamento #6
   👤 Paciente: João da Silva
   👨‍⚕️ Médico: Dr. João Silva - Cardiologia
   🏥 Estabelecimento: Clínica Saúde Total
   📅 Data: 2025-11-28
   ⏰ Horário: 08:00
   ✅ Status: scheduled

2. Agendamento #7
   👤 Paciente: Nome teste
   👨‍⚕️ Médico: Dr. João Silva - Cardiologia
   🏥 Estabelecimento: Clínica Saúde Total
   📅 Data: 2025-11-28
   ⏰ Horário: 14:30
   ✅ Status: scheduled

Deseja cancelar algum agendamento?
```

---

### ❌ Exemplo 4: Cancelar Agendamento

**Conversação:**

```
Usuário: "Quero cancelar o agendamento #6"

Bot: "Para confirmar o cancelamento, por favor me informe seu email."

Usuário: "joao@email.com"

Bot: "✅ Agendamento #6 cancelado com sucesso!

Detalhes da consulta cancelada:
📅 Data: 2025-11-28
⏰ Horário: 08:00
👨‍⚕️ Médico: Dr. João Silva - Cardiologia

Se precisar reagendar ou marcar uma nova consulta, é só me avisar!"
```

---

## 🔄 Fluxo Conversacional Completo

```
1. Usuário: "Preciso de um cardiologista"
   Bot: [Busca estabelecimentos com cardiologistas]

2. Usuário: "Quero agendar com esse médico"
   Bot: [Lista médicos disponíveis para agendamento]

3. Usuário: [Escolhe médico e fornece dados]
   Bot: [Confirma e cria agendamento]

4. Bot: [Fornece número de confirmação]
```

---

## 🛠️ Testando as Funcionalidades

### Usando o CLI (main.py)

```bash
cd "LangGraph FindDoctor"
python main.py
```

```
Você: Liste os médicos disponíveis
Bot: [Lista médicos...]

Você: Quero agendar com o médico ID 5
Bot: [Solicita informações do paciente...]

Você: João Silva, joao@email.com, (14) 98765-4321, 2025-12-15, 14:30
Bot: [Confirma agendamento...]
```

### Usando o Script de Teste

```bash
python test_appointment.py
```

Este script executa testes automatizados das funcionalidades.

---

## 📊 Estrutura de Dados

### Formato de Agendamento

```json
{
  "doctor_id": 5,
  "patient_name": "João da Silva",
  "patient_email": "joao@email.com",
  "patient_phone": "(14) 98765-4321",
  "appointment_date": "2025-12-15",
  "appointment_time": "14:30",
  "notes": "Consulta de rotina"
}
```

### Resposta de Sucesso

```json
{
  "sucesso": true,
  "agendamento_id": 8,
  "paciente": "João da Silva",
  "medico_id": 5,
  "data": "2025-12-15",
  "horario": "14:30",
  "status": "scheduled",
  "mensagem": "Consulta agendada com sucesso! Número do agendamento: 8"
}
```

---

## 🐛 Troubleshooting

### Erro: "Médico não encontrado"
**Solução:** Verifique se a API de agendamentos está rodando e se existem médicos cadastrados:
```bash
curl http://localhost:8000/api/doctors/
```

### Erro: "Este horário já está ocupado"
**Solução:** Escolha outro horário ou data. O sistema valida conflitos automaticamente.

### Erro: "Não é possível agendar para datas passadas"
**Solução:** Use uma data futura no formato YYYY-MM-DD.

### Erro: "Agendamento não encontrado"
**Solução:** Verifique se o ID do agendamento está correto e se o email corresponde ao cadastrado.

---

## 📝 Notas Importantes

1. **Email como Identificador**: O email é usado para consultar e gerenciar agendamentos
2. **Formato de Data**: Sempre use YYYY-MM-DD (ex: 2025-12-15)
3. **Formato de Horário**: Sempre use HH:MM (ex: 14:30)
4. **Número do Agendamento**: Guarde o número para referência futura
5. **Validações**: O sistema valida automaticamente conflitos e disponibilidade

---

## 🎯 Próximos Passos (Prioridade 3)

- [ ] Implementar lembretes e notificações proativas
- [ ] Integração com calendário (exportar .ics)
- [ ] Avaliações e feedback pós-consulta
- [ ] Histórico de consultas do paciente

---

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação completa no `README.md` ou abra uma issue no repositório.
