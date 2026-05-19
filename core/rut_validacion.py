"""
Módulo de validación de RUT chileno
Algoritmo oficial Módulo 11
"""

def limpiar_rut(rut_ingresado):
    """Elimina puntos y espacios del RUT. Devuelve (cuerpo, dv) o None si el formato es inválido."""
    rut = str(rut_ingresado).strip().replace(".", "").replace("-", "").replace(" ", "").upper()

    if len(rut) < 2:
        return None

    # El DV siempre es el último carácter, el cuerpo es el resto
    cuerpo = rut[:-1]
    dv = rut[-1]

    if not cuerpo.isdigit():
        return None

    if dv not in "0123456789K":
        return None

    if len(cuerpo) < 7 or len(cuerpo) > 8:
        return None

    return cuerpo, dv


def calcular_dv(cuerpo):
    """
    Calcula el dígito verificador esperado dado el cuerpo del RUT.
    Devuelve el DV como string ('0'-'9' o 'K') y el detalle del procedimiento.
    """
    factores = [2, 3, 4, 5, 6, 7]
    digitos = [int(d) for d in reversed(cuerpo)]

    productos = []
    suma = 0
    for i, digito in enumerate(digitos):
        factor = factores[i % 6]
        producto = digito * factor
        productos.append((digito, factor, producto))
        suma += producto

    resto = suma % 11
    dv_numerico = 11 - resto

    if dv_numerico == 11:
        dv_calculado = "0"
    elif dv_numerico == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(dv_numerico)

    procedimiento = {
        "digitos_con_factores": productos,
        "suma": suma,
        "resto": resto,
        "dv_numerico": dv_numerico,
        "dv_calculado": dv_calculado,
    }

    return dv_calculado, procedimiento


def generar_texto_procedimiento(cuerpo, dv_real, procedimiento):
    """
    Retorna el procedimiento paso a paso como un string formateado, 
    ideal para enviarlo a la interfaz web o imprimirlo.
    """
    lineas = []
    lineas.append("=" * 55)
    lineas.append("       VALIDACIÓN DE RUT — ALGORITMO MÓDULO 11")
    lineas.append("=" * 55)

    lineas.append(f"\nRUT ingresado : {cuerpo}-{dv_real}")
    lineas.append(f"Cuerpo        : {cuerpo}  ({len(cuerpo)} dígitos)")
    lineas.append(f"DV ingresado  : {dv_real}")

    lineas.append("\n--- PASO 1: Multiplicar dígitos por sus factores ---")
    lineas.append("(Se recorre el cuerpo de derecha a izquierda, ciclando 2→3→4→5→6→7)\n")

    lineas.append(f"  {'Posición':<12} {'Dígito':<10} {'Factor':<10} {'Producto'}")
    lineas.append(f"  {'-'*44}")

    for idx, (digito, factor, producto) in enumerate(procedimiento["digitos_con_factores"]):
        pos_label = f"d{len(cuerpo) - idx} (pos {idx+1})"
        lineas.append(f"  {pos_label:<12} {digito:<10} ×{factor:<9} = {producto}")

    lineas.append("\n--- PASO 2: Sumar todos los productos ---")
    suma_str = " + ".join(str(p) for _, _, p in procedimiento["digitos_con_factores"])
    lineas.append(f"  Suma = {suma_str}")
    lineas.append(f"  Suma total = {procedimiento['suma']}")

    lineas.append("\n--- PASO 3: Calcular el resto (Suma mod 11) ---")
    lineas.append(f"  {procedimiento['suma']} mod 11 = {procedimiento['resto']}")

    lineas.append("\n--- PASO 4: Calcular el DV esperado ---")
    lineas.append(f"  DV = 11 - resto = 11 - {procedimiento['resto']} = {procedimiento['dv_numerico']}")

    dv_num = procedimiento["dv_numerico"]
    if dv_num == 11:
        lineas.append("  Como el resultado es 11, el DV esperado es: 0")
    elif dv_num == 10:
        lineas.append("  Como el resultado es 10, el DV esperado es: K")
    else:
        lineas.append(f"  El DV esperado es: {procedimiento['dv_calculado']}")

    lineas.append("\n--- PASO 5: Comparar DV calculado vs DV ingresado ---")
    lineas.append(f"  DV calculado : {procedimiento['dv_calculado']}")
    lineas.append(f"  DV ingresado : {dv_real}")

    if procedimiento["dv_calculado"] == dv_real:
        lineas.append("\n  ✓ Los dígitos verificadores COINCIDEN.")
        lineas.append("  ✓ El RUT es VÁLIDO.")
    else:
        lineas.append("\n  ✗ Los dígitos verificadores NO coinciden.")
        lineas.append("  ✗ El RUT es INVÁLIDO.")

    lineas.append("=" * 55)
    return "\n".join(lineas)


def extraer_digitos(cuerpo):
    """Devuelve la lista [d1, d2, ..., d8] con ceros a la izquierda si el cuerpo tiene 7 dígitos."""
    cuerpo_8 = cuerpo.zfill(8)
    return [int(c) for c in cuerpo_8]


def validar_rut(rut_ingresado):
    """
    Función principal. Recibe un RUT, valida y devuelve todos los datos limpios.
    Retorna un diccionario con los datos listos para consumir desde la web o consola.
    """
    resultado = limpiar_rut(rut_ingresado)

    if resultado is None:
        return {
            "es_valido": False,
            "error": "Formato de RUT inválido. Ejemplos correctos: 12345678-9 o 12.345.678-9"
        }

    cuerpo, dv_real = resultado
    dv_calculado, procedimiento = calcular_dv(cuerpo)
    texto_procedimiento = generar_texto_procedimiento(cuerpo, dv_real, procedimiento)
    es_valido = (dv_calculado == dv_real)

    if es_valido:
        digitos = extraer_digitos(cuerpo)
        return {
            "es_valido": True,
            "digitos": digitos,
            "dv": dv_real,
            "texto_procedimiento": texto_procedimiento
        }
    else:
        return {
            "es_valido": False,
            "error": "El RUT ingresado es inválido.",
            "texto_procedimiento": texto_procedimiento
        }

def generar_texto_calculo(cuerpo, procedimiento):
    """
    Genera el texto paso a paso exclusivamente para cuando se está 
    calculando un DV faltante, sin comparar con uno ingresado.
    """
    lineas = []
    lineas.append("=" * 55)
    lineas.append("       CÁLCULO DE DÍGITO VERIFICADOR — MÓDULO 11")
    lineas.append("=" * 55)

    lineas.append(f"\nCuerpo ingresado : {cuerpo}  ({len(cuerpo)} dígitos)")

    lineas.append("\n--- PASO 1: Multiplicar dígitos por sus factores ---")
    lineas.append(f"  {'Posición':<12} {'Dígito':<10} {'Factor':<10} {'Producto'}")
    lineas.append(f"  {'-'*44}")

    for idx, (digito, factor, producto) in enumerate(procedimiento["digitos_con_factores"]):
        pos_label = f"d{len(cuerpo) - idx} (pos {idx+1})"
        lineas.append(f"  {pos_label:<12} {digito:<10} ×{factor:<9} = {producto}")

    lineas.append("\n--- PASO 2: Sumar todos los productos ---")
    suma_str = " + ".join(str(p) for _, _, p in procedimiento["digitos_con_factores"])
    lineas.append(f"  Suma = {suma_str}")
    lineas.append(f"  Suma total = {procedimiento['suma']}")

    lineas.append("\n--- PASO 3: Calcular el resto (Suma mod 11) ---")
    lineas.append(f"  {procedimiento['suma']} mod 11 = {procedimiento['resto']}")

    lineas.append("\n--- PASO 4: Calcular el DV esperado ---")
    lineas.append(f"  DV = 11 - resto = 11 - {procedimiento['resto']} = {procedimiento['dv_numerico']}")

    dv_num = procedimiento["dv_numerico"]
    if dv_num == 11:
        lineas.append("  Como el resultado es 11, el DV es: 0")
    elif dv_num == 10:
        lineas.append("  Como el resultado es 10, el DV es: K")
    else:
        lineas.append(f"  El DV es: {procedimiento['dv_calculado']}")

    lineas.append("\n--- RESULTADO FINAL ---")
    lineas.append(f"  ★ El RUT completo es: {cuerpo}-{procedimiento['dv_calculado']}")
    lineas.append("=" * 55)
    
    return "\n".join(lineas)


def completar_rut(cuerpo_ingresado):
    """
    Recibe un cuerpo de RUT (sin DV), lo limpia, calcula su DV 
    y retorna los datos y el procedimiento.
    """
    # Limpiamos puntos y espacios por si acaso
    cuerpo = str(cuerpo_ingresado).strip().replace(".", "").replace(" ", "")
    
    if not cuerpo.isdigit() or len(cuerpo) < 7 or len(cuerpo) > 8:
        return {
            "exito": False,
            "error": "El cuerpo del RUT debe tener entre 7 y 8 números."
        }
        
    dv_calculado, procedimiento = calcular_dv(cuerpo)
    texto_calculo = generar_texto_calculo(cuerpo, procedimiento)
    
    return {
        "exito": True,
        "rut_completo": f"{cuerpo}-{dv_calculado}",
        "dv": dv_calculado,
        "texto_procedimiento": texto_calculo
    }

# ── Ejecución directa ─────────────────────────────────────
if __name__ == "__main__":
    while True:
        print("\n=== MENÚ DE PRUEBAS DE RUT ===")
        print("1. Validar un RUT completo (ej: 12.345.678-9)")
        print("2. Calcular DV faltante (ej: 12345678)")
        print("3. Salir")
        
        opcion = input("Elige una opción (1-3): ")
        
        if opcion == "1":
            rut = input("\nIngresa el RUT completo: ")
            datos = validar_rut(rut)
            
            if "error" in datos and not datos.get("texto_procedimiento"):
                print(f"\n[ERROR] {datos['error']}")
            else:
                print("\n" + datos["texto_procedimiento"])
                if datos["es_valido"]:
                    print(f"\nLista de dígitos extraídos: {datos['digitos']}")
                    
        elif opcion == "2":
            cuerpo = input("\nIngresa el cuerpo del RUT (sin guion ni DV): ")
            datos = completar_rut(cuerpo)
            
            if not datos["exito"]:
                print(f"\n[ERROR] {datos['error']}")
            else:
                print("\n" + datos["texto_procedimiento"])
                
        elif opcion == "3":
            print("Saliendo del programa de pruebas...")
            break
            
        else:
            print("Opción inválida. Intenta de nuevo.")
