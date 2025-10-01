#!/usr/bin/python3

from datetime import datetime

def get_now() -> str:
    ahora = datetime.now()
    fecha_hora = ahora.strftime("%Y-%m-%d %H:%M")
    return fecha_hora
