import requests
from typing import List, Dict, Optional, Any

class FindDoctorApiClient:
    """Cliente para interação com a API FindDoctor para busca de profissionais de saúde"""
    
    def __init__(self, base_url: str = "http://localhost:5210", appointment_api_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.appointment_api_url = appointment_api_url.rstrip("/")
        
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
    
    # ========== MÉTODOS DE AGENDAMENTO ==========
    
    def list_doctors(self, establishment_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lista todos os médicos disponíveis para agendamento"""
        endpoint = f"{self.appointment_api_url}/api/doctors/"
        params = {}
        if establishment_id:
            params["establishment_id"] = establishment_id
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_doctor(self, doctor_id: int) -> Dict[str, Any]:
        """Obtém informações de um médico específico"""
        endpoint = f"{self.appointment_api_url}/api/doctors/{doctor_id}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def create_appointment(
        self,
        doctor_id: int,
        patient_name: str,
        patient_email: str,
        patient_phone: str,
        appointment_date: str,  # formato: "YYYY-MM-DD"
        appointment_time: str,  # formato: "HH:MM"
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Cria um novo agendamento de consulta"""
        endpoint = f"{self.appointment_api_url}/api/appointments/"
        payload = {
            "doctor_id": doctor_id,
            "patient_name": patient_name,
            "patient_email": patient_email,
            "patient_phone": patient_phone,
            "appointment_date": appointment_date,
            "appointment_time": appointment_time
        }
        if notes:
            payload["notes"] = notes
        
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    
    def list_appointments(
        self,
        doctor_id: Optional[int] = None,
        patient_email: Optional[str] = None,
        status: Optional[str] = None,
        appointment_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Lista agendamentos com filtros opcionais"""
        endpoint = f"{self.appointment_api_url}/api/appointments/"
        params = {}
        if doctor_id:
            params["doctor_id"] = doctor_id
        if patient_email:
            params["patient_email"] = patient_email
        if status:
            params["status"] = status
        if appointment_date:
            params["appointment_date"] = appointment_date
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_appointment(self, appointment_id: int) -> Dict[str, Any]:
        """Obtém detalhes de um agendamento específico"""
        endpoint = f"{self.appointment_api_url}/api/appointments/{appointment_id}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def update_appointment_status(
        self,
        appointment_id: int,
        status: str  # "scheduled", "confirmed", "completed", "cancelled"
    ) -> Dict[str, Any]:
        """Atualiza o status de um agendamento"""
        endpoint = f"{self.appointment_api_url}/api/appointments/{appointment_id}"
        payload = {"status": status}
        response = requests.patch(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    
    def cancel_appointment(self, appointment_id: int) -> None:
        """Cancela um agendamento (altera status para cancelled)"""
        return self.update_appointment_status(appointment_id, "cancelled")