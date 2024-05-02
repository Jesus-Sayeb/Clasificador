from ultralytics import YOLO
import cv2 as cv
import easyocr
from dateutil import parser
from datetime import datetime, timedelta
from pruebafecha import *

mod_coordenadas = YOLO("C:/Users/jesus/Documents/ESCOM/fastAPI/Modelos/FechaComp.pt")
path = "C:/Users/jesus/Documents/ESCOM/fastAPI/PDF_Pruebas/4hojasOCR/1.jpg"
# Suponiendo que 'fecha' es una cadena obtenida de la imagen
# para comparar con la fecha actual se debe quitar "fecha_referencia_str" que se le pasa a la funcion validar_fecha
def validar_fecha(fecha_str, fecha_referencia_str):
    """
    Esta función analiza una cadena que representa una fecha en diversos formatos
    y verifica si está dentro de los últimos tres meses desde la fecha actual.
    """
    try:
        # Analizar la fecha desde la cadena
        fecha_extraida = parser.parse(fecha_str, dayfirst=True)
        
        # Obtener la fecha actual
        #fecha_actual = datetime.now()
        # fechas de prueba
        fecha_referencia = parser.parse(fecha_referencia_str, dayfirst=True)
        # Calcular la fecha límite (hace 3 meses)
        tres_meses_atras = fecha_referencia - timedelta(days=90)
        
        # Verificar si la fecha extraída es más reciente que la fecha límite
        if fecha_extraida >= tres_meses_atras and fecha_extraida <= fecha_referencia:
            return "VALIDO"
            #return True, fecha_extraida.strftime('%d-%m-%Y')
        else:
            return "INVALIDO"
            #return False, fecha_extraida.strftime('%d-%m-%Y')
    except ValueError:
        return "Formato de fecha no válido."


def obtener_coordenadas(imagen):
    results = mod_coordenadas(imagen, conf=0.7, imgsz=768)
    boxes = results[0].boxes
    if len(boxes.xyxy) > 0:
        coordenadas = boxes.xyxy[0]
        return coordenadas
    else:
        # Devolver None o lanzar un error específico si no se encuentran coordenadas.
        return None

def read_fecha(result, frame, reader):
    xmin, ymin, xmax, ymax = result[:4]
    plate = frame[int(ymin):int(ymax), int(xmin):int(xmax)]

    # Ajustar brillo y claridad
    alpha = 1.5  # Factor para el brillo
    beta = 50    # Incremento para la claridad
    bright_adjusted = cv.convertScaleAbs(plate, alpha=alpha, beta=beta)

    # Convertir a escala de grises
    gray = cv.cvtColor(bright_adjusted, cv.COLOR_BGR2GRAY)

    # OCR
    text = reader.readtext(gray)
    text = ' '.join([t[1] for t in text])
    return text

def imagen(source0):
    # Cargar el lector OCR
    reader = easyocr.Reader(['es'])

    # Leer y procesar la única imagen
    imagen = cv.imread(source0)
    coordenadas = obtener_coordenadas(imagen)

    if coordenadas is not None:
        # Procesar la detección de texto y OCR para la única imagen
        extracted_text = read_fecha(coordenadas, imagen, reader)
        #print("Texto extraído:", extracted_text)
        #print(type(extracted_text))
        return extracted_text
    else:
        return "No se encontraron fechas en la imagen"

#fechaConvertida = convertir_fecha(imagen(path))
"""
resultado_validacion, fecha_formateada = validar_fecha(fechaConvertida, fecha_referencia)
if resultado_validacion:
    print("La fecha está dentro del rango permitido:", fecha_formateada)
else:
    print("La fecha NO está dentro del rango permitido o es inválida:", fecha_formateada)


print(f"la fecha es: {imagen(path)}")
"""