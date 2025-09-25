import pandas as pd

def create_message(row: pd.Series) -> str:
    if "Mensagem" in row and pd.notna(row["Mensagem"]) and str(row["Mensagem"]).strip() != "":
        return str(row["Mensagem"])
    
    nome = row.get("Nome_Responsável", "")
    titular = row.get("Titular", "")
    cpf = row.get("CPF", "")
    cnpj = row.get("CNPJ", "")
    tipo_cert = row.get("Tipo_Certificado", "")
    vencimento = row.get("Data_Vencimento", "")

    if isinstance(vencimento, pd.Timestamp):
        vencimento = vencimento.strftime("%d/%m/%Y")

    if pd.notna(cnpj) and str(cnpj).strip() != "" and pd.notna(titular) and str(titular).strip() != "":
        msg = ("*ESSA É UMA MENSAGEM AUTOMÁTICA*\n"
                "Aqui é o Nicollas da Certificação da *Unitas*\n"
                f"Vi no meu sistema que o certificado {tipo_cert} de {titular} - {cnpj}, está vencendo no dia {vencimento}. "
                "Vai ser necessário renovar esse certificado?")
        
    else:
        msg = ("*ESSA É UMA MENSAGEM AUTOMÁTICA*\n"
                "Aqui é o Nicollas da Certificação da *Unitas*\n"
                f"Vi no meu sistema que o certificado {tipo_cert} de {nome} - {cpf}, está vencendo no dia {vencimento}. "
                "Vai ser necessário renovar esse certificado?")
        
    return msg