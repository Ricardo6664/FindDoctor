from fastapi import APIRouter, Query
from typing import List, Optional
from csharp_client import csharp_client

router = APIRouter(prefix="/csharp", tags=["C# API Proxy"])

@router.get("/address/search")
async def search_address(
    address: str = Query(..., description="Endereço para buscar")
):
    """Proxy para busca de endereços na API C#"""
    results = await csharp_client.search_address(address)
    return results

@router.get("/establishments/search")
async def search_establishments(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    radius_km: float = Query(5.0, description="Raio de busca em km"),
    specialty_id: Optional[str] = Query(None, description="ID da especialidade"),
    doctor_name: Optional[str] = Query(None, description="Nome do médico")
):
    """Proxy para busca de estabelecimentos na API C#"""
    results = await csharp_client.search_establishments(
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        specialty_id=specialty_id,
        doctor_name=doctor_name
    )
    return results

@router.get("/establishments/{cnes_code}")
async def get_establishment_details(
    cnes_code: str
):
    """Proxy para detalhes de um estabelecimento na API C#"""
    result = await csharp_client.get_establishment_details(cnes_code)
    if not result:
        return {"error": "Estabelecimento não encontrado"}
    return result

@router.get("/specialties")
async def get_specialties():
    """Proxy para lista de especialidades na API C#"""
    results = await csharp_client.get_specialties()
    return results
