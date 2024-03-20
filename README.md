![Robot](https://github.com/ErikSarriegui/ConversationDataMining/blob/main/imgs/stable-diffusion-turbo.jpeg)

# **Introducción**
Este proyecto tiene como objetivo la transcripción con etiquetado de interlocutores de audios y vídeos. Es una herramienta útil para reuniones, conferencias, entrevistas, etc. Sin embargo, en OpenPsy se va a utilizar para extraer conversaciones entre pacientes y psicólogos que pueden encontrarse en audio o vídeo.

# **Instalación**
Para poder utilizar este repositorio, primero deberá clonarlo.
``` bash
$ git clone https://github.com/ErikSarriegui/ConversationDataMining
```

Posteriormente debe instalar las dependencias necesaria.
``` bash
$ pip install -r requirements.txt
```

# **QuickStart**
Puede utilizar el código mediante el método `downloadAndTranscriptAudio()` de `data_engine.py`. Este método utiliza `AudioDownloader` para descargar el audio de YouTube y
`transcriptAudio` para realizar la transcripción.

Argumentos de entrada:
- url_list (list): Una lista con los urls de los audios a descargar de
YouTube.
- hf_token (str): Es el token de Huggingface, necesario para utilizar algunos
modelos de diarización.
- downloaded_audios_dir (str): Es el directorio en el que se almacenarán
los audios que se descargen de YouTube.
- diarization_dir (str): Es el directorio en el que se almacenan los audios
recortados tras la diarización.
- transcriptions_output_dir (str): Es el directorio en el que se descargarán los
archivos .csv con las transcripciones.
- delete_orginal_audio (bool): Elimina (True) o no (False) los audios originales y
el directorio en el que se encuentran.
- delete_diarization_audio (bool): Elimina (True) o no (False) los audios diarizados
y el directorio en el que se encuentran.

Devuelve:
- Un archivo `.csv` con la trascripción del audio en el directorio especificado.