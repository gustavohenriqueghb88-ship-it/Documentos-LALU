"""
Teste manual E2E: monta payload de exemplo, choca POST /api/fill e valida .docx.
Executar com o backend já em execução (uvicorn) ou com TestClient.
"""
import json
import re
import sys
import zipfile
from pathlib import Path

# Garantir import do app
BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app.services.contract_schema import ROTA_DO_SOL_SCHEMA, FieldType  # noqa: E402
from app.config.parties import STATIC_PARTIES  # noqa: E402


def build_sample_fields() -> dict:
    out = {}
    for fid, fd in ROTA_DO_SOL_SCHEMA.items():
        t = fd.type
        # field_validator infere "número" pelo campo_id (ex.: *NUMERO*), não só pelo tipo do schema
        if "numero" in fid.lower() and fid not in ("COMPRADOR_PF_TELEFONE_NUMERO",):
            out[fid] = "42"
        elif t == FieldType.CPF:
            out[fid] = "529.982.247-25"
        elif t == FieldType.CNPJ:
            out[fid] = "12.345.678/0001-90"
        elif t == FieldType.CURRENCY:
            out[fid] = "123456.78"
        elif t == FieldType.DATE:
            out[fid] = "2026-04-15"
        elif t == FieldType.NUMBER:
            out[fid] = 10
        elif t == FieldType.EMAIL:
            out[fid] = "comprador.exemplo@email.com"
        elif t == FieldType.PHONE:
            out[fid] = "987654321"
        elif t == FieldType.SELECT:
            out[fid] = (fd.options or ["ok"])[0]
        elif t == FieldType.TEXTAREA:
            out[fid] = "Confrontações de exemplo: norte com Rua A, sul com lote 02."
        else:
            out[fid] = f"Texto_{fid[-12:]}"
    # Ajustes legíveis
    out["COMPRADOR_PF_NOME"] = "João Carlos Teste Silva"
    out["ASSINATURA_COMPRADOR_NOME"] = "João Carlos Teste Silva"
    out["PRECO_TOTAL_EXTENSO"] = "trezentos mil reais"
    out["COMISSAO_TOTAL_EXTENSO"] = "quinze mil reais"
    out["BEM_VALOR_TOTAL_EXTENSO"] = "duzentos mil reais"
    out["BEM_ENTRADA_VALOR_TOTAL_EXTENSO"] = "cinquenta mil reais"
    out["BEM_ENTRADA_PARCELAS_QTD_EXTENSO"] = "cinco"
    out["BEM_ENTRADA_PARCELA_VALOR_EXTENSO"] = "dez mil reais"
    out["PARCELAS_VALOR_TOTAL_EXTENSO"] = "cento e cinquenta mil reais"
    out["PARCELAS_QUANTIDADE_EXTENSO"] = "sessenta"
    out["PARCELAS_VALOR_UNITARIO_EXTENSO"] = "dois mil e quinhentos reais"
    out["ASSINATURA_DATA_MES"] = "abril"
    out["IMOBILIARIA_NOME"] = "Imobiliária Exemplo Ltda"
    return out


def placeholders_left(docx_path: Path) -> set[str]:
    z = zipfile.ZipFile(docx_path)
    found = set()
    for n in z.namelist():
        if not n.startswith("word/") or not n.endswith(".xml"):
            continue
        data = z.read(n).decode("utf-8", errors="ignore")
        for m in re.findall(r"\{\{([A-Z0-9_]+)\}\}", data):
            found.add(m)
    return found


def main():
    import urllib.request

    base = "http://127.0.0.1:8000"
    payload = {
        "template_id": "rota_do_sol",
        "fields": build_sample_fields(),
        "buyer_type": "PF",
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{base}/api/fill",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    print("POST /api/fill ...")
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print("ERRO na requisição:", e)
        sys.exit(1)

    print(json.dumps(data, indent=2, ensure_ascii=False))
    docs = data.get("documents") or []
    out_dir = BACKEND_ROOT / "output"
    print("\n--- Validação dos .docx em", out_dir.resolve())

    for doc in docs:
        did = doc["download_id"]
        p = out_dir / f"{did}.docx"
        print(f"\n>> {doc['name']} ({doc['id']})")
        print(f"   Arquivo: {p.resolve()}")
        print(f"   Existe: {p.exists()}")
        if not p.exists():
            continue
        left = placeholders_left(p)
        print(f"   Placeholders {{...}} restantes: {len(left)}")
        if left:
            print("   ", sorted(left))
        # VENDEDOR só no quadro resumo
        if doc["id"] == "quadro_resumo":
            xml = zipfile.ZipFile(p).read("word/document.xml").decode("utf-8", errors="ignore")
            for k, v in STATIC_PARTIES.items():
                ok = v in xml or v.replace(".", "") in xml
                print(f"   STATIC {k} presente no XML: {ok} ({v[:20]}...)")

    print("\n--- Condições gerais (só ASSINATURA_COMPRADOR_NOME)")
    cg = next((d for d in docs if d["id"] == "condicoes_gerais"), None)
    if cg:
        p = out_dir / f"{cg['download_id']}.docx"
        if p.exists():
            left = placeholders_left(p)
            print(f"   Placeholders restantes: {left}")


if __name__ == "__main__":
    main()
