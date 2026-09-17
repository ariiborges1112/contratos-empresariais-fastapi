from enum import Enum
from pydantic import BaseModel, Field, model_validator
from datetime import datetime, date
from typing import Optional

class SituacaoContrato(str, Enum):
    VIGENTE = "vigente"
    VENCIDO = "vencido"
    PROXIMO_VENCIMENTO = "proximo_vencimento" #serve pra representar os contratos prestes a vencer

class PeriodoContrato(BaseModel):
    inicio: date
    termino: date

    @model_validator(mode="after")
    def validar_datas(self):
        if self.inicio >= self.termino:
            raise ValueError("A data de início deve ser anterior a data de término")
        return self

class ContratoBase(BaseModel):
    descricao: Optional[str] = None
    categoria: str
    contratante: str
    contratado: str
    periodo: PeriodoContrato

class ContratoArmazenado(ContratoBase):
    id: int
    nome_original: str
    nome_armazenado: str
    extensao:
    tipo_mime: str
    categoria: str
    contratante: str
    contratado: str
    sha256: str
    tamanho: int
    data_inicio: date
    data_termino: date
    situacao: SituacaoContrato
