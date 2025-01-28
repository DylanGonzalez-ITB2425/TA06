import os

# Leer el archivo con formato específico
def load_data(file_path):
    """Carga el archivo y devuelve los datos como una lista de diccionarios."""
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()[2:]  # Ignorar las primeras dos líneas (si son encabezados)
        for line in lines:
            parts = line.split()
            try:
                record = {
                    'ID': parts[0],
                    'Year': int(parts[1]),
                    'Month': int(parts[2]),
                    'Days': [float(x) if x != '-999' else None for x in parts[3:]]
                }
                data.append(record)
            except ValueError as e:
                print(f"Error al procesar la línea: {line}. Error: {e}")
    return data

# Manejo de valores faltantes
def handle_missing_values(data):
    """Reemplaza valores faltantes o inválidos."""
    for record in data:
        record['Days'] = [x if x is not None else -999 for x in record['Days']]
    return data

# Cálculo de medias anuales
def calculate_annual_means(data):
    """Calcula la media anual de la precipitación acumulada y devuelve una lista de años con sus medias."""
    annual_data = {}
    
    for record in data:
        year = record['Year']
        valid_values = [x for x in record['Days'] if x != -999]
        
        if year not in annual_data:
            annual_data[year] = []
        
        annual_data[year].extend(valid_values)
    
    annual_means = []
    for year, values in annual_data.items():
        if values:  # Evitar división por cero si no hay valores válidos
            total_precipitation = sum(values)  # Sumar toda la precipitación del año
            annual_means.append((year, total_precipitation))
    
    return sorted(annual_means, key=lambda x: x[0])  # Ordenar por año

# Procesar todos los archivos en una carpeta en paquetes
def process_folder_in_batches(folder_path, batch_size=1000):
    """Procesa los archivos en una carpeta en paquetes de tamaño especificado y genera informes."""
    total_files = 0
    total_lines = 0
    overall_annual_means = {}

    if not os.path.exists(folder_path):
        print(f"La carpeta {folder_path} no existe.")
        return

    all_files = [os.path.join(root, file_name)
                 for root, _, files in os.walk(folder_path)
                 for file_name in files if os.path.isfile(os.path.join(root, file_name))]
    
    total_batches = (len(all_files) + batch_size - 1) // batch_size

    for batch_num in range(total_batches):
        start_index = batch_num * batch_size
        end_index = min(start_index + batch_size, len(all_files))
        batch_files = all_files[start_index:end_index]

        print(f"Procesando paquete {batch_num + 1} de {total_batches}...")

        for file_path in batch_files:
            try:
                data = load_data(file_path)
                data = handle_missing_values(data)
                
                annual_means = calculate_annual_means(data)
                for year, mean in annual_means:
                    if year not in overall_annual_means:
                        overall_annual_means[year] = []
                    overall_annual_means[year].append(mean)
                
                total_files += 1
                total_lines += len(data)
            except Exception as e:
                print(f"Error procesando el archivo {file_path}: {e}")

    # Calcular la media anual combinada
    combined_annual_means = [(year, sum(means) / len(means)) for year, means in overall_annual_means.items()]
    combined_annual_means = sorted(combined_annual_means, key=lambda x: x[0])

    # Informe único con todos los resultados
    print("""
========================================================
ANÁLISIS DE PRECIPITACIÓN - INFORME COMPLETO
========================================================

1. ESTADÍSTICAS GENERALES
--------------------------------------------------------
Archivos procesados: {total_files:,}
Líneas procesadas: {total_lines:,}
""".format(total_files=total_files, total_lines=total_lines))

    print("\n========================================================")
    print("MEDIAS ANUALES DE PRECIPITACIÓN ACUMULADA")
    print("========================================================")
    print("{:<10} {:<15}".format("Año", "Precipitación (mm)"))
    print("-" * 25)
    for year, mean in combined_annual_means:
        print("{:<10} {:<15.2f}".format(year, mean))

# Ruta de la carpeta a analizar
carpeta = r'TA06/E01/precip.MIROC5.RCP60.2006-2100.SDSM_REJ'
process_folder_in_batches(carpeta)
