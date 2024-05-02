from pydantic import BaseModel
from typing import List, Tuple


class soli_bec(BaseModel):
   # id: str | None
    alumno_apellido_paterno: str
    alumno_apellido_materno: str
    alumno_primer_nombre: str
    alumno_segundo_nombre: str
    boleta: int
    beca_solicitada: str

    tipo_comprobante: str
    conf_tipo_comprobante: float
    validez_comprobante: str
    conf_validez_comprobante: float

    tipo_conf_credencial: List[Tuple[str,float]]
    validez_conf_credencial: List[Tuple[str,float]]
    
    beca_aprobada: bool
    
    solicitud_PDF: bytes
    img_comprobante_tipo: bytes
    img_comprobante_validez: bytes
    img_credencial_tipo: bytes
    img_credencial_validez: bytes

    fecha: str

class edit_soli_bec(BaseModel):
   # id: str | None
    alumno_apellido_paterno: str
    alumno_apellido_materno: str
    alumno_primer_nombre: str
    alumno_segundo_nombre: str
    boleta: int
    beca_solicitada: str

    tipo_comprobante: str
    conf_tipo_comprobante: float
    validez_comprobante: str
    conf_validez_comprobante: float

    tipo_conf_credencial: List[Tuple[str,float]]
    validez_conf_credencial: List[Tuple[str,float]]
    
    beca_aprobada: bool
