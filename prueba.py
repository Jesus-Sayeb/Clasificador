def verificar_credencial(resultado_val_conf_cred):
    aprobacion = True  # Asumimos inicialmente que la credencial es válida

    # Revisar cada resultado para ver si es inválido
    for resultado in resultado_val_conf_cred:
        print("Revisando resultado:", resultado)  # Debug: Ver qué se está revisando
        # Verificar si el resultado indica credencial inválida o nula
        if "CRED_INVAL" in resultado[0] or "NULL" in resultado[0]:
            aprobacion = False
            print("Encontrado inválido:", resultado)  # Debug: Confirmar cuál resultado es inválido
            break  # Si se encuentra un resultado inválido, termina el bucle

    print("Aprobación final:", aprobacion)  # Debug: Ver el estado final de 'aprobacion'
    return aprobacion

# Ejemplo de llamada de función
resultado_val_conf_cred = [
    ["CRED_VAL", 0.9769445061683655],
    ["CRED_INVAL", 0.9414406418800354]
]

verificar_credencial(resultado_val_conf_cred)
