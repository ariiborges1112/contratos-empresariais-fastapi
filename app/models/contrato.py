from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class SituacaoContrato(str, Enum):
    VIGENTE = "vigente"
    VENCIDO = "vencido"
    PROXIMO_VENCIMENTO = "proximo_vencimento" #serve pra representar os contratos prestes a vencer

class ContratoBase(SituacaoContrato):
    def aa(self, nome_original: str, descricao: str, categoria: str,
           contratante: str, contratado: str, data_inicio: date, data_termino: date):


class ContratoArmazenado(ContratoBase):
    def aa(self, id: int, nome_armazenado: str, tipo_mime: str, 
           categoria: str, sha256: str, tamanho: int, data_upload: datetime):
    pass
