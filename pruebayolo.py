from ultralytics import YOLO

#Se cargan los modelos de clasificacion 
mod_comp_tipo = YOLO('C:/Users/jesus/Documents/ESCOM/fastAPI/Modelos/CompTipo2.pt')  # load a custom model
mod_comp_val = YOLO("C:/Users/jesus/Documents/ESCOM/fastAPI/Modelos/CompValidez.pt")

mod_cred_tipo = YOLO("C:/Users/jesus/Documents/ESCOM/fastAPI/Modelos/CredTipo2.pt")
mod_cred_val = YOLO("C:/Users/jesus/Documents/ESCOM/fastAPI/Modelos/CredVal3.pt")

# {0: 'C_AGUA', 1: 'C_LUZ', 2: 'C_GAS', 3: 'C_TEL', 4: 'NULL'}
# {0: 'C_VAL', 1: 'C_INVA', 2: 'NULL'}
# {0: 'ESCOM_FRENTE', 1: 'ESCOM_REVERSO', 2: 'INE_FRENTE', 3: 'INE_REVERSO', 4: 'NULL_CRED'}
# {0: 'CRED_VAL', 1: 'CRED_INVAL', 2: 'NULL'}

# Funcion que recibe la ruta de la imagen del comprobante a clasificar en la pagina 3
# y le aplica el modelo de tipo de comprobante 
def path_tipo_comp(source0): # conf = 0.81
    results0 = mod_comp_tipo(source0, conf= 0.8, imgsz=768)
    for r in results0:
        r.save(filename="C:/Users/jesus/Documents/ESCOM/fastApi/pdf_images/tipo_comprobante.jpg")
    return results0

# Funcion que extrae el resultado del tipo de comprobante y su confianza 
def clasificacion_tipo_comp(results0):  
    class_name = "sin deteccion tipo de comprobante, revisar manualmente"
    conf_score = 100.0 
    for result in results0:
        for i in range(len(result.boxes)):
            class_name = result.names[result.boxes.cls[i].tolist()] # Obtener el nombre de la clase para cada detección
            conf_score = result.boxes.conf[i].item() # Obtener la puntuación de confianza para cada detección    
        return str(class_name), float(conf_score)

# Funcion que recibe la ruta de la imagen del comprobante a clasificar 
# y le aplica el modelo de validez de comprobante
def path_validez_comp(source0):
    results1 = mod_comp_val(source0, conf=0.7, imgsz=768)
    for r in results1:
        r.save(filename="C:/Users/jesus/Documents/ESCOM/fastApi/pdf_images/validez_comprobante.jpg")
    return results1

# Funcion que extrae el resultado de validez de comprobante y su confianza
def clasificacion_validez_comp(results1):  
    class_name = "sin deteccion validez de comprobante, revisar manualmente"
    conf_score = 100.0   
    for result in results1:
        for i in range(len(result.boxes)):
            class_name = result.names[result.boxes.cls[i].tolist()] # Obtener el nombre de la clase para cada detección
            conf_score = result.boxes.conf[i].item() # Obtener la puntuación de confianza para cada detección
    return str(class_name), float(conf_score)

# Funcion que recibe la ruta de la imagen que contiene la identificacion a clasificar 
# y le aplica el modelo de tipo de identificacion
def path_tipo_cred(source1):
    results2 = mod_cred_tipo(source1, conf=0.7, imgsz=768)
    for r in results2:
        r.save(filename="C:/Users/jesus/Documents/ESCOM/fastApi/pdf_images/tipo_credencial.jpg")
    return results2

# Funcion que extrae el resultado del tipo de credencial y su confianza
def clasificacion_tipo_cred(results2):  
    resultados = []  
    for result in results2:
        for i in range(len(result.boxes)):
            class_name = result.names[result.boxes.cls[i].tolist()] # Obtener el nombre de la clase para cada detección
            conf_score = result.boxes.conf[i].item() # Obtener la puntuación de confianza para cada detección
            resultados.append((str(class_name), float(conf_score)))
    if len(resultados) != 2:
        resultados.append((("Sin deteccion. Revisar manualmente"),(100.00)))
    return resultados

# Funcion que recibe la ruta de la imagen que contiene la identificacion a clasificar 
# y le aplica el modelo de validez de identificacion
def path_validez_cred(source1):
    results3 = mod_cred_val(source1, conf=0.7, imgsz=768)
    for r in results3:
        r.save(filename="C:/Users/jesus/Documents/ESCOM/fastApi/pdf_images/validez_credencial.jpg")
    return results3

# Funcion que extrae el resultado del tipo de credencial y su confianza
def clasificacion_validez_cred(results3):
    resultados1=[]    
    for result in results3:
        for i in range(len(result.boxes)):
            class_name = result.names[result.boxes.cls[i].tolist()] # Obtener el nombre de la clase para cada detección
            conf_score = result.boxes.conf[i].item() # Obtener la puntuación de confianza para cada detección
            resultados1.append((str(class_name), float(conf_score)))
    if len(resultados1) != 2:
        resultados1.append((("Sin deteccion. Revisar manualmente"),(100.00)))
    return resultados1
