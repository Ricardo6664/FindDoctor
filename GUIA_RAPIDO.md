# 🚀 Guia Rápido - Iniciar FindDoctor

## 📋 Portas dos Serviços

- **API Python**: http://localhost:8000
- **FindDoctorNewFrontEnd** (Busca + Edições): http://localhost:5173
- **FrontEndAgendamento** (Consultas): http://localhost:5174
- **API C#**: http://localhost:5210 (opcional - apenas para geocoding/estabelecimentos)

## ⚡ Como Iniciar

### Terminal 1 - API Python
```powershell
cd FindDoctorPythonAPI
uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend de Busca e Edições
```powershell
cd FindDoctorNewFrontEnd
npm run dev
```
Acesse: http://localhost:5173

### Terminal 3 - Frontend de Agendamentos
```powershell
cd FrontEndAgendamento
npm run dev
```
Acesse: http://localhost:5174

## ✅ Correções Aplicadas

1. **Erro de sintaxe no ReviewEdits.tsx** - Corrigido
2. **Conflito de portas** - Resolvido:
   - FindDoctorNewFrontEnd: porta 3000 → 5173
   - FrontEndAgendamento: porta 3000 → 5174
3. **CORS da API Python** - Atualizado para aceitar as novas portas

## 🎯 Fluxo de Teste

1. **Buscar Estabelecimento** (Frontend 5173):
   - Digite "Av. Paulista, São Paulo" 
   - Clique em Buscar
   - Visualize estabelecimentos próximos

2. **Sugerir Edição** (Frontend 5173):
   - Clique em um estabelecimento
   - Clique em "Sugerir Edição"
   - Preencha o formulário
   - Envie a sugestão

3. **Revisar Sugestões** (Frontend 5173):
   - Navegue para "Revisar Edições"
   - Veja as sugestões pendentes
   - Aprove ou rejeite

4. **Agendar Consulta** (Frontend 5174):
   - Selecione um médico
   - Escolha data e horário
   - Preencha dados do paciente
   - Confirme o agendamento

5. **Ver Dashboard** (Frontend 5174):
   - Acesse "Dashboard Médico"
   - Visualize consultas
   - Atualize status das consultas

## 🐛 Troubleshooting

### Erro: "Failed to fetch"
- Verifique se a API Python está rodando em http://localhost:8000
- Teste: `curl http://localhost:8000/health`

### Erro: "Port already in use"
- Mate o processo na porta: `Get-Process -Id (Get-NetTCPConnection -LocalPort PORTA).OwningProcess | Stop-Process`
- Ou use outra porta no vite.config.ts

### Banco de dados não conecta
- Verifique se o Docker do PostgreSQL está rodando:
  ```powershell
  docker ps
  ```
- Se não estiver, inicie:
  ```powershell
  docker start <container_id>
  ```
