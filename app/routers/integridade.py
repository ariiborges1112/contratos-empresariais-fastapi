from fastapi import APIRouter, HTTPException, status
from app.services import storage_service, hash_service
from app.models.contrato import ContratoArmazenado
from app.services.storage_service import obter_caminho_fisico
import logging

logger = logging.getLogger()

router = APIRouter(tags=["Integridade"])

def _verificar_um_documento(contrato: ContratoArmazenado) -> dict:
    caminho_arquivo = obter_caminho_fisico(contrato)
    hash_atual = hash_service.calcular_hash_arquivo(caminho_arquivo)

    integro = hash_atual is not None and hash_atual.lower() == contrato.sha256.lower()

    if not integro:
        logger.warning(f"INTEGRIDADE_FALHOU id={contrato.id}")

    return {
        "id": contrato.id,
        "nome_original": contrato.nome_original,
        "integro": integro,
        "hash_esperado": contrato.sha256,
        "hash_atual": hash_atual
    }

#F9
@router.get("/documentos/{id}/integridade")
def verificar_integridade_documento(id: int):
    contrato = storage_service.buscar_documento_via_id(id)

    if not contrato:
        logger.warning(f"DOCUMENTO_NAO_ENCONTRADO id={id}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento com ID {id} não encontrado"
        )

    return _verificar_um_documento(contrato)

#F10
@router.get("/integridade")
def verificar_integridade_global():
    contratos = storage_service.listar_documentos()

    detalhes = []
    total_integros = 0
    total_corrompidos = 0
    total_ausentes = 0

    for contrato in contratos:
        resultado = _verificar_um_documento(contrato)

        if resultado["hash_atual"] is None:
            status_arquivo = "arquivo ausente"
            total_ausentes += 1
        elif resultado["integro"]:
            status_arquivo = "integro"
            total_integros += 1
        else:
            status_arquivo = "corrompido"
            total_corrompidos += 1

        detalhes.append({**resultado, "status": status_arquivo})

    logger.info(
        f"VERIFICACAO_GLOBAL total={len(contratos)} "
        f"integros={total_integros} corrompidos={total_corrompidos} ausentes={total_ausentes}"
    )

    return {
        "total_documentos": len(contratos),
        "total_integros": total_integros,
        "total_corrompidos": total_corrompidos,
        "total_ausentes": total_ausentes,
        "detalhes": detalhes
    }