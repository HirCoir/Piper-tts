import os

# Ruta de la carpeta
carpeta = r'C:\Users\Hir\Desktop\locutor'

# Función para eliminar archivos de 0 bytes
def eliminar_archivos_cero_bytes():
    archivos = os.listdir(carpeta)
    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta, archivo)
        if os.path.isfile(ruta_archivo) and os.path.getsize(ruta_archivo) == 0:
            os.remove(ruta_archivo)
            print(f"Archivo {archivo} eliminado porque tiene 0 bytes")

# Función para ordenar archivos restantes y renombrarlos
def ordenar_y_renombrar_archivos():
    archivos = os.listdir(carpeta)
    archivos = sorted([f for f in archivos if f.endswith('.wav')])  # Filtrar solo archivos .ogg y ordenarlos
    for indice, archivo in enumerate(archivos, start=1):
        nuevo_nombre = f"{indice}.wav"  # Nuevo nombre con formato fileX.ogg
        os.rename(os.path.join(carpeta, archivo), os.path.join(carpeta, nuevo_nombre))
        print(f"Archivo {archivo} renombrado como {nuevo_nombre}")

# Eliminar archivos de 0 bytes
eliminar_archivos_cero_bytes()

# Ordenar y renombrar archivos restantes
ordenar_y_renombrar_archivos()
