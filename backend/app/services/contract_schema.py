"""
Schema estático de campos para o contrato "RESIDENCIAL ROTA DO SOL"
Define todos os campos editáveis com seus tipos, labels e validações.

Alinhado aos placeholders do CONTRATO_ROTA_DO_SOL_TEMPLATE.docx (exceto
VENDEDOR_*, injetados em runtime via app.config.parties.STATIC_PARTIES).
"""
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel


class FieldType(str, Enum):
    """Tipos de campos suportados"""
    TEXT = "text"
    NUMBER = "number"
    CURRENCY = "currency"
    DATE = "date"
    CPF = "cpf"
    CNPJ = "cnpj"
    CEP = "cep"
    PHONE = "phone"
    EMAIL = "email"
    SELECT = "select"
    TEXTAREA = "textarea"


class FieldDefinition(BaseModel):
    """Definição de um campo do formulário"""
    field_id: str
    label: str
    type: FieldType
    required: bool = True
    section: str
    options: Optional[List[str]] = None
    placeholder: Optional[str] = None
    mask: Optional[str] = None


ROTA_DO_SOL_SCHEMA: Dict[str, FieldDefinition] = {
    # ========== COMPRADOR PESSOA FÍSICA ==========
    "COMPRADOR_PF_NOME": FieldDefinition(
        field_id="COMPRADOR_PF_NOME",
        label="Nome completo do comprador",
        type=FieldType.TEXT,
        section="COMPRADOR_PF",
        placeholder="Ex: João da Silva",
    ),
    "COMPRADOR_PF_NACIONALIDADE": FieldDefinition(
        field_id="COMPRADOR_PF_NACIONALIDADE",
        label="Nacionalidade",
        type=FieldType.TEXT,
        section="COMPRADOR_PF",
        placeholder="Ex: brasileiro",
    ),
    "COMPRADOR_PF_ESTADO_CIVIL": FieldDefinition(
        field_id="COMPRADOR_PF_ESTADO_CIVIL",
        label="Estado civil",
        type=FieldType.SELECT,
        section="COMPRADOR_PF",
        options=["solteiro(a)", "casado(a)", "divorciado(a)", "viúvo(a)", "união estável"],
    ),
    "COMPRADOR_PF_PROFISSAO": FieldDefinition(
        field_id="COMPRADOR_PF_PROFISSAO",
        label="Profissão",
        type=FieldType.TEXT,
        section="COMPRADOR_PF",
        placeholder="Ex: empresário",
    ),
    "COMPRADOR_PF_RG": FieldDefinition(
        field_id="COMPRADOR_PF_RG",
        label="RG",
        type=FieldType.TEXT,
        section="COMPRADOR_PF",
        placeholder="Ex: 12.345.678-9",
    ),
    "COMPRADOR_PF_CPF": FieldDefinition(
        field_id="COMPRADOR_PF_CPF",
        label="CPF",
        type=FieldType.CPF,
        section="COMPRADOR_PF",
        placeholder="000.000.000-00",
        mask="999.999.999-99",
    ),
    "COMPRADOR_PF_TELEFONE_DDD": FieldDefinition(
        field_id="COMPRADOR_PF_TELEFONE_DDD",
        label="DDD",
        type=FieldType.TEXT,
        section="COMPRADOR_PF",
        placeholder="41",
    ),
    "COMPRADOR_PF_TELEFONE_NUMERO": FieldDefinition(
        field_id="COMPRADOR_PF_TELEFONE_NUMERO",
        label="Telefone",
        type=FieldType.PHONE,
        section="COMPRADOR_PF",
        placeholder="99999-9999",
        mask="99999-9999",
    ),
    "COMPRADOR_PF_RUA": FieldDefinition(
        field_id="COMPRADOR_PF_RUA",
        label="Rua/Logradouro",
        type=FieldType.TEXT,
        section="COMPRADOR_PF",
        placeholder="Ex: Rua das Flores",
    ),
    "COMPRADOR_PF_CIDADE": FieldDefinition(
        field_id="COMPRADOR_PF_CIDADE",
        label="Cidade",
        type=FieldType.TEXT,
        section="COMPRADOR_PF",
        placeholder="Ex: Curitiba",
    ),
    "COMPRADOR_PF_UF": FieldDefinition(
        field_id="COMPRADOR_PF_UF",
        label="UF",
        type=FieldType.SELECT,
        section="COMPRADOR_PF",
        options=[
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
            "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
        ],
    ),
    "COMPRADOR_PF_EMAIL": FieldDefinition(
        field_id="COMPRADOR_PF_EMAIL",
        label="E-mail",
        type=FieldType.EMAIL,
        section="COMPRADOR_PF",
        placeholder="Ex: email@exemplo.com",
    ),
    # ========== DADOS DA UNIDADE ==========
    "UNIDADE_LOTE_NUMERO": FieldDefinition(
        field_id="UNIDADE_LOTE_NUMERO",
        label="Número do Lote",
        type=FieldType.TEXT,
        section="UNIDADE",
        placeholder="Ex: 15",
    ),
    "UNIDADE_QUADRA_NUMERO": FieldDefinition(
        field_id="UNIDADE_QUADRA_NUMERO",
        label="Número da Quadra",
        type=FieldType.TEXT,
        section="UNIDADE",
        placeholder="Ex: 3",
    ),
    "UNIDADE_MATRICULA": FieldDefinition(
        field_id="UNIDADE_MATRICULA",
        label="Matrícula do imóvel",
        type=FieldType.TEXT,
        section="UNIDADE",
        placeholder="Ex: 12.345",
    ),
    "UNIDADE_CONFRONTACOES": FieldDefinition(
        field_id="UNIDADE_CONFRONTACOES",
        label="Confrontações (conforme matrícula)",
        type=FieldType.TEXTAREA,
        section="UNIDADE",
        placeholder="Descrever conforme matrícula do imóvel",
    ),
    "UNIDADE_INSCRICAO_IMOBILIARIA": FieldDefinition(
        field_id="UNIDADE_INSCRICAO_IMOBILIARIA",
        label="Inscrição imobiliária municipal",
        type=FieldType.TEXT,
        section="UNIDADE",
        placeholder="Ex: inscrição municipal",
    ),
    # ========== PREÇO TOTAL ==========
    "PRECO_TOTAL_VALOR": FieldDefinition(
        field_id="PRECO_TOTAL_VALOR",
        label="Valor total (R$)",
        type=FieldType.CURRENCY,
        section="PRECO",
    ),
    "PRECO_TOTAL_EXTENSO": FieldDefinition(
        field_id="PRECO_TOTAL_EXTENSO",
        label="Valor por extenso",
        type=FieldType.TEXT,
        section="PRECO",
        placeholder="Ex: duzentos mil reais",
    ),
    # ========== COMISSÃO DE CORRETAGEM ==========
    "COMISSAO_TOTAL_VALOR": FieldDefinition(
        field_id="COMISSAO_TOTAL_VALOR",
        label="Valor total da comissão (R$)",
        type=FieldType.CURRENCY,
        section="COMISSAO",
    ),
    "COMISSAO_TOTAL_EXTENSO": FieldDefinition(
        field_id="COMISSAO_TOTAL_EXTENSO",
        label="Valor por extenso",
        type=FieldType.TEXT,
        section="COMISSAO",
        placeholder="Ex: dez mil reais",
    ),
    # ========== DADOS DA IMOBILIÁRIA ==========
    "IMOBILIARIA_NOME": FieldDefinition(
        field_id="IMOBILIARIA_NOME",
        label="Nome da Imobiliária",
        type=FieldType.TEXT,
        section="IMOBILIARIA",
        placeholder="Ex: Imobiliária XYZ",
    ),
    "IMOBILIARIA_CNPJ": FieldDefinition(
        field_id="IMOBILIARIA_CNPJ",
        label="CNPJ",
        type=FieldType.CNPJ,
        section="IMOBILIARIA",
        placeholder="00.000.000/0000-00",
        mask="99.999.999/9999-99",
    ),
    "IMOBILIARIA_CRECI": FieldDefinition(
        field_id="IMOBILIARIA_CRECI",
        label="CRECI",
        type=FieldType.TEXT,
        section="IMOBILIARIA",
        placeholder="Ex: CRECI 12345",
    ),
    "IMOBILIARIA_BANCO_NOME": FieldDefinition(
        field_id="IMOBILIARIA_BANCO_NOME",
        label="Nome do Banco",
        type=FieldType.TEXT,
        section="IMOBILIARIA",
        placeholder="Ex: Banco do Brasil",
    ),
    "IMOBILIARIA_BANCO_CODIGO": FieldDefinition(
        field_id="IMOBILIARIA_BANCO_CODIGO",
        label="Código do Banco",
        type=FieldType.TEXT,
        section="IMOBILIARIA",
        placeholder="Ex: 001",
    ),
    "IMOBILIARIA_AGENCIA": FieldDefinition(
        field_id="IMOBILIARIA_AGENCIA",
        label="Agência",
        type=FieldType.TEXT,
        section="IMOBILIARIA",
        placeholder="Ex: 1234-5",
    ),
    "IMOBILIARIA_CONTA": FieldDefinition(
        field_id="IMOBILIARIA_CONTA",
        label="Conta",
        type=FieldType.TEXT,
        section="IMOBILIARIA",
        placeholder="Ex: 12345-6",
    ),
    "IMOBILIARIA_PIX": FieldDefinition(
        field_id="IMOBILIARIA_PIX",
        label="Chave PIX",
        type=FieldType.TEXT,
        section="IMOBILIARIA",
        placeholder="Ex: email@exemplo.com ou CNPJ",
    ),
    # ========== PREÇO DO BEM / ENTRADA (VENDEDOR_* via STATIC_PARTIES) ==========
    "BEM_VALOR_TOTAL": FieldDefinition(
        field_id="BEM_VALOR_TOTAL",
        label="Valor total do bem (R$)",
        type=FieldType.CURRENCY,
        section="BEM",
    ),
    "BEM_VALOR_TOTAL_EXTENSO": FieldDefinition(
        field_id="BEM_VALOR_TOTAL_EXTENSO",
        label="Valor por extenso",
        type=FieldType.TEXT,
        section="BEM",
        placeholder="Ex: duzentos mil reais",
    ),
    "BEM_ENTRADA_VALOR_TOTAL": FieldDefinition(
        field_id="BEM_ENTRADA_VALOR_TOTAL",
        label="Valor total da entrada (R$)",
        type=FieldType.CURRENCY,
        section="BEM",
    ),
    "BEM_ENTRADA_VALOR_TOTAL_EXTENSO": FieldDefinition(
        field_id="BEM_ENTRADA_VALOR_TOTAL_EXTENSO",
        label="Valor total da entrada por extenso",
        type=FieldType.TEXT,
        section="BEM",
        placeholder="Ex: quarenta mil reais",
    ),
    "BEM_ENTRADA_PARCELAS_QTD": FieldDefinition(
        field_id="BEM_ENTRADA_PARCELAS_QTD",
        label="Quantidade de parcelas da entrada",
        type=FieldType.NUMBER,
        section="BEM",
        placeholder="Ex: 5",
    ),
    "BEM_ENTRADA_PARCELAS_QTD_EXTENSO": FieldDefinition(
        field_id="BEM_ENTRADA_PARCELAS_QTD_EXTENSO",
        label="Quantidade de parcelas por extenso",
        type=FieldType.TEXT,
        section="BEM",
        placeholder="Ex: cinco",
    ),
    "BEM_ENTRADA_PARCELA_VALOR": FieldDefinition(
        field_id="BEM_ENTRADA_PARCELA_VALOR",
        label="Valor de cada parcela da entrada (R$)",
        type=FieldType.CURRENCY,
        section="BEM",
    ),
    "BEM_ENTRADA_PARCELA_VALOR_EXTENSO": FieldDefinition(
        field_id="BEM_ENTRADA_PARCELA_VALOR_EXTENSO",
        label="Valor de cada parcela por extenso",
        type=FieldType.TEXT,
        section="BEM",
        placeholder="Ex: oito mil reais",
    ),
    # ========== PARCELAS ==========
    "PARCELAS_VALOR_TOTAL": FieldDefinition(
        field_id="PARCELAS_VALOR_TOTAL",
        label="Valor total das parcelas (R$)",
        type=FieldType.CURRENCY,
        section="PARCELAS",
    ),
    "PARCELAS_VALOR_TOTAL_EXTENSO": FieldDefinition(
        field_id="PARCELAS_VALOR_TOTAL_EXTENSO",
        label="Valor por extenso",
        type=FieldType.TEXT,
        section="PARCELAS",
        placeholder="Ex: cento e sessenta mil reais",
    ),
    "PARCELAS_QUANTIDADE": FieldDefinition(
        field_id="PARCELAS_QUANTIDADE",
        label="Quantidade de parcelas",
        type=FieldType.NUMBER,
        section="PARCELAS",
        placeholder="Ex: 60",
    ),
    "PARCELAS_QUANTIDADE_EXTENSO": FieldDefinition(
        field_id="PARCELAS_QUANTIDADE_EXTENSO",
        label="Quantidade por extenso",
        type=FieldType.TEXT,
        section="PARCELAS",
        placeholder="Ex: sessenta",
    ),
    "PARCELAS_VALOR_UNITARIO": FieldDefinition(
        field_id="PARCELAS_VALOR_UNITARIO",
        label="Valor de cada parcela (R$)",
        type=FieldType.CURRENCY,
        section="PARCELAS",
    ),
    "PARCELAS_VALOR_UNITARIO_EXTENSO": FieldDefinition(
        field_id="PARCELAS_VALOR_UNITARIO_EXTENSO",
        label="Valor por extenso",
        type=FieldType.TEXT,
        section="PARCELAS",
        placeholder="Ex: dois mil e seiscentos reais",
    ),
    "PARCELAS_DIA_VENCIMENTO": FieldDefinition(
        field_id="PARCELAS_DIA_VENCIMENTO",
        label="Dia de vencimento",
        type=FieldType.NUMBER,
        section="PARCELAS",
        placeholder="Ex: 10",
    ),
    "PARCELAS_DATA_PRIMEIRA": FieldDefinition(
        field_id="PARCELAS_DATA_PRIMEIRA",
        label="Data da primeira parcela",
        type=FieldType.DATE,
        section="PARCELAS",
        placeholder="DD/MM/AAAA",
    ),
    # ========== ASSINATURA ==========
    "ASSINATURA_DATA_DIA": FieldDefinition(
        field_id="ASSINATURA_DATA_DIA",
        label="Dia",
        type=FieldType.NUMBER,
        section="ASSINATURA",
        placeholder="Ex: 15",
    ),
    "ASSINATURA_DATA_MES": FieldDefinition(
        field_id="ASSINATURA_DATA_MES",
        label="Mês",
        type=FieldType.TEXT,
        section="ASSINATURA",
        placeholder="Ex: janeiro",
    ),
    "ASSINATURA_DATA_ANO": FieldDefinition(
        field_id="ASSINATURA_DATA_ANO",
        label="Ano",
        type=FieldType.NUMBER,
        section="ASSINATURA",
        placeholder="Ex: 2025",
    ),
    "ASSINATURA_COMPRADOR_NOME": FieldDefinition(
        field_id="ASSINATURA_COMPRADOR_NOME",
        label="Nome do comprador (assinatura)",
        type=FieldType.TEXT,
        section="ASSINATURA",
        placeholder="Ex: João da Silva",
    ),
    # ========== TESTEMUNHAS ==========
    "TESTEMUNHA_1_NOME": FieldDefinition(
        field_id="TESTEMUNHA_1_NOME",
        label="Nome da Testemunha 1",
        type=FieldType.TEXT,
        section="TESTEMUNHAS",
        placeholder="Ex: Maria Santos",
    ),
    "TESTEMUNHA_1_CPF": FieldDefinition(
        field_id="TESTEMUNHA_1_CPF",
        label="CPF da Testemunha 1",
        type=FieldType.CPF,
        section="TESTEMUNHAS",
        placeholder="000.000.000-00",
        mask="999.999.999-99",
    ),
    "TESTEMUNHA_2_NOME": FieldDefinition(
        field_id="TESTEMUNHA_2_NOME",
        label="Nome da Testemunha 2",
        type=FieldType.TEXT,
        section="TESTEMUNHAS",
        placeholder="Ex: Pedro Oliveira",
    ),
    "TESTEMUNHA_2_CPF": FieldDefinition(
        field_id="TESTEMUNHA_2_CPF",
        label="CPF da Testemunha 2",
        type=FieldType.CPF,
        section="TESTEMUNHAS",
        placeholder="000.000.000-00",
        mask="999.999.999-99",
    ),
}


SECTION_ORDER = [
    ("COMPRADOR_PF", "Dados do Comprador (Pessoa Física)"),
    ("UNIDADE", "Dados da Unidade"),
    ("PRECO", "Preço Total"),
    ("COMISSAO", "Comissão de Corretagem"),
    ("IMOBILIARIA", "Dados da Imobiliária"),
    ("BEM", "Preço do Bem e Entrada"),
    ("PARCELAS", "Parcelamento"),
    ("ASSINATURA", "Data e Local"),
    ("TESTEMUNHAS", "Testemunhas"),
]


def get_fields_by_section(section: str) -> List[FieldDefinition]:
    """Retorna todos os campos de uma seção específica"""
    return [f for f in ROTA_DO_SOL_SCHEMA.values() if f.section == section]


def get_all_field_ids() -> List[str]:
    """Retorna lista de todos os IDs de campos do formulário (exclui VENDEDOR_* estáticos)."""
    return list(ROTA_DO_SOL_SCHEMA.keys())
