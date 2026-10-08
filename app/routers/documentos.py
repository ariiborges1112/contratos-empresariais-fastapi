from fastapi import APIRouter,File, HTTPException, status, UploadFile, Form
from datetime import date
from fastapi.responses import FileResponse
from pydantic import ValidationError
import logging
from app.models.contrato import ContratoArmazenado, ContratoUpdate, ContratoCreate, SituacaoContrato
from app.services import storage_service

logger = logging.getLogger()

router = APIRouter(prefix="/documentos", tags=["Documentos"])

#F1
@router.post("", response_model=ContratoArmazenado, status_code=status.HTTP_201_CREATED)
async def criar_documento(
    categoria: str = Form(...),
    contratante: str = Form(...),
    contratado: str = Form(...),
    data_inicio: date = Form(...),
    data_termino: date = Form(...),
    descricao: str | None = Form(None),
    arquivo: UploadFile = File(...)
):
    try:
        conteudo = await arquivo.read()

        dados_contrato = ContratoCreate(
            descricao=descricao,
            categoria=categoria,
            contratante=contratante,
            contratado=contratado,
            data_inicio=data_inicio,
            data_termino=data_termino
        )

    
        novo_contrato = storage_service.salvar_documentos(
            dados=dados_contrato,
            nome_arquivo_original=arquivo.filename,
            conteudo_arquivo=conteudo
        )

    except ValidationError as erro:
        mensagens = []

        for problema in erro.errors():
            texto = problema["msg"]
            texto = texto.replace("Value error, ", "")
            mensagens.append(texto)

            mensagem = "; ".join(mensagens)
        
        logger.warning(f"UPLOAD_REJEITADO arquivo={arquivo.filename}")

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=mensagem
        )
    
    except ValueError as erro:
        logger.warning(f"UPLOAD_REJEITADO arquivo={arquivo.filename} motivo={erro}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro)
        )

    except OSError as erro:
        logger.error(f"UPLOAD_FALHOU arquivo={arquivo.filename} erro={erro}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível gravar o arquivo no servidor."
        )
    
    logger.info(f"UPLOAD id={novo_contrato.id} arquivo={arquivo.filename}")

    return novo_contrato


#F2, F7
@router.get("", response_model=list[ContratoArmazenado])
def listar_documentos(
    contratante: str | None = None,
    situacao: SituacaoContrato | None = None,
    categoria: str | None = None,
    extensao: str | None = None
):
    resultado = storage_service.listar_documentos(
        contratante=contratante,
        situacao=situacao,
        categoria=categoria,
        extensao=extensao
    )

    logger.info(f"CONSULTA_LISTAGEM total={len(resultado)}")

    return resultado

#F3
@router.get("/{id}", response_model=ContratoArmazenado)
def buscar_documento_por_id(id:int):
    contrato = storage_service.buscar_documento_via_id(id)

    if not contrato:
        logger.warning(f"DOCUMENTO_NAO_ENCONTRADO id={id}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento com ID {id} não encontrado"
        )
    logger.info(f"CONSULTA id={id}")
    
    return contrato

#F4
@router.get("/{id}/download")
def baixar_documento(id: int):
    resultado = storage_service.download_documentos(id)

    if not resultado:
        logger.warning(f"DOWNLOAD_FALHOU id={id} motivo=arquivo_nao_localizado")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Arquivo do documento com ID {id} não foi localizado no servidor"
        )

    caminho_arquivo, nome_original, tipo_mime = resultado

    logger.info(f"DOWNLOAD id={id} arquivo={nome_original}")

    return FileResponse(
        path=caminho_arquivo,
        filename=nome_original,
        media_type=tipo_mime
    )

#F5
@router.put("/{id}", response_model=ContratoArmazenado)
def atualizar_documento(id: int, dados: ContratoUpdate):
    contrato_atualizado = storage_service.atualizar_documento(id, dados)

    if not contrato_atualizado:
        logger.warning(f"ATUALIZACAO_FALHOU id={id} motivo=nao_encontrado")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento com ID {id} não encontrado para atualização."
        )
    logger.info(f"ATUALIZACAO id={id}")
    
    return contrato_atualizado

#F6
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_documento(id: int):
    sucesso= storage_service.excluir_documento(id)

    if not sucesso:
        logger.warning(f"EXCLUSAO_FALHOU id={id} motivo=nao_encontrado")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento com ID {id} não encontrado para exclusão."
        )
    logger.info(f"EXCLUSAO id={id}")
    
    return None