import os
import speech_recognition as sr

# Ruta de la carpeta con archivos WAV
carpeta_wav = r'C:\Users\Hir\Desktop\locutor'

# Ruta del archivo de texto para las transcripciones
archivo_transcripciones = r'C:\Users\Hir\Desktop\transcripciones.txt'

# Inicializar reconocedor
recognizer = sr.Recognizer()

# Función para transcribir archivos WAV y escribir las transcripciones en el archivo de texto
def transcribir_y_escribir():
    # Obtener la lista de archivos WAV y ordenarlos
    archivos_wav = sorted([f for f in os.listdir(carpeta_wav) if f.endswith('.wav')], key=lambda x: int(x.split('.')[0]))
    
    with open(archivo_transcripciones, 'w') as f:
        for archivo in archivos_wav:
            ruta_wav = os.path.join(carpeta_wav, archivo)
            with sr.AudioFile(ruta_wav) as source:
                audio_data = recognizer.record(source)  # Leer el archivo de audio
                try:
                    texto_transcrito = recognizer.recognize_google(audio_data, language='es-ES')  # Transcribir audio a texto
                    f.write(f"wavs/{archivo}|{texto_transcrito}\n")  # Escribir transcripción en el archivo de texto
                    print(f"Transcripción de {archivo} completada.")
                except sr.UnknownValueError:
                    print(f"No se pudo transcribir {archivo}. Audio no reconocido.")
                except sr.RequestError as e:
                    print(f"No se pudo completar la solicitud para {archivo}; {e}")

# Transcribir archivos y escribir transcripciones en el archivo de texto
transcribir_y_escribir()
