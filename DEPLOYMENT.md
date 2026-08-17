# 🚀 Guía de Despliegue en Render (Render.com)

Esta guía explica cómo desplegar **Palantir Deluxe** de forma gratuita en la nube usando **Render.com**.

---

## 🛠️ Archivos creados para el despliegue

1. **`Dockerfile`**: Configura un contenedor Python 3.11 con **FFmpeg preinstalado** en Linux para garantizar que la transcodificación de audio Dolby (EAC3 ➔ AAC) funcione en la nube sin cortes.
2. **`requirements.txt`**: Define las librerías necesarias (`fastapi`, `uvicorn`, `pydantic`, `requests`, `pycryptodome`).
3. **`render.yaml`**: Blueprint automático para que Render configure el servicio Web sin errores.
4. **`server.py`**: Adaptado para escuchar automáticamente en el puerto `${PORT}` que asigna Render.

---

## 📋 Pasos para desplegar en Render (3 Minutos)

### Paso 1: Subir el proyecto a GitHub
1. Crea un nuevo repositorio en tu cuenta de GitHub (ej. `palantir-deluxe`).
2. Abre la terminal en esta carpeta y ejecuta:
```bash
git init
git add .
git commit -m "Palantir Deluxe para Render"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/palantir-deluxe.git
git push -u origin main
```

### Paso 2: Crear el servicio en Render.com
1. Inicia sesión en **[https://dashboard.render.com](https://dashboard.render.com)** (puedes entrar directo con tu cuenta de GitHub).
2. Pulsa en el botón **`New +`** (arriba a la derecha) y selecciona **`Web Service`**.
3. Elige la opción **`Build and deploy from a Git repository`** y selecciona tu repositorio `palantir-deluxe`.
4. Render detectará automáticamente el archivo `Dockerfile`.
5. En la sección **Instance Type**, selecciona **`Free`** (0$/mes).
6. Pulsa en **`Create Web Service`**.

---

## 🎉 ¡Listo!
Render construirá la imagen Docker, instalará FFmpeg y desplegará tu app en un par de minutos. Te entregará una URL pública **HTTPS** permanente como:

👉 **`https://palantir-deluxe.onrender.com`**

Podrás abrirla desde cualquier móvil, tablet, televisión o PC del mundo sin necesidad de tener tu ordenador personal encendido. 🚀
