import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, Response, status
from app.services.export_service import gerar_relatorio_csv

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/exportar",
    tags=["Exportação"],
)

@router.get("/csv")
def exportar_csv():
    try:
        conteudo = gerar_relatorio_csv()

    except (ValueError, OSError) as erro:
        logger.error("Falha ao exportar catálogo em CSV: %s", erro)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível gerar o CSV do catálogo.",
        ) from erro

    nome_arquivo = f"catalogo_contratos_{datetime.now():%Y-%m-%d_%H%M}.csv"

    logger.info("Download do CSV solicitado: %s", nome_arquivo)

    return Response(
        content=conteudo.encode("utf-8-sig"),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{nome_arquivo}"',
        },
    )