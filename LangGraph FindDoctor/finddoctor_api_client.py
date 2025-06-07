import requests
from typing import List, Dict, Optional, Any

class FindDoctorApiClient:
    """Cliente para interação com a API FindDoctor para busca de profissionais de saúde"""
    
    def __init__(self, base_url: str = "http://localhost:5210"):
        self.base_url = base_url.rstrip("/")
        
    def search_address(self, address_text: str) -> List[Dict[str, Any]]:
        """Busca por um endereço e retorna suas coordenadas geográficas"""
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
        """Busca estabelecimentos de saúde próximos a uma localização"""
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
        """Obtém informações detalhadas sobre um estabelecimento específico"""
        endpoint = f"{self.base_url}/api/Estabelecimento/{cnes_code}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def get_all_specialties(self) -> List[Dict[str, Any]]:
        """Obtém todas as especialidades médicas disponíveis"""
        endpoint = f"{self.base_url}/api/Especialidade"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()