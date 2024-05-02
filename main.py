from Routers import Soli_Bec
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


app = FastAPI()

# Routers
app.include_router(Soli_Bec.router)

#funcion editar el header del API
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Clasificador de Comprobantes de Domicilio y Credenciales de identificación",
        version="IA",
        summary="El documento que debes subir debe ser nombrado con la nomenclatura que se menciona abajo, ser en formato PDF y debe ser conformado por 4 hojas.",
        description=''' 
        * Nomenclatura para nombrar el documento: Apellido Paterno_Apellido Materno_Nombre(s)_Boleta_Beca Solicitada. \n\n 
        * Hoja uno y dos: Acuse de solicitud de beca y carta compromiso. \n\n 
        * Hoja tres: Comprobante de domicilio (agua, gas, luz, telefono). \n\n
        * Hoja cuatro: FRENTE de credencial de identificacion (INE o credencial escolar) y REVERSO de credencial de identificacion (INE o credencial escolar).''',
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# Cuando construyes una API, el "path" es la manera principal de separar los "intereses" y los "recursos".
@app.get("/main")
# "/" en het significa que esta en la raiz de la ip donde se este desplegando la api
# no podemos tener 5 operaciones get en la raiz, solo se debetener una
async def root():
    return {"message": "hola inicio"}
