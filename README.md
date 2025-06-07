Entrar na pasta FindDoctor e rodar no terminal:

	- npm install
	- npm run dev

# Projeto: Busca de Locais de Atendimento Médico

Este projeto tem como objetivo fornecer um serviço de busca de locais de atendimento médico próximos a um endereço informado pelo usuário.

---

## 💻 Tecnologias Utilizadas

- **Front-end:** React
- **Back-end:** .NET (C#)
- **Inteligência Artificial:** Python

---

## 🗺️ Fluxo de Funcionamento

1. **Obtenção da Localização (Latitude e Longitude)**  
   - Utiliza a API do **Photon** para converter o endereço informado em coordenadas geográficas (latitude e longitude).  

2. **Busca de Pontos de Atendimento Médico**  
  - As coordenadas obtidas são utilizadas para buscar no banco de dados locais de atendimento médico previamente cadastrados.

3. **Consulta no Banco de Dados**  
   - Serão exibidas demais informações sobre o estabelecimento previamente cadastradas. Essas informações serão buscadas do **CNES**

---

## 🗃️ Fontes de Dados

- **Photon API:** Para geocodificação de endereços.  
- **CNES:** Base de dados oficial de estabelecimentos de saúde no Brasil.  

---

## 🚀 Como Rodar o Projeto

1. Clonar o repositório:  
   ```bash
   git clone https://github.com/seuusuario/projeto-medico.git
   ```
2. Configurar variáveis de ambiente (API keys e banco de dados).  
3. Iniciar o backend:  
   ```bash
   cd backend
   dotnet run
   ```
4. Iniciar o frontend:  
   ```bash
   cd frontend
   npm install
   npm start
   ```
5. Acessar a aplicação no navegador:  
   ```
   http://localhost:3000
   ```

---

Link do vídeo de explicação técnica: https://youtu.be/sysp09FanyY