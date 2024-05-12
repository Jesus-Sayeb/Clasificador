# Documentacion con Swagger: http://127.0.0.1:8000/docs
# Documentacion con Redocly: http://127.0.0.1:8000/redocs
from fastapi import File, UploadFile, HTTPException, APIRouter, Depends, Response, Body
from DB.cliente import client 
from DB.models.beca_mod import soli_bec
from DB.models.beca_mod import edit_soli_bec
import fitz

from pdf2image import convert_from_bytes
import os
from pymongo.collection import Collection 
from pruebayolo import *

from starlette.responses import StreamingResponse
import io
import zipfile

from OCR_Final import *
from pruebafecha import *
#fecha_referencia = "01.01.2023"
# Definir el arreglo fuera del endpoint
#nombres: List[str] = []

def guardar_pdf_como_imagenes(content: bytes, nombre_archivo: str, output_folder: str = "./pdf_images",
                              size: tuple = None) -> list:
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # opciones adicionales para la conversion
    conversion_kwargs = {}
    if size:
        conversion_kwargs['size'] = size    
    #Convertir el PDF a una lista de imágenes
    """convert_from_bytes(),trabaja directamente con el contenido binario de un archivo PDF. 
    Esto es útil cuando se trabaja con 
    PDFs en memoria o recibidos como archivos cargados en una aplicación web, 
    sin necesidad de guardarlos primero en el disco."""    
    
    images = convert_from_bytes(content, **conversion_kwargs)
    
    # Lista para guardar las rutas de las imágenes guardadas
    saved_images_paths = []

    # Guardar cada página como una imagen JPG
    for i, image in enumerate(images):
        filename = f"{nombre_archivo}_pagina_{i+1}.jpg"
        image_path = os.path.join(output_folder, filename)
        image.save(image_path, "JPEG")
        saved_images_paths.append(image_path)
    
    return saved_images_paths


# Suponiendo que tienes una función para obtener la colección de MongoDB
def get_db() -> Collection:
    return client["beca"]["solicitudes_beca"]

# La variable router_beca será un instancia de la clase APIRouter
router = APIRouter(tags=["Solicitud Beca"])

@router.post("/Cargar_Solicitud")
async def create_upload_file(file: UploadFile = File(...)):
    # Verificar si el archivo es un PDF
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="El archivo no es un PDF")
    
    content = await file.read()
    #Utilizar PyMuPDF para contar el número de páginas
    pdf_document = fitz.open("pdf", content)
    num_pages = len(pdf_document)
    # validar que el pdf contenga 4 paginas
    if num_pages != 4:
        raise HTTPException(status_code=400, detail="El numero de paginas no es correcto, recuerda que tu solicitud debe estar compuesta de 4 paginas")

    # Extraer el nombre del archivo (sin la extensión .pdf)
    nombre_archivo = file.filename.rsplit('.', 1)[0]  # Esto quita la extensión del archivo

    # Convertir el PDF en imágenes y guardarlas
    saved_images_paths = guardar_pdf_como_imagenes(content, nombre_archivo)

    # Dividir el nombre del archivo en sus partes
    partes_nombre = nombre_archivo.split('_')
    if len(partes_nombre) not in [5,6]:
        raise HTTPException(status_code=400, detail="El nombre del archivo no sigue la nomenclatura esperada")
    
    if len(partes_nombre) == 5:
        apell_al_pat,apell_al_mat,nombre_alumno, boleta, beca_solicitada = partes_nombre
        nombre_alumno2 = "Sin segundo nombre"
    else:
        apell_al_pat,apell_al_mat,nombre_alumno, nombre_alumno2, boleta, beca_solicitada = partes_nombre
    #encoded_pdf = base64.b64encode(content).decode('utf-8')

    if len(saved_images_paths) >= 4:  # Asegurando que hay al menos 4 páginas
    # Pagina 3 y 4 (índices 2 y 3)
        source0  = saved_images_paths[2]
        source1 = saved_images_paths[3]
        
        resultado_tipo_comp, conf_tipo_comp = clasificacion_tipo_comp(path_tipo_comp(source0))
        resultado_val_comp, conf_val_comp  = clasificacion_validez_comp(path_validez_comp(source0))

        resultado_tipo_conf_cred = clasificacion_tipo_cred(path_tipo_cred(source1))
        resultado_val_conf_cred = clasificacion_validez_cred(path_validez_cred(source1))

    img_tipo_comp="C:/Users/jesus/Documents/ESCOM/fastApi/pdf_images/tipo_comprobante.jpg"
    img_val_comp="C:/Users/jesus/Documents/ESCOM/fastApi/pdf_images/validez_comprobante.jpg"
    img_tipo_cred="C:/Users/jesus/Documents/ESCOM/fastApi/pdf_images/tipo_credencial.jpg"
    img_val_cred="C:/Users/jesus/Documents/ESCOM/fastApi/pdf_images/validez_credencial.jpg"

    def read_image_as_binary(filename):
        with open(filename, "rb") as image_file:
            return image_file.read()   
         
    img_t_comp = read_image_as_binary(img_tipo_comp)
    img_v_comp = read_image_as_binary(img_val_comp)
    img_t_cred = read_image_as_binary(img_tipo_cred)
    img_validez_cred = read_image_as_binary(img_val_cred)

    if resultado_val_comp == "C_VAL":
        fecha = imagen(source0)
        conver = convertir_fecha(fecha)
        valfech = validar_fecha(conver, "12.07.2023")
        if valfech == "VALIDO":
            aprobacion = True
        else:
            aprobacion = False 
    else:
        fecha = "No se extrajo fecha porque el comprobante es invalido o nulo"
        valfech = "INVALIDO"
        aprobacion = False

    if len(resultado_val_conf_cred) == 2:
        print(resultado_val_conf_cred)
    for resultado, _ in resultado_val_conf_cred:
        if "CRED_INVAL" in resultado or "NULL" in resultado:
            aprobacion = False
            break

     # Crear una instancia de soli_bec con los datos extraídos
    solicitud_beca = soli_bec(
        alumno_apellido_paterno = apell_al_pat,
        alumno_apellido_materno = apell_al_mat,
        alumno_primer_nombre = nombre_alumno,
        alumno_segundo_nombre = nombre_alumno2,
        boleta=int(boleta),
        beca_solicitada=beca_solicitada,

        tipo_comprobante = resultado_tipo_comp,
        conf_tipo_comprobante = conf_tipo_comp,  
        validez_comprobante = resultado_val_comp,
        conf_validez_comprobante = conf_val_comp,

        tipo_conf_credencial = resultado_tipo_conf_cred,
        validez_conf_credencial = resultado_val_conf_cred,

        beca_aprobada=aprobacion,
        solicitud_PDF= content,
        img_comprobante_tipo = img_t_comp,
        img_comprobante_validez= img_v_comp,
        img_credencial_tipo= img_t_cred,
        img_credencial_validez= img_validez_cred,

        fecha = fecha
    )

    # Guardar en MongoDB
   # db = client.beca
   # db.solicitudes_beca.insert_one(solicitud_beca.dict())
    
    return { "filename": file.filename, 
            "message": "Archivo PDF recibido y almacenado correctamente",

            "Tipo de comprobante": resultado_tipo_comp,
            "Confianza del tipo de comprobante": conf_tipo_comp,

            "Validez del comprobante": resultado_val_comp, 
            "Confianza de validez del comprobante": conf_val_comp,

            "Tipo y confianza de credencial ": resultado_tipo_conf_cred,
            "Validez y confianza de credencial": resultado_val_conf_cred,

            "La fecha extraida es": fecha,
            "La fecha de antiguedad del coprobante es": valfech,

            "La beca fue aprobada": aprobacion
    }
#---------------------------------------------------
@router.get("/Buscar_Solicitud/", 
    summary="Buscar una solicitud de beca específica",
    description='''Este endpoint permite buscar una solicitud de beca específica en la base de datos. \n\n
    Si deseas consultar el PDF de la solicitud y las imagenes clasificadas, descarga la solicitud completa.''')
async def read_solicitud(alumno_apellido_paterno: str, alumno_apellido_materno: str, boleta: int, db: Collection = Depends(get_db)):
    # Buscar la solicitud en la base de datos usando el apellido, nombre y boleta
    solicitud = db.find_one({"alumno_apellido_paterno": alumno_apellido_paterno, "alumno_apellido_materno": alumno_apellido_materno, "boleta": boleta})
    
    if solicitud:
        # Eliminar el campo _id y solicitud_PDF para evitar problemas de serialización y porque no se desean mostrar
        solicitud.pop("_id", None)
        #solicitud['solicitud_PDF'] = base64.b64encode(solicitud['solicitud_PDF']).decode('utf-8')  # Codificar PDF como base64 para evitar problemas de codificación al devolver JSON
        solicitud.pop("solicitud_PDF", None)
        solicitud.pop("img_comprobante_tipo", None)
        solicitud.pop("img_comprobante_validez", None)
        solicitud.pop("img_credencial_tipo", None)
        solicitud.pop("img_credencial_validez", None)
        return solicitud
    else:
        raise HTTPException(status_code=404, detail=f"No se encontró la solicitud con los datos ingresados")
#----------------------------------------------------------
@router.put("/Editar_Solicitud/",
            summary="Este endpoint permite buscar una solicitud de beca específica en la base de datos y editarla",
            description=''' Solo se permite editar los datos del alumno, los resultados de la clasificacion y si la beca fue aprobada o no \n\n
            En dado caso que quiera editar el PDF almacenado de la solicitud debera elimnar la solicitud previa y subir de nuevo el PDF.
''')
async def update_beca(alumno_apellido_paterno: str, alumno_apellido_materno: str, boleta: int, solicitud_beca: edit_soli_bec):
    db = client.beca
    # Buscar el documento que coincida con los tres campos
    documento_existente = db.solicitudes_beca.find_one({"alumno_apellido_paterno": alumno_apellido_paterno, "alumno_apellido_materno": alumno_apellido_materno, "boleta": boleta})

    if documento_existente is None:
        raise HTTPException(status_code=404, detail="La solicitud de beca no existe")

    # Actualizar documento
    db.solicitudes_beca.update_one(
        {"_id": documento_existente["_id"]},
        {"$set": solicitud_beca.dict(exclude_unset=True)}
    )
    return {"message": "Solicitud de beca actualizada con éxito"}
#----------------------------------------------------------

@router.delete("/Eliminar_Solicitud")
async def delete_solicitud(boleta: int, alumno_apellido_paterno: str, alumno_apellido_materno: str):
    db = client.beca
    result = db.solicitudes_beca.delete_one({
        "boleta": boleta,
        "apellido_alumno": alumno_apellido_paterno,
        "nombre_alumno": alumno_apellido_materno
    })

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    return {"message": "Solicitud eliminada correctamente"}
#-------------------------------------------------------------------------
@router.get("/Descargar_Solicitud_Completa/",
    summary="Descargar solicitud completa de beca",
    description="Este endpoint permite descargar el PDF y la imagen clasificada de la solicitud de beca basados en el apellido, nombre y número de boleta del solicitante.",
    responses={200: {"content": {"application/zip": {}}}})
async def download_complete_solicitud(alumno_apellido_paterno: str, alumno_apellido_materno: str, boleta: int, db: Collection = Depends(get_db)):
    solicitud = db.find_one({"alumno_apellido_paterno": alumno_apellido_paterno, "alumno_apellido_materno": alumno_apellido_materno, "boleta": boleta})
    
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada con los datos proporcionados.")

    pdf_content = solicitud.get('solicitud_PDF')
    img_content = solicitud.get('img_comprobante_tipo')
    img_v_comp = solicitud.get('img_comprobante_validez')
    img_t_cred = solicitud.get('img_credencial_tipo')
    img_v_cred = solicitud.get('img_credencial_validez')
    beca_soli = solicitud.get('beca_solicitada')
    
    if not pdf_content or not img_content:
        raise HTTPException(status_code=404, detail="El contenido necesario no está completamente disponible.")
    
    # Crear un buffer de memoria para el archivo ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(f"{alumno_apellido_paterno}_{alumno_apellido_materno}_{boleta}_{beca_soli}.pdf", pdf_content)
        zip_file.writestr(f"{alumno_apellido_paterno}_{alumno_apellido_materno}_{boleta}_tipo_comprobante.jpg", img_content)
        zip_file.writestr(f"{alumno_apellido_paterno}_{alumno_apellido_materno}_{boleta}_validez_comprobante.jpg", img_v_comp)
        zip_file.writestr(f"{alumno_apellido_paterno}_{alumno_apellido_materno}_{boleta}_tipo_credencial.jpg", img_t_cred)
        zip_file.writestr(f"{alumno_apellido_paterno}_{alumno_apellido_materno}_{boleta}_validez_credencial.jpg", img_v_cred)
    
    # Preparar el buffer para ser enviado como respuesta
    zip_buffer.seek(0)
    headers = {
        "Content-Disposition": f"attachment; filename={alumno_apellido_paterno}_{alumno_apellido_materno}_{boleta}_solicitud_completa.zip"
    }
    return StreamingResponse(zip_buffer, media_type="application/zip", headers=headers)
#-----------------------------------------------------------
