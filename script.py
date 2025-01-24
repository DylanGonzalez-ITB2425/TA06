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

# Estadísticas descriptivas
def generate_statistics(data):
    """Genera estadísticas descriptivas para los datos."""
    total_values = 0
    missing_values = 0

    for record in data:
        total_values += len(record['Days'])
        missing_values += sum(1 for x in record['Days'] if x == -999)

    return total_values, missing_values

# Cálculo de medias anuales
def calculate_annual_means(data):
    """Calcula la media anual de la precipitación y devuelve una lista de años con sus medias."""
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
            mean_precipitation = sum(values) / len(values)
            annual_means.append((year, mean_precipitation))
    
    return sorted(annual_means, key=lambda x: x[0])  # Ordenar por año

# Procesar todos los archivos en una carpeta en paquetes
def process_folder_in_batches(folder_path, batch_size=1000):
    """Procesa los archivos en una carpeta en paquetes de tamaño especificado y genera informes."""
    total_files = 0
    total_lines = 0
    total_values = 0
    missing_values = 0
    overall_annual_means = {}

    if not os.path.exists(folder_path):
        print(f"La carpeta {folder_path} no existe.")
        return

    # Obtener todos los archivos de la carpeta
    all_files = []
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                all_files.append(file_path)

    total_batches = (len(all_files) + batch_size - 1) // batch_size  # Número total de paquetes

    # Procesar los archivos en lotes
    for batch_num in range(total_batches):
        start_index = batch_num * batch_size
        end_index = min(start_index + batch_size, len(all_files))
        batch_files = all_files[start_index:end_index]

        print(f"Procesando paquete {batch_num + 1} de {total_batches}...")

        for file_path in batch_files:
            try:
                # Procesar cada archivo
                data = load_data(file_path)
                data = handle_missing_values(data)

                file_total_values, file_missing_values = generate_statistics(data)

                total_files += 1
                total_lines += len(data)
                total_values += file_total_values
                missing_values += file_missing_values

                # Calcular medias anuales por archivo
                annual_means = calculate_annual_means(data)
                for year, mean in annual_means:
                    if year not in overall_annual_means:
                        overall_annual_means[year] = []
                    overall_annual_means[year].append(mean)

            except Exception as e:
                print(f"Error procesando el archivo {file_path}: {e}")

    # Calcular la media anual combinada
    combined_annual_means = []
    for year, means in overall_annual_means.items():
        combined_mean = sum(means) / len(means)
        combined_annual_means.append((year, combined_mean))
    combined_annual_means = sorted(combined_annual_means, key=lambda x: x[0])

    # Calcular el porcentaje de valores faltantes
    missing_percentage = (missing_values / total_values) * 100 if total_values > 0 else 0

    # Informe único con todos los resultados
    print("""
========================================================
ANÁLISIS DE PRECIPITACIÓN - INFORME COMPLETO
========================================================

1. ESTADÍSTICAS GENERALES
--------------------------------------------------------
Total de valores procesados: {total_values:,}
Valores faltantes (-999): {missing_values:,}
Porcentaje de datos faltantes: {missing_percentage:.2f}%
Archivos procesados: {total_files:,}
Líneas procesadas: {total_lines:,}
""".format(
        total_values=total_values,
        missing_values=missing_values,
        missing_percentage=missing_percentage,
        total_files=total_files,
        total_lines=total_lines
    ))

    # Tabla de medias anuales combinadas
    print("\n========================================================")
    print("MEDIAS ANUALES DE PRECIPITACIÓN")
    print("========================================================")
    print("{:<10} {:<15}".format("Año", "Media (mm)"))
    print("-" * 25)
    for year, mean in combined_annual_means:
        print("{:<10} {:<15.2f}".format(year, mean))

# Ruta de la carpeta a analizar
carpeta = r'TA06/E01/precip.MIROC5.RCP60.2006-2100.SDSM_REJ'  # Asegúrate de que esta ruta sea correcta
process_folder_in_batches(carpeta)
