import time
from datetime import datetime, timedelta
import pandas as pd
import phonenumbers

from config import EXCEL_FILE, DEFAULT_COUNTRY, MINUTES_BETWEEN_MESSAGES
from storage import read_contacts, save_contacts, mark_status
from mensagens import create_message
from whatsappCliente import send_whatsapp_number
from emailCliente import send_email
from report import append_weekly_report 

def format_numbers_to_e164(raw_number, default_region=DEFAULT_COUNTRY):
    try:
        num = phonenumbers.parse(str(raw_number), default_region)
        if not phonenumbers.is_possible_number(num) or not phonenumbers.is_valid_number(num):
            return None
        return phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)
    except:
        return None
    

def main():
    df = read_contacts(EXCEL_FILE)
    start_time = datetime.now() + timedelta(minutes=1)
    print(f"[INFO] Iniciando envio a partir de: {start_time.strftime('%Y-%m-%d %H:%M')}")

    for i, row in df.iterrows():
        raw_tel = row.get("Telefone")
        email = row.get("Email")
        
        # Telefone vazio -> tenta e-mail
        if pd.isna(raw_tel) or str(raw_tel).strip() == "":
            print(f"[AVISO] linha {i+1}: Telefone Vazio - Usando fallback por e-mail se houver...")
            if pd.notna(email) and str(email).strip() != "":
                body = create_message(row)
                ok = send_email(email, "Aviso de Vencimento de Certificado", body)
                mark_status(df, i, "Enviado (e-mail)", "Telefone Vazio")
                append_weekly_report("", email, "E-mail", "Enviado", "Telefone Vazio")
            else:
                mark_status(df, i, "Pendente", "Sem telefone e sem email válido")
                append_weekly_report("", "", "Nenhum", "Pendente", "Sem telefone e sem e-mail válido")
            continue

        phone_e164 = format_numbers_to_e164(raw_tel)
        if phone_e164 is None:
            print(f"[ERRO] linha {i+1}: número inválido -> {raw_tel} - usando fallback por e-mail se houver")
            if pd.notna(email) and str(email).strip() != "":
                body = create_message(row)
                ok = send_email(email, "Aviso de Vencimento de Certificado", body)
                mark_status(df, i, "Enviado (e-mail)", "Telefone inválido")
                append_weekly_report("", email, "E-mail", "Enviado", f"Telefone inválido: {raw_tel}")
            else:
                mark_status(df, i, "Pendente", "Sem telefone e sem email válido")
                append_weekly_report("", "", "Nenhum", "Pendente", f"Telefone inválido: {raw_tel}, sem e-mail")
            continue

        msg = create_message(row)
        send_dt = start_time + timedelta(minutes=i * MINUTES_BETWEEN_MESSAGES)
        hour = send_dt.hour
        minute = send_dt.minute

        print(f"[AGENDADO] {phone_e164} às {hour:02d}:{minute:02d} -> {msg[:40]}...")

        try:
            send_whatsapp_number(phone_e164, msg, hour, minute)
            mark_status(df, i, "Enviado (whatsapp)")
            append_weekly_report(phone_e164, email, "WhatsApp", "Enviado", "")
            time.sleep(MINUTES_BETWEEN_MESSAGES * 60)
        except Exception as e:
            print(f"[ERRO WHATS] {e} - tentando envio por e-mail se houver")
            if pd.notna(email) and str(email).strip() != "":
                ok = send_email(email, "Aviso de Vencimento de Certificado", msg)
                if ok:
                    mark_status(df, i, "Enviado (e-mail)", "Fallback após erro no WhatsApp")
                    append_weekly_report(phone_e164, email, "E-mail", "Enviado", "Fallback após erro no WhatsApp")
                else:
                    mark_status(df, i, "Pendente", "Erro no WhatsApp e no envio de e-mail")
                    append_weekly_report(phone_e164, email, "E-mail", "Falhou", "Erro no WhatsApp e e-mail")
            else:
                mark_status(df, i, "Pendente", "Erro no WhatsApp e sem e-mail")
                append_weekly_report(phone_e164, "", "WhatsApp", "Falhou", "Erro no WhatsApp e sem e-mail")
    
    save_contacts(df, EXCEL_FILE)
    print("[FIM] Processo concluído. Planilha atualizada com status.")

if __name__ == "__main__":
    main()
