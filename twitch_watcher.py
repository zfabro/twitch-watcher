"""
twitch_watcher.py
-----------------
Simula la visualización de un canal de Twitch usando requests.
No necesita Chrome ni Selenium — funciona en cualquier servidor.

Configuración via variables de entorno (Railway):
    TWITCH_CHANNEL      → nombre del canal a ver
    TWITCH_AUTH_TOKEN   → tu token de autenticación de Twitch
    CHECK_INTERVAL      → segundos entre pings (default: 60)
"""

import os
import time
import requests
from datetime import datetime

CANAL = os.environ.get("TWITCH_CHANNEL", "")
AUTH_TOKEN = os.environ.get("TWITCH_AUTH_TOKEN", "")
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", "60"))

CLIENT_ID = "kimne78kx3ncx6brgo4mv6wki5h1ko"

def log(mensaje):
    ahora = datetime.now().strftime("%H:%M:%S")
    print(f"[{ahora}] {mensaje}", flush=True)

def obtener_headers():
    return {
        "Authorization": f"OAuth {AUTH_TOKEN}",
        "Client-Id": CLIENT_ID,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://www.twitch.tv",
        "Referer": f"https://www.twitch.tv/{CANAL}",
    }

def canal_en_vivo():
    url = "https://gql.twitch.tv/gql"
    query = [
        {
            "operationName": "StreamMetadata",
            "variables": {"channelLogin": CANAL.lower()},
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "a647c2a13599e5991e175155f798ca7f1ecddde73f7f341f39009c14dbf59121"
                }
            }
        }
    ]
    try:
        resp = requests.post(url, json=query, headers=obtener_headers(), timeout=10)
        data = resp.json()
        log(f"[DEBUG] Respuesta API: {data[0].get('data', {}).get('user')}")
        user = data[0].get("data", {}).get("user")
        if user is None:
            return False
        stream = user.get("stream")
        return stream is not None
    except Exception as e:
        log(f"Error al verificar estado: {e}")
        return False

def enviar_minuto_visto():
    url = "https://gql.twitch.tv/gql"
    query = [
        {
            "operationName": "VideoAdRequestHandled",
            "variables": {
                "input": {
                    "channelLogin": CANAL.lower(),
                    "playerType": "site"
                }
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "69a2e374748a10e27182f393a1e3b40e5a73b35af6d29e2b8d18da21f46b5e17"
                }
            }
        }
    ]
    try:
        resp = requests.post(url, json=query, headers=obtener_headers(), timeout=10)
        return resp.status_code == 200
    except Exception as e:
        log(f"Error al enviar ping: {e}")
        return False

def validar_config():
    errores = []
    if not CANAL:
        errores.append("Falta TWITCH_CHANNEL")
    if not AUTH_TOKEN:
        errores.append("Falta TWITCH_AUTH_TOKEN")
    return errores

def main():
    log("=" * 50)
    log("Twitch Watcher - Railway Edition")
    log("=" * 50)

    errores = validar_config()
    if errores:
        for e in errores:
            log(f"[ERROR] {e}")
        log("Configurá las variables de entorno en Railway y volvé a deployar.")
        return

    log(f"Canal: {CANAL}")
    log(f"Ping cada: {CHECK_INTERVAL}s")
    log("Iniciando...\n")

    en_vivo = canal_en_vivo()
    estado = "🔴 EN VIVO" if en_vivo else "⚫ offline"
    log(f"Estado actual: {estado}")

    horas = 0
    minutos = 0
    pings_ok = 0
    pings_fail = 0

    while True:
        time.sleep(CHECK_INTERVAL)
        minutos += CHECK_INTERVAL // 60

        if minutos >= 60:
            horas += 1
            minutos = 0

        en_vivo = canal_en_vivo()
        estado = "🔴 EN VIVO" if en_vivo else "⚫ offline"

        if en_vivo:
            ok = enviar_minuto_visto()
            if ok:
                pings_ok += 1
            else:
                pings_fail += 1

        log(f"{estado} | Tiempo: {horas}h {minutos}m | Pings OK: {pings_ok} | Fallos: {pings_fail}")

if __name__ == "__main__":
    main()
