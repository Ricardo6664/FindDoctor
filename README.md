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
   - Utiliza a API do **Nominatim** para converter o endereço informado em coordenadas geográficas (latitude e longitude).  

2. **Busca de Pontos de Atendimento Médico**  
   - Com as coordenadas obtidas, a aplicação consulta:  
     - A API **Google Places** para obter locais cadastrados.  
     - O serviço **Overpass API** como alternativa gratuita para busca de estabelecimentos médicos.  

3. **Consulta no Banco de Dados**  
   - As coordenadas obtidas são utilizadas para buscar no banco de dados locais de atendimento médico previamente cadastrados.  
   - Os dados são inicialmente coletados e atualizados com base no **Cadastro Nacional de Estabelecimentos de Saúde (CNES)**.  

---

## 🗃️ Fontes de Dados

- **Nominatim:** Para geocodificação de endereços.  
- **Google Places API:** Para obtenção de pontos de interesse médico.  
- **Overpass API:** Alternativa gratuita para consultas espaciais.  
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

## 📝 Licença
Este projeto está licenciado sob a licença MIT.
