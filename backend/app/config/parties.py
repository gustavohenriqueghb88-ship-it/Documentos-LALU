"""
Dados estáticos das partes fixas envolvidas nos contratos do Loteamento
Residencial Rota do Sol.

Estes valores NÃO devem ser expostos no formulário do frontend, pois são
constantes entre todos os contratos gerados. Alterá-los aqui reflete
automaticamente em todos os contratos futuros.

Uso esperado (no pipeline de preenchimento do contrato):

    from app.config.parties import STATIC_PARTIES

    user_fields_sanitized = {k: v for k, v in request.fields.items() if not k.startswith("VENDEDOR_")}
    fields = {**STATIC_PARTIES, **user_fields_sanitized}

Chaves ``VENDEDOR_*`` enviadas pelo cliente são ignoradas em ``fill.py``;
o dict final usa sempre os valores definidos em ``STATIC_PARTIES``.
"""

# -----------------------------------------------------------------------------
# VENDEDOR — LALU Administradora de Bens Ltda
# -----------------------------------------------------------------------------
# Dados bancários fixos usados no item 5.2 do Quadro Resumo (entrada).
# CNPJ e endereço da LALU já estão hardcoded no corpo textual do template,
# portanto não precisam estar aqui.
VENDEDOR_LALU = {
    "VENDEDOR_CONTA": "577590324-9",
    "VENDEDOR_AGENCIA": "0368",
    "VENDEDOR_BANCO_NOME": "Caixa Econômica Federal",
    "VENDEDOR_BANCO_CODIGO": "104",
    "VENDEDOR_PIX": "08.296.247/0001-09",
}

# -----------------------------------------------------------------------------
# Dict consolidado — usar este no fill
# -----------------------------------------------------------------------------
# Nota: os campos IMOBILIARIA_* NÃO estão aqui porque podem variar entre
# contratos (diferentes imobiliárias intermediárias). Eles continuam sendo
# preenchidos pelo formulário do usuário.
STATIC_PARTIES: dict[str, str] = {
    **VENDEDOR_LALU,
}
