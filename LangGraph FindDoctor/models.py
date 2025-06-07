from typing import List, Optional
from pydantic import BaseModel, Field

class Coordinate(BaseModel):
    """Representa coordenadas geográficas (latitude e longitude)"""
    latitude: float = Field(description="Latitude da localização")
    longitude: float = Field(description="Longitude da localização")

class Address(BaseModel):
    """Representa um endereço completo com localização geográfica"""
    street: Optional[str] = Field(None, description="Nome da rua")
    district: Optional[str] = Field(None, description="Distrito")
    city: Optional[str] = Field(None, description="Cidade")
    postcode: Optional[str] = Field(None, description="CEP")
    country: Optional[str] = Field(None, description="País")
    county: Optional[str] = Field(None, description="Condado")
    state: Optional[str] = Field(None, description="Estado")
    name: Optional[str] = Field(None, description="Nome do local")
    location: Coordinate = Field(description="Coordenadas geográficas do endereço")

class Professional(BaseModel):
    """Representa um profissional de saúde"""
    co_Profissional: str = Field(description="Código do profissional")
    nome: str = Field(description="Nome completo do profissional")
    cns: str = Field(description="Número do Cartão Nacional de Saúde")
    sus: Optional[bool] = Field(None, description="Indica se atende pelo SUS")
    especialidadeNome: Optional[int] = Field(None, description="ID da especialidade médica, obtido da consulta")

class Establishment(BaseModel):
    """Representa um estabelecimento de saúde"""
    codigoCNES: str = Field(description="Código CNES do estabelecimento")
    nome: str = Field(description="Nome do estabelecimento")
    cnpj: str = Field(description="CNPJ do estabelecimento")
    endereco: str = Field(description="Endereço completo")
    numero: str = Field(description="Número do endereço")
    bairro: str = Field(description="Bairro")
    cidade: str = Field(description="Cidade")
    uf: str = Field(description="Unidade Federativa (estado)")
    latitude: float = Field(description="Latitude da localização")
    longitude: float = Field(description="Longitude da localização")
    telefone: str = Field(description="Número de telefone")
    profissionais: List[Professional] = Field(description="Lista de profissionais que atuam no estabelecimento")

class Specialty(BaseModel):
    """Representa uma especialidade médica"""
    id: str = Field(description="ID único da especialidade")
    nome: str = Field(description="Nome da especialidade médica")

class UserQuery(BaseModel):
    """Representa uma consulta do usuário para busca de profissionais de saúde"""
    location: Optional[str] = Field(None, description="Localização ou endereço para busca")
    specialty: Optional[str] = Field(None, description="Especialidade médica desejada")
    doctor_name: Optional[str] = Field(None, description="Nome do médico a ser buscado")
    radius_km: Optional[float] = Field(5, description="Raio de busca em quilômetros")