import os
import pandas as pd
from datetime import datetime

REPORT_FOLDER = "reports"
REPORT_FILE = os.path.join(REPORT_FOLDER, "weekly_report.xlsx")
COLUMNS = ["Data/Hora_Envio", "Telefone", "Email", "Tipo_Envio", "Status", "Observação"]

def ensure_report_file():
    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)
    if not os.path.exists(REPORT_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_excel(REPORT_FILE, index=False)

def append_weekly_report(telefone="", email="", tipo_envio="", status="", observacao=""):
    ensure_report_file()
    df = pd.read_excel(REPORT_FILE)

    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    new = {
        "Data/Hora_Envio": now,
        "Telefone": telefone,
        "Email": email,
        "Tipo_Envio": tipo_envio,
        "Status": status,
        "Observação": observacao
    }

    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    df.to_excel(REPORT_FILE, index=False)
    