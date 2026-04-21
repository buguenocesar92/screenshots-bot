# Screenshots Bot

Bot que recorre un sitio web completo y genera capturas en 3 viewports.
Produce un PDF de reporte listo para presentar al cliente.

Usado en KraftDo para mostrar redesigns de WordPress antes del deploy a produccion.

## Como funciona

    URL del sitio (via Cloudflare Tunnel)
            |
    Playwright escanea todos los links internos
            |
    Captura en mobile (375px) + tablet (768px) + desktop (1440px)
            |
    pdf.py compila todas las capturas en un PDF
            |
    Reporte_Proyecto.pdf listo para enviar al cliente

## Instalacion

    git clone https://github.com/buguenocesar92/screenshots-bot.git
    cd screenshots-bot
    npm install
    npx playwright install chromium
    pip install Pillow --break-system-packages

## Configuracion

    cp .env.example .env
    # Editar BASE_URL con la URL del sitio o tunel Cloudflare

## Uso

    node index.js      # genera capturas en /screenshots/
    python3 pdf.py     # compila PDF del reporte

## Caso de uso real

Usado para presentar el redesign de Extractores Chile al cliente
antes de hacer deploy, enviando el PDF por WhatsApp para aprobacion.

## Stack

- Node.js + Playwright
- Python + Pillow
- Compatible con tuneles Cloudflare (cloudflared)

---

Parte del ecosistema KraftDo SpA — digitalizamos PYMEs chilenas.
https://kraftdo.cl
