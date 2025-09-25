import pywhatkit as kit
from config import WAIT_TIME, CLOSE_TIME

def send_whatsapp_number(phone_e164: str, message: str, hour: int, minute: int) -> None:
    kit.sendwhatmsg(phone_e164, message, hour, minute, wait_time=WAIT_TIME, tab_close=True, close_time=CLOSE_TIME)