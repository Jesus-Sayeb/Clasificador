import re
from datetime import datetime

def convertir_fecha(fecha_str):
    # Diccionario para convertir nombre del mes a número
    meses = {
        'Enero': '01', 'Febrero': '02', 'Marzo': '03', 'Abril': '04', 'Mayo': '05', 'Junio': '06',
        'Julio': '07', 'Agosto': '08', 'Septiembre': '09', 'Octubre': '10', 'Noviembre': '11', 'Diciembre': '12',
        'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
        'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
    }
    
    # Intentar parsear la fecha según diferentes formatos conocidos
    try:
        if re.match(r'\d{2} de [A-Za-z]+ \d{4}', fecha_str):
            # "10 de Enero 2023"
            dia, mes_nombre, año = re.match(r'(\d{2}) de ([A-Za-z]+) (\d{4})', fecha_str).groups()
            mes_nombre = mes_nombre.capitalize()
            mes_numero = meses[mes_nombre]
        elif re.match(r'\d{2} [A-Z]{3} \d{4}', fecha_str):
            # "21 SEP 2023"
            dia, mes, año = fecha_str.split()
            mes_numero = meses[mes.upper()]
        elif re.match(r'\d{2}-[A-Z]{3}-\d{4}', fecha_str):
            # "21-MAR-2024"
            dia, mes, año = fecha_str.split('-')
            mes_numero = meses[mes]
        elif re.match(r'\d{2}\.\d{2}\.\d{4}', fecha_str):
            # "23.01.2024"
            return fecha_str
        else:
            raise ValueError("Formato de fecha no reconocido.")
        
        # Construir la nueva fecha en formato "DD.MM.AAAA"
        nueva_fecha = f"{int(dia):02d}.{mes_numero}.{año}"
        return nueva_fecha
    except Exception as e:
        return f"Error: {str(e)}"


