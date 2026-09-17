from enum import Enum
from pydantic import BaseModel, model_validator
from datetime import datetime, date
from typing import Optional

class SituacaoContrato(str, Enum):
    VIGENTE = "vigente"
    VENCIDO = "vencido"
    PROXIMO_VENCIMENTO = "proximo_vencimento" #serve pra representar os contratos prestes a vencer

class ContratoBase(BaseModel):
    descricao: Optional[str] = None
    categoria: str
    contratante: str
    contratado: str
    data_inicio: date
    data_termino: date

    @model_validator(mode="after")
    def validar_datas(self):
        if self.data_inicio >= self.data_termino:
            raise ValueError("A data de início deve ser anterior a data de término")
        return self

class ContratoArmazenado(ContratoBase):
    id: int
    nome_original: str
    nome_armazenado: str
    extensao: str
    tipo_mime: str
    tamanho: int
    situacao: SituacaoContrato
    data_upload: datetime
    sha256: str