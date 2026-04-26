# Twitch Watcher — Railway Edition

Corre en Railway gratis, sin Chrome, sin PC prendida.

## Archivos
- `twitch_watcher.py` — script principal
- `requirements.txt` — dependencias
- `Procfile` — instrucciones para Railway

---

## Cómo obtener tu Auth Token de Twitch

1. Abrí [twitch.tv](https://twitch.tv) e iniciá sesión
2. Abrí las DevTools del navegador (F12)
3. Ir a la pestaña **Application** (Chrome) o **Storage** (Firefox)
4. En el panel izquierdo: **Cookies → https://www.twitch.tv**
5. Buscá la cookie llamada **`auth-token`**
6. Copiá el valor (es una cadena larga de letras y números)

---

## Configuración en Railway

Variables de entorno a configurar en Railway → Settings → Variables:

| Variable | Valor |
|---|---|
| `TWITCH_CHANNEL` | nombre del canal (ej: `ibai`) |
| `TWITCH_AUTH_TOKEN` | el token que copiaste |
| `CHECK_INTERVAL` | segundos entre pings (recomendado: `60`) |

---

## Pasos para deployar

1. Creá un repo en GitHub y subí los 3 archivos
2. Entrá a [railway.app](https://railway.app) y creá cuenta con GitHub
3. **New Project → Deploy from GitHub repo**
4. Seleccioná tu repo
5. Ir a **Settings → Variables** y cargá las 3 variables
6. Railway despliega solo y el script empieza a correr

---

## Ver los logs

En Railway podés ver los logs en tiempo real desde la pestaña **Deployments → View Logs**.
Vas a ver algo así:

```
[12:00:00] 🔴 EN VIVO | Tiempo: 0h 1m | Pings OK: 1 | Fallos: 0
[12:01:00] 🔴 EN VIVO | Tiempo: 0h 2m | Pings OK: 2 | Fallos: 0
```
