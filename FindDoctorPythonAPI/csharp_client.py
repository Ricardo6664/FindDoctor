import httpx
import json
from pathlib import Path
from typing import List, Optional
from config import settings
from schemas import EstablishmentFromCSharp, SpecialtyFromCSharp

class CSharpAPIClient:
    """Cliente para comunicação com a API C# do FindDoctor"""
    
    def __init__(self):
        self.base_url = settings.CSHARP_API_URL
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search_address(self, address: str) -> List[dict]:
        """Busca endereço via API C#"""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/Address/buscar",
                params={"endereco": address}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Erro ao buscar endereço: {e}")
            return []
    
    async def search_establishments(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 2.0,
        specialty_id: Optional[str] = None,
        doctor_name: Optional[str] = None
    ) -> List[dict]:
        """Busca estabelecimentos próximos via API C#"""
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "raioKm": radius_km
            }
            
            if specialty_id:
                params["especialidadeId"] = specialty_id
            if doctor_name:
                params["nomeMedico"] = doctor_name
            
            response = await self.client.get(
                f"{self.base_url}/api/Estabelecimento/proximos",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Erro ao buscar estabelecimentos: {e}")
            return []
    
    async def get_establishment_details(self, cnes_code: str) -> Optional[dict]:
        """Busca detalhes de um estabelecimento via API C#"""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/Estabelecimento/{cnes_code}"
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Erro ao buscar detalhes do estabelecimento: {e}")
            return None
    
    async def get_specialties(self) -> List[dict]:
        """Busca todas as especialidades do arquivo JSON local"""
        try:
            # Usar arquivo local ao invés do endpoint C# com problema
            json_path = Path(__file__).parent / "medical_specialties.json"
            with open(json_path, 'r', encoding='utf-8') as f:
                specialties = json.load(f)
            return specialties
        except Exception as e:
            print(f"Erro ao carregar especialidades do arquivo: {e}")
            return []
    
    async def close(self):
        """Fecha a conexão HTTP"""
        await self.client.aclose()

# Instância global do cliente
csharp_client = CSharpAPIClient()
