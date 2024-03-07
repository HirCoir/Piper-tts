import os
import shutil
import speech_recognition as sr
from tqdm import tqdm  # Importar tqdm para la barra de progreso
from tkinter import Tk, filedialog, Button, Label, messagebox

# Función para eliminar archivos de 0 bytes
def eliminar_archivos_cero_bytes(carpeta):
    archivos = os.listdir(carpeta)
    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta, archivo)
        if os.path.isfile(ruta_archivo) and os.path.getsize(ruta_archivo) == 0:
            os.remove(ruta_archivo)
            print(f"Archivo {archivo} eliminado porque tiene 0 bytes")

# Función para ordenar archivos restantes y renombrarlos
def ordenar_y_renombrar_archivos(carpeta):
    archivos = os.listdir(carpeta)
    archivos = sorted([f for f in archivos if f.endswith('.wav')])  # Filtrar solo archivos .wav y ordenarlos
    for indice, archivo in enumerate(archivos, start=1):
        nuevo_nombre = f"{indice}.wav"  # Nuevo nombre con formato fileX.wav
        os.rename(os.path.join(carpeta, archivo), os.path.join(carpeta, nuevo_nombre))
        print(f"Archivo {archivo} renombrado como {nuevo_nombre}")

# Función para transcribir archivos WAV y escribir las transcripciones en un archivo CSV
def transcribir_y_escribir(carpeta_wav, archivo_transcripciones):
    # Inicializar reconocedor
    recognizer = sr.Recognizer()

    # Obtener la lista de archivos WAV y ordenarlos
    archivos_wav = sorted([f for f in os.listdir(carpeta_wav) if f.endswith('.wav')], key=lambda x: int(x.split('.')[0]))

    with open(archivo_transcripciones, 'w', encoding='utf-8-sig') as f:
        for archivo in tqdm(archivos_wav, desc="Transcribiendo", unit="archivo"):
            ruta_wav = os.path.join(carpeta_wav, archivo)
            with sr.AudioFile(ruta_wav) as source:
                audio_data = recognizer.record(source)  # Leer el archivo de audio
                try:
                    texto_transcrito = recognizer.recognize_google(audio_data, language='es-ES')  # Transcribir audio a texto
                    f.write(f"{archivo}|{texto_transcrito}\n")  # Escribir transcripción en el archivo de texto
                except sr.UnknownValueError:
                    pass  # Puedes manejar esto según tus necesidades
                except sr.RequestError as e:
                    print(f"No se pudo completar la solicitud para {archivo}; {e}")

# Función para que el usuario seleccione la ubicación donde guardar el archivo de transcripciones
def seleccionar_ubicacion_guardado():
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter

    # Mostrar el cuadro de diálogo para seleccionar la ubicación de guardado
    ubicacion_guardado = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")], title="Guardar transcripciones como")

    return ubicacion_guardado

# Función para mostrar los créditos
def mostrar_creditos():
    messagebox.showinfo("Créditos", "Este código fue desarrollado por Min.")

# Mensaje inicial
print("Bienvenido al terminal de gestión de archivos de audio.")

# Mostrar opciones al usuario
while True:
    print("\nSeleccione la opción que desee:")
    print("1. Renombrar archivos WAV en una carpeta.")
    print("2. Transcribir archivos WAV en una carpeta.")
    print("3. Salir.")
    
    opcion = input("Ingrese el número de la opción que desea realizar: ")

    if opcion == '1':
        print("\nRENOMBRAR ARCHIVOS WAV\n")
        carpeta = filedialog.askdirectory(title="Selecciona una carpeta")
        eliminar_archivos_cero_bytes(carpeta)
        ordenar_y_renombrar_archivos(carpeta)
        print("¡Proceso completado!")

    elif opcion == '2':
        print("\nTRANSCRIBIR ARCHIVOS WAV\n")
        carpeta_wav = filedialog.askdirectory(title="Selecciona una carpeta")
        archivo_transcripciones = "transcript.csv"  # Nombre predeterminado del archivo de transcripciones

        transcribir_y_escribir(carpeta_wav, archivo_transcripciones)
        print("¡Proceso completado!")

        # Preguntar al usuario si desea seleccionar una ubicación diferente para guardar las transcripciones
        respuesta = messagebox.askyesno("Guardar transcripciones", "¿Desea seleccionar una ubicación diferente para guardar las transcripciones?")
        
        if respuesta:
            ubicacion_guardado = seleccionar_ubicacion_guardado()

            # Mover o copiar el archivo de transcripciones a la ubicación seleccionada
            if ubicacion_guardado:
                try:
                    shutil.move(archivo_transcripciones, ubicacion_guardado)
                    print(f"Archivo de transcripciones guardado en: {ubicacion_guardado}")
                except Exception as e:
                    print(f"Error al mover el archivo: {e}")
            else:
                print("No se seleccionó una ubicación válida. El archivo de transcripciones se encuentra en el directorio actual.")

    elif opcion == '3':
        print("Saliendo. ¡Hasta luego!")
        break

    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
