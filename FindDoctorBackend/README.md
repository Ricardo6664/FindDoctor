# FindDoctor API - LangGraph Agent Integration Guide

This document provides comprehensive instructions for creating a LangGraph agent that interacts with the FindDoctor API service, which helps users locate healthcare providers and establishments based on their location, specialties, and other criteria.

## Table of Contents
- [Project Overview](#project-overview)
- [API Endpoints](#api-endpoints)
- [Setting Up Your LangGraph Agent](#setting-up-your-langgraph-agent)
- [Agent Implementation](#agent-implementation)
- [Example Use Cases](#example-use-cases)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Project Overview

FindDoctor is a healthcare provider search platform that allows users to find medical establishments and professionals based on:
- Geographical proximity
- Medical specialties
- Doctor names
- Insurance coverage

The backend consists of a .NET 8 API with several endpoints for searching healthcare establishments, filtering by specialties, and geocoding addresses.

## API Endpoints

### 1. Address Search API

**Endpoint:** `GET /api/Address/buscar`

**Parameters:**
- `endereco`: The address text to search for (required)

**Response:** List of address matches with geographic coordinates

**Example Request:**
```
GET /api/Address/buscar?endereco=Avenida Paulista, São Paulo
```

**Example Response:**
```json
[
  {
    "street": "Avenida Paulista",
    "district": "Bela Vista",
    "city": "São Paulo",
    "postcode": "01310-100",
    "country": "Brazil",
    "county": "São Paulo",
    "state": "SP",
    "name": "Avenida Paulista",
    "location": {
      "latitude": -23.5632,
      "longitude": -46.6541
    }
  },
  // Additional address matches...
]
```

### 2. Healthcare Establishments Search API

**Endpoint:** `GET /api/Estabelecimento/proximos`

**Parameters:**
- `latitude`: Geographic latitude coordinate (required)
- `longitude`: Geographic longitude coordinate (required)
- `raioKm`: Search radius in kilometers (optional, default = 5)
- `especialidadeId`: ID of a medical specialty (optional)
- `nomeMedico`: Doctor name to filter by (optional)
- `convenioId`: Insurance provider ID (optional)

**Response:** List of healthcare establishments with their details and affiliated professionals

**Example Request:**
```
GET /api/Estabelecimento/proximos?latitude=-23.5632&longitude=-46.6541&raioKm=3&especialidadeId=225125&nomeMedico=Silva
```

**Example Response:**
```json
[
  {
    "codigoCNES": "1234567",
    "nome": "Hospital Santa Cruz",
    "cnpj": "12345678901234",
    "endereco": "Avenida Rebouças",
    "numero": "123",
    "bairro": "Pinheiros",
    "cidade": "São Paulo",
    "uf": "SP",
    "latitude": -23.5658,
    "longitude": -46.6607,
    "telefone": "(11) 2222-3333",
    "profissionais": [
      {
        "co_Profissional": "123456",
        "nome": "Dr. João Silva",
        "cns": "123456789012345",
        "sus": true,
        "especialidadeNome": "Cardiologia"
      },
      // Additional professionals...
    ]
  },
  // Additional establishments...
]
```

### 3. Establishment Details API

**Endpoint:** `GET /api/Estabelecimento/{codigoCNES}`

**Parameters:**
- `codigoCNES`: CNES code of the healthcare establishment (required, in URL path)

**Response:** Detailed information about a specific healthcare establishment

**Example Request:**
```
GET /api/Estabelecimento/1234567
```

**Example Response:**
```json
{
  "codigoCNES": "1234567",
  "nome": "Hospital Santa Cruz",
  "cnpj": "12345678901234",
  "endereco": "Avenida Rebouças",
  "numero": "123",
  "bairro": "Pinheiros",
  "cidade": "São Paulo",
  "uf": "SP",
  "latitude": -23.5658,
  "longitude": -46.6607,
  "telefone": "(11) 2222-3333",
  "profissionais": [
    {
      "co_Profissional": "123456",
      "nome": "Dr. João Silva",
      "cns": "123456789012345",
      "sus": true
    },
    // Additional professionals...
  ]
}
```

### 4. Medical Specialties API

**Endpoint:** `GET /api/Especialidade`

**Parameters:** None

**Response:** List of all available medical specialties

**Example Request:**
```
GET /api/Especialidade
```

**Example Response:**
```json
[
  {
    "id": "225125",
    "nome": "Cardiologia"
  },
  {
    "id": "225142",
    "nome": "Neurologia"
  },
  // Additional specialties...
]
```

## Setting Up Your LangGraph Agent

### Prerequisites

1. Python 3.9+ installed
2. Required packages:
   - langchain
   - langgraph
   - requests
   - pydantic

### Installation

```bash
pip install langchain langgraph requests pydantic
```

## Agent Implementation

Below is a step-by-step guide to implement a LangGraph agent that can interact with the FindDoctor API.

### 1. Define API Client

Create a client class to interact with the FindDoctor API:

```python
# finddoctor_api_client.py
import requests
from typing import List, Dict, Optional, Any

class FindDoctorApiClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip("/")
        
    def search_address(self, address_text: str) -> List[Dict[str, Any]]:
        """Search for an address and get its coordinates"""
        endpoint = f"{self.base_url}/api/Address/buscar"
        params = {"endereco": address_text}
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def search_establishments(
        self, 
        latitude: float, 
        longitude: float, 
        radius_km: float = 5, 
        specialty_id: Optional[str] = None,
        doctor_name: Optional[str] = None,
        insurance_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Search for healthcare establishments near a location"""
        endpoint = f"{self.base_url}/api/Estabelecimento/proximos"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "raioKm": radius_km
        }
        
        if specialty_id:
            params["especialidadeId"] = specialty_id
        if doctor_name:
            params["nomeMedico"] = doctor_name
        if insurance_id:
            params["convenioId"] = insurance_id
            
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_establishment_details(self, cnes_code: str) -> Dict[str, Any]:
        """Get detailed information about a specific establishment"""
        endpoint = f"{self.base_url}/api/Estabelecimento/{cnes_code}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def get_all_specialties(self) -> List[Dict[str, Any]]:
        """Get all available medical specialties"""
        endpoint = f"{self.base_url}/api/Especialidade"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
```

### 2. Create Pydantic Models

Define data models to validate API responses and agent inputs/outputs:

```python
# models.py
from typing import List, Optional
from pydantic import BaseModel

class Coordinate(BaseModel):
    latitude: float
    longitude: float

class Address(BaseModel):
    street: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    postcode: Optional[str] = None
    country: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    name: Optional[str] = None
    location: Coordinate

class Professional(BaseModel):
    co_Profissional: str
    nome: str
    cns: str
    sus: Optional[bool] = None
    especialidadeNome: Optional[str] = None

class Establishment(BaseModel):
    codigoCNES: str
    nome: str
    cnpj: str
    endereco: str
    numero: str
    bairro: str
    cidade: str
    uf: str
    latitude: float
    longitude: float
    telefone: str
    profissionais: List[Professional]

class Specialty(BaseModel):
    id: str
    nome: str

class UserQuery(BaseModel):
    location: Optional[str] = None
    specialty: Optional[str] = None
    doctor_name: Optional[str] = None
    radius_km: Optional[float] = 5
```

### 3. Implement LangGraph Agent

Create a LangGraph agent that can process user requests and interact with the FindDoctor API:

```python
# finddoctor_agent.py
from typing import List, Dict, Any, Optional, Annotated, TypedDict
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
import json

from finddoctor_api_client import FindDoctorApiClient
from models import Address, Establishment, Specialty

# Initialize the API client
client = FindDoctorApiClient("http://localhost:5000")  # Replace with your API URL

# Define agent state
class AgentState(TypedDict):
    messages: List[Any]
    current_location: Optional[Dict]
    specialty_id: Optional[str]
    doctor_name: Optional[str]
    establishments: Optional[List[Dict]]

# Define tools
@tool
def search_address(query: str) -> str:
    """Search for an address and return geolocation information."""
    try:
        results = client.search_address(query)
        if not results:
            return "No addresses found for this query."
        return json.dumps(results[:3], ensure_ascii=False)
    except Exception as e:
        return f"Error searching for address: {str(e)}"

@tool
def get_specialties() -> str:
    """Get the list of all medical specialties."""
    try:
        specialties = client.get_all_specialties()
        return json.dumps(specialties, ensure_ascii=False)
    except Exception as e:
        return f"Error fetching specialties: {str(e)}"

@tool
def search_establishments(
    latitude: float,
    longitude: float,
    radius_km: float = 5,
    specialty_id: Optional[str] = None,
    doctor_name: Optional[str] = None
) -> str:
    """
    Search for healthcare establishments near the specified coordinates.
    
    Args:
        latitude: The latitude coordinate
        longitude: The longitude coordinate
        radius_km: Search radius in kilometers
        specialty_id: Optional ID of a medical specialty
        doctor_name: Optional doctor name to filter results
    """
    try:
        results = client.search_establishments(
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            specialty_id=specialty_id,
            doctor_name=doctor_name
        )
        if not results:
            return "No establishments found matching your criteria."
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        return f"Error searching establishments: {str(e)}"

@tool
def get_establishment_details(cnes_code: str) -> str:
    """Get detailed information about a specific healthcare establishment."""
    try:
        details = client.get_establishment_details(cnes_code)
        return json.dumps(details, ensure_ascii=False)
    except Exception as e:
        return f"Error fetching establishment details: {str(e)}"

# Create graph nodes
def process_user_input(state: AgentState) -> AgentState:
    """Process the user's query and update the agent's state."""
    messages = state["messages"]
    last_message = messages[-1].content if messages else ""
    
    # Here you can parse the user input to extract location, specialty, etc.
    # For now, we'll just pass the message to the LLM node
    
    return state

def llm_node(state: AgentState) -> AgentState:
    """LLM processing node."""
    messages = state["messages"]
    
    # Create a list of available tools
    tools = [search_address, get_specialties, search_establishments, get_establishment_details]
    
    # Initialize the language model
    llm = ChatOpenAI(temperature=0, model="gpt-4-turbo")
    
    # Create system message
    system_message = SystemMessage(
        content="""You are a helpful assistant designed to help users find healthcare providers and establishments in Brazil.
        
You can help users search for doctors and medical facilities based on:
1. Location/address
2. Medical specialty
3. Doctor's name
4. Distance (radius in km)

Follow these steps to help the user:
1. First, determine what the user is looking for - address search or healthcare provider search
2. If needed, ask for any missing information like location or specialty
3. Use the appropriate tool to search for information
4. Present results in a clear, structured format
5. Offer to refine the search or get more details if needed

Remember that all addresses and healthcare data are in Brazil."""
    )
    
    # Run the LLM with tools
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=llm,
        tools=tools,
        return_intermediate_steps=True,
        verbose=True,
        handle_parsing_errors=True
    )
    
    # Execute the agent
    response = agent_executor.invoke({
        "chat_history": messages[:-1],
        "input": messages[-1].content
    })
    
    # Update messages with AI response
    updated_messages = messages.copy()
    updated_messages.append(AIMessage(content=response["output"]))
    
    # Update state
    return {"messages": updated_messages,
            "current_location": state.get("current_location"),
            "specialty_id": state.get("specialty_id"),
            "doctor_name": state.get("doctor_name"),
            "establishments": state.get("establishments")}

# Create the graph
def create_agent_graph() -> StateGraph:
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("process_input", process_user_input)
    workflow.add_node("llm", llm_node)
    
    # Add edges
    workflow.add_edge("process_input", "llm")
    workflow.add_edge("llm", END)
    
    # Set entry point
    workflow.set_entry_point("process_input")
    
    return workflow

# Initialize the agent
agent_graph = create_agent_graph()
agent = agent_graph.compile()

def ask_agent(user_input: str, chat_history: List[Dict] = None) -> Dict[str, Any]:
    """Function to interact with the agent."""
    if chat_history is None:
        chat_history = []
        
    # Format messages
    messages = chat_history.copy()
    messages.append(HumanMessage(content=user_input))
    
    # Run the agent
    result = agent.invoke({"messages": messages})
    
    return {
        "response": result["messages"][-1].content,
        "chat_history": result["messages"]
    }
```

### 4. Create a Simple Interface

Implement a basic interface to interact with your agent:

```python
# main.py
from finddoctor_agent import ask_agent

def main():
    chat_history = []
    
    print("FindDoctor Agent")
    print("Type 'exit' to quit")
    print("-" * 50)
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            break
        
        # Process with agent
        result = ask_agent(user_input, chat_history)
        chat_history = result["chat_history"]
        
        print("\nAssistant:", result["response"])
        print("-" * 50)

if __name__ == "__main__":
    main()
```

## Example Use Cases

Here are some examples of how users might interact with your LangGraph agent:

### Use Case 1: Finding Nearby Cardiologists

**User Query:** "I need to find a cardiologist near Avenida Paulista in São Paulo"

The agent would:
1. Use the `search_address` tool to geocode "Avenida Paulista, São Paulo"
2. Get the list of specialties to find the specialty ID for "Cardiologia"
3. Use the `search_establishments` tool with the coordinates and specialty ID
4. Present a list of healthcare establishments with cardiologists

### Use Case 2: Getting Details About a Specific Hospital

**User Query:** "Tell me more about Hospital Santa Cruz with code 1234567"

The agent would:
1. Use the `get_establishment_details` tool with the CNES code
2. Format and present the detailed information about the hospital

### Use Case 3: Finding a Specific Doctor

**User Query:** "I'm looking for Dr. Silva near Bela Vista neighborhood"

The agent would:
1. Use the `search_address` tool to geocode "Bela Vista, São Paulo"
2. Use the `search_establishments` tool with the coordinates and doctor name "Silva"
3. Present a list of establishments where Dr. Silva works

## Error Handling

Your LangGraph agent should handle these common errors:

1. **Address Not Found**: If the geocoding service can't find the address, suggest alternatives or ask for more details.

2. **No Results Found**: When no establishments match the criteria, suggest broadening the search (e.g., increasing radius).

3. **API Connection Issues**: Handle network errors gracefully with clear error messages.

4. **Ambiguous Requests**: When user requests are unclear, the agent should ask clarifying questions.

## Best Practices

1. **Cache Common Data**: Consider caching the specialties list to avoid repeated API calls.

2. **Maintain Context**: Keep track of the user's location and previous searches to improve subsequent interactions.

3. **Suggest Refinements**: When results are too numerous, suggest ways to narrow the search.

4. **Format Results**: Present healthcare establishments in a clear, structured format with key information highlighted.

5. **Validate User Input**: Before making API calls, validate user inputs for correctness and completeness.

6. **Respect Privacy**: Be careful with handling and storing any personal information.

7. **Provide References**: When giving information about healthcare providers, include their CNES code for reference.

---

This README provides detailed instructions for implementing a LangGraph agent that can interact with the FindDoctor API. Customize the implementation based on your specific requirements and the LLM provider you're using.