import pandas as pd
from pathlib import Path
from typing import Tuple
from config import EXCEL_FILE

def read_contacts(excel_file: str = EXCEL_FILE) -> pd.DataFrame:
    df = pd.read_excel(excel_file)

    for col in ["Telefone", "Nome_Responsável", "Titular", "CPF", "CNPJ", "Tipo_Certificado", "Data_Vencimento"]:
        if col not in df.columns:
            df[col] = ""
        
        if "Status" not in df.columns:
            df["Status"] = "Pendente"
        return df
    

def save_contacts(df: pd.DataFrame, excel_file: str = EXCEL_FILE):
    df.to_excel(excel_file, index=False)


def mark_status(df: pd.DataFrame, index: int, status: str, note: str = "") -> None:
    df.at[index, "Status"] = status
    if note:
        df.at[index, "Nota"] = note
        