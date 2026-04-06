"""
Rota para download de documentos preenchidos
"""
import os
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pathlib import Path
from app.services.document_storage import DocumentStorage

router = APIRouter()
storage = DocumentStorage()


@router.get("/download/{document_id}")
async def download_document(
    document_id: str,
    fmt: str = Query("pdf", alias="format", description="pdf ou docx"),
):
    """
    Download do contrato preenchido em PDF (padrão) ou Word (.docx).
    Ex.: /api/download/UUID_quadro_resumo?format=docx
    """
    try:
        fmt = (fmt or "pdf").lower().strip()
        if fmt not in ("pdf", "docx"):
            raise HTTPException(
                status_code=400,
                detail="Parâmetro 'format' deve ser 'pdf' ou 'docx'",
            )

        ext = ".pdf" if fmt == "pdf" else ".docx"
        media_type = "application/pdf" if fmt == "pdf" else (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        file_path = storage.get_filled_file_path(document_id, file_format=fmt)
        
        print(f"[DOWNLOAD] document_id recebido: {document_id}", flush=True)
        print(f"[DOWNLOAD] format: {fmt}, caminho: {file_path}", flush=True)
        print(f"[DOWNLOAD] Arquivo existe: {os.path.exists(file_path)}", flush=True)
        
        if not Path(file_path).exists():
            output_dir = storage.output_dir
            if output_dir.exists():
                matching_files = list(output_dir.glob(f"{document_id}*{ext}"))
                if matching_files:
                    file_path = str(matching_files[0])
                    print(f"[DOWNLOAD] Arquivo encontrado por padrão: {file_path}", flush=True)
                else:
                    available = list(output_dir.glob(f"*{ext}"))
                    print(f"[DOWNLOAD] Arquivos {ext} no output: {[f.name for f in available]}", flush=True)
                    raise HTTPException(
                        status_code=404,
                        detail=(
                            f"Documento não encontrado. Procurado: {file_path}. "
                            f"Arquivos disponíveis: {[f.name for f in available]}"
                        ),
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Diretório de output não existe: {output_dir}"
                )
        
        label = "contrato"
        if "condicoes_gerais" in document_id:
            label = "condicoes_gerais"
        filename = f"{label}_{document_id[:8]}{ext}"
        
        return FileResponse(
            path=file_path,
            media_type=media_type,
            filename=filename,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar download: {str(e)}"
        )
