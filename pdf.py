from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from PIL import Image as PILImage
import os
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
CARPETA = "screenshots"
OUTPUT = "Reporte_Extractores_Perfecto.pdf"

# ==========================================
# 2. LÓGICA DE ORDENAMIENTO (AGRUPACIÓN EXACTA)
# ==========================================
def obtener_prioridades(nombre_archivo):
    """
    Agrupa dinámicamente por el nombre de la vista (ignorando el dispositivo)
    y luego ordena estrictamente: Desktop (1) -> Tablet (2) -> Mobile (3).
    """
    nombre = nombre_archivo.lower()
    
    # 1. Determinar el orden del dispositivo
    if "desktop" in nombre or "escritorio" in nombre:
        dispositivo = 1
    elif "tablet" in nombre:
        dispositivo = 2
    elif "mobile" in nombre or "celular" in nombre:
        dispositivo = 3
    else:
        dispositivo = 4
        
    # 2. Extraer la "raíz" (nombre base) de la página
    # Le quitamos las palabras de dispositivo y extensiones para que queden agrupados
    raiz = nombre.replace("desktop", "").replace("tablet", "").replace("mobile", "")
    raiz = raiz.replace(".png", "").replace(".jpg", "").replace("_", "").strip()
    
    # Si la raíz queda vacía (como en tu archivo __desktop.png), asumimos que es el Home
    # Le ponemos "00_home" para forzar que el Home sea lo primero en todo el PDF
    if not raiz:
        raiz = "00_home"
        
    # Retorna la tupla. Ordena alfabéticamente por página, y luego por tamaño de pantalla.
    return (raiz, dispositivo, nombre_archivo)

def limpiar_titulo(nombre_archivo):
    """Genera un título muy limpio y profesional a partir del nombre del archivo."""
    nombre = nombre_archivo.lower().replace(".png", "").replace(".jpg", "")
    
    # Determinar texto del dispositivo
    disp_txt = ""
    if "desktop" in nombre: disp_txt = "(Vista Escritorio)"
    elif "tablet" in nombre: disp_txt = "(Vista Tablet)"
    elif "mobile" in nombre: disp_txt = "(Vista Celular)"
        
    # Extraer nombre base limpio
    base = nombre.replace("desktop", "").replace("tablet", "").replace("mobile", "")
    base = base.replace("_", " ").strip().title()
    
    if not base:
        base = "Página De Inicio"
        
    return f"{base} {disp_txt}".strip()

def get_proportional_image(image_path, max_width, max_height):
    try:
        img = PILImage.open(image_path)
        img_width, img_height = img.size
        aspect_ratio = img_height / float(img_width)
        new_width = max_width
        new_height = new_width * aspect_ratio
        
        if new_height > max_height:
            new_height = max_height
            new_width = new_height / aspect_ratio
        return new_width, new_height
    except Exception as e:
        print(f"Error con dimensiones: {e}")
        return max_width, max_height

# ==========================================
# 3. ESTILOS Y HEADER/FOOTER
# ==========================================
styles = getSampleStyleSheet()
COLOR_PRIMARIO = colors.HexColor("#0d2a4a")
COLOR_FONDO_TITULO = colors.HexColor("#f0f4f8")

estilo_portada = ParagraphStyle("Portada", parent=styles["Title"], fontSize=32, spaceAfter=20, textColor=COLOR_PRIMARIO, alignment=TA_CENTER, fontName="Helvetica-Bold")
estilo_subtitulo = ParagraphStyle("Subtitulo", parent=styles["Normal"], fontSize=16, textColor=colors.dimgray, alignment=TA_CENTER, spaceAfter=30)
estilo_titulos_img = ParagraphStyle("TitulosImg", parent=styles["Heading2"], fontSize=14, textColor=COLOR_PRIMARIO, alignment=TA_CENTER, spaceAfter=15, spaceBefore=20, backColor=COLOR_FONDO_TITULO, borderPadding=10)
estilo_cuerpo = ParagraphStyle("Cuerpo", parent=styles["Normal"], fontSize=12, leading=18, alignment=TA_JUSTIFY, textColor=colors.darkslategray)

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.lightgrey)
    canvas.line(40, 40, A4[0] - 40, 40)
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.gray)
    canvas.drawString(40, 25, "Extractores Chile - Reporte de Diseño Responsivo")
    if doc.page > 1:
        canvas.drawRightString(A4[0] - 40, 25, f"Página {doc.page}")
    canvas.restoreState()

# ==========================================
# 4. CONSTRUCCIÓN DEL DOCUMENTO
# ==========================================
doc = SimpleDocTemplate(OUTPUT, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=50, bottomMargin=60)
story = []

# --- A. PORTADA ---
fecha_hoy = datetime.now().strftime("%d de %B, %Y")
story.append(Spacer(1, 150))
story.append(Paragraph("Extractores Chile", estilo_portada))
story.append(Paragraph("Reporte Visual de Interfaz (UI) y Experiencia de Usuario (UX)", estilo_subtitulo))
story.append(Spacer(1, 30))
story.append(Paragraph(f"Fecha de entrega: {fecha_hoy}", ParagraphStyle("Fecha", parent=estilo_subtitulo, fontSize=12)))
story.append(PageBreak())

# --- B. RESUMEN EJECUTIVO ---
story.append(Paragraph("1. Resumen del Proyecto", ParagraphStyle("H1", parent=styles["Heading1"], textColor=COLOR_PRIMARIO, fontSize=20)))
story.append(Spacer(1, 15))

texto_intro = """
En este documento presentamos el resultado final de las vistas clave del rediseño web. 
El objetivo principal de esta actualización ha sido modernizar la identidad visual, 
mejorar la legibilidad de la información técnica (como los beneficios ecológicos y características de los extractores) 
y optimizar los puntos de contacto (botones de WhatsApp y formularios de cotización) en todos los 
dispositivos.<br/><br/>
Para facilitar su revisión, <b>cada página ha sido agrupada de forma independiente</b>, mostrando 
el flujo exacto de adaptación a pantallas de <b>Escritorio, Tablet y Celular</b> de manera secuencial.
"""
story.append(Paragraph(texto_intro, estilo_cuerpo))
story.append(PageBreak())

# --- C. PROCESAMIENTO DE IMÁGENES ORDENADAS ---
if os.path.exists(CARPETA):
    archivos = [f for f in os.listdir(CARPETA) if f.lower().endswith((".png", ".jpg"))]
    
    # Aquí ocurre la magia: Agrupa por vista y luego ordena Escritorio->Tablet->Celular
    imagenes_ordenadas = sorted(archivos, key=obtener_prioridades)
    
    for img in imagenes_ordenadas:
        ruta = os.path.join(CARPETA, img)
        titulo = limpiar_titulo(img)
        
        bloque = []
        bloque.append(Paragraph(titulo, estilo_titulos_img))
        
        w, h = get_proportional_image(ruta, doc.width, doc.height - 80)
        
        try:
            imagen_final = RLImage(ruta, width=w, height=h)
            bloque.append(imagen_final)
        except Exception as e:
            continue
        
        story.append(KeepTogether(bloque))
        story.append(PageBreak())

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"✅ Reporte PERFECTO generado con éxito: {OUTPUT}")