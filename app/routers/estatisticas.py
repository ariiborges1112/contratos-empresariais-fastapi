import logging
from collections import Counter
from datetime import date
from typing import Literal

from fastapi import APIRouter, HTTPException, Query, status

from app.config import settings
from app.models.contrato import ContratoArmazenado, SituacaoContrato
from app.services.storage_service import listar_documentos

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documentos",
    tags=["Estatísticas"],
)

MAPA_TIPO_SITUACAO = {
    "vencidos": SituacaoContrato.VENCIDO,
    "vigentes": SituacaoContrato.VIGENTE,
    "proximos": SituacaoContrato.PROXIMO_VENCIMENTO,
}


def _carregar_documentos() -> list[ContratoArmazenado]:
    """Lê o catálogo persistido (a situação já vem recalculada)."""
    try:
        return listar_documentos()

    except (ValueError, OSError) as erro:
        logger.error("Falha ao ler o catálogo: %s", erro)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível ler o catálogo de documentos.",
        ) from erro


@router.get("/estatisticas")
def estatisticas_acervo():
    documentos = _carregar_documentos()

    total = len(documentos)
    tamanho_total = sum(doc.tamanho for doc in documentos)

    por_extensao = Counter(doc.extensao.lower() for doc in documentos)
    por_categoria = Counter(doc.categoria for doc in documentos)

    por_situacao = {situacao.value: 0 for situacao in SituacaoContrato}
    for doc in documentos:
        por_situacao[doc.situacao.value] += 1

    maior = max(documentos, key=lambda doc: doc.tamanho, default=None)

    logger.info("Estatísticas do acervo geradas: %d documento(s).", total)

    return {
        "total_documentos": total,
        "tamanho_total_bytes": tamanho_total,
        "tamanho_medio_bytes": round(tamanho_total / total, 2) if total else 0,
        "maior_documento": (
            {
                "id": maior.id,
                "nome_original": maior.nome_original,
                "tamanho": maior.tamanho,
            }
            if maior
            else None
        ),
        "por_extensao": dict(por_extensao),
        "por_categoria": dict(por_categoria),
        "por_situacao": por_situacao,
    }


@router.get("/situacao")
def consultar_situacao(
    tipo: Literal["vencidos", "vigentes", "proximos"] = Query(
        description="vencidos, vigentes ou proximos",
    ),
):
    documentos = _carregar_documentos()
    alvo = MAPA_TIPO_SITUACAO[tipo]

    resultado = [
        doc.model_dump(mode="json")
        for doc in documentos
        if doc.situacao == alvo
    ]

    logger.info(
        "Consulta de situação: tipo=%s, %d resultado(s).",
        tipo,
        len(resultado),
    )

    return {
        "tipo": tipo,
        "data_referencia": date.today().isoformat(),
        "dias_alerta_vencimento": settings.contrato.dias_alerta_vencimento,
        "total": len(resultado),
        "documentos": resultado,
    }