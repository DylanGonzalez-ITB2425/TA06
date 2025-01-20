import os
import traceback

def determinar_delimitador_y_columnas(archivo):
    """
    Función que lee las primeras dos líneas de un archivo para determinar el delimitador
    y el número de columnas.
    """
    with open(archivo, 'r') as file:
        lineas = [next(file) for _ in range(2)]  # Leer las primeras dos líneas
        
    # Verificar que las primeras dos líneas tengan el mismo formato
    if lineas[0].strip() != lineas[1].strip():
        return None, None
    
    # Determinar el delimitador (espacios, comas, tabulaciones)
    delimitadores_posibles = [' ']
    delimitador_detectado = None
    num_columnas = None

    for linea in lineas:
        for delimitador in delimitadores_posibles:
            columnas = linea.strip().split(delimitador)
            if num_columnas is None:
                num_columnas = len(columnas)
                delimitador_detectado = delimitador
            elif len(columnas) != num_columnas:
                return None, None  # No es consistente con las columnas esperadas
    
    return delimitador_detectado, num_columnas

def verificar_formato_archivos(carpeta, archivos):
    """
    Función que recorre todos los archivos en la carpeta, verifica que todos los archivos
    tengan el mismo número de columnas y delimitador, y cumplan con las restricciones adicionales.
    """
    delimitador_global = None
    num_columnas_global = None
    archivos_incorrectos = []

    # Procesar los archivos en lotes para evitar sobrecargar la memoria
    for archivo in archivos:
        archivo_completo = os.path.join(carpeta, archivo)
        
        # Verificar el delimitador y número de columnas en el archivo
        delimitador, num_columnas = determinar_delimitador_y_columnas(archivo_completo)
        
        if delimitador is None:
            archivos_incorrectos.append((archivo, "Error en la detección del delimitador"))  # Si no hay consistencia, el archivo es incorrecto
        elif delimitador_global is None and num_columnas_global is None:
            # Primer archivo, establecer el formato global
            delimitador_global = delimitador
            num_columnas_global = num_columnas
        elif delimitador != delimitador_global or num_columnas != num_columnas_global:
            # Si el delimitador o el número de columnas no coincide, el archivo es incorrecto
            archivos_incorrectos.append((archivo, "Error en la línea: " + str(lineas.index(linea) + 1)))
        
        # Verificar restricciones adicionales
        with open(archivo_completo, 'r') as file:
            lineas = file.readlines()
        
        # Verificar que cada año tenga 12 meses
        for i in range(2, len(lineas)):
            if i % 13 == 0:
                if lineas[i].strip() != '':
                    archivos_incorrectos.append((archivo, f"Error en la línea {i + 1}: Se esperaba una línea en blanco"))
            else:
                columnas = lineas[i].strip().split(delimitador)
                if len(columnas) != num_columnas:
                    archivos_incorrectos.append((archivo, f"Error en la línea {i + 1}: Número de columnas incorrecto"))
                elif i % 13 == 1 and columnas[0][0] != 'P':
                    archivos_incorrectos.append((archivo, f"Error en la línea {i + 1}: La primera letra de la primera columna debe ser 'P'"))
                elif i % 13 > 1:
                    for j in range(1, len(columnas)):
                        if not columnas[j].isdigit() and not columnas[j].replace('-', '').isdigit():
                            archivos_incorrectos.append((archivo, f"Error en la línea {i + 1}, columna {j + 1}: No se permiten letras, puntos ni comas"))
        
        # Verificar que los años sean de 2006 al 2100
        anio = int(lineas[2].strip().split(delimitador)[1])
        if anio < 2006 or anio > 2100:
            archivos_incorrectos.append((archivo, f"Error en la línea 3: El año debe estar entre 2006 y 2100"))

    return archivos_incorrectos

def procesar_archivos_en_lotes(carpeta, archivos, batch_size=1000):
    """
    Función que procesa los archivos por lotes, para manejar grandes cantidades de archivos. salida
    """
    archivos_incorrectos_totales = []

    for i in range(0, len(archivos), batch_size):
        # Procesar lotes de archivos
        batch = archivos[i:i + batch_size]
        archivos_incorrectos = verificar_formato_archivos(carpeta, batch)
        archivos_incorrectos_totales.extend(archivos_incorrectos)
        
        # Puedes agregar un mensaje de progreso
        print(f"Procesando lotes erroneos {i // batch_size + 1} de {len(archivos) // batch_size + 1} archivos...")

    return archivos_incorrectos_totales


# Ejemplo de uso con la ruta correcta de la carpeta
carpeta = '/home/adria.montero.7e5/Baixades/TA06/TA06/E01/precip.MIROC5.RCP60.2006-2100.SDSM_REJ'
archivos = os.listdir(carpeta)

# Filtrar solo los archivos .dat
archivos_dat = [archivo for archivo in archivos if archivo.endswith('.dat')]

# Procesar los archivos en lotes de 1000 (puedes ajustar el tamaño del lote)
archivos_incorrectos = procesar_archivos_en_lotes(carpeta, archivos_dat, batch_size=1000)

if archivos_incorrectos:
    print("Los siguientes archivos no están en el formato correcto:")
    for archivo, error in archivos_incorrectos:
        print(f"Archivo: {archivo}, Error: {error}")
else:
    print("Todos los archivos tienen el mismo formato.")
