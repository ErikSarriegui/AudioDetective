![Robot](https://github.com/ErikSarriegui/ConversationDataMining/blob/main/imgs/stable-diffusion-turbo.jpeg)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ErikSarriegui/ConversationDataMining/blob/main/quickstart.ipynb)

# **Introducción**
Este proyecto tiene como objetivo la transcripción con etiquetado de interlocutores de audios y vídeos. Es una herramienta útil para reuniones, conferencias, entrevistas, etc.

# **Instalación**
Para poder utilizar este repositorio, primero deberá clonarlo.
``` bash
$ git clone https://github.com/ErikSarriegui/ConversationDataMining
```

Posteriormente debe instalar las dependencias necesaria.
``` bash
$ pip install -r requirements.txt
```
# **Quickstart**
## **1. Utilizando `web_ui.ipynb`**
Para poder probar el modelo sin necesidad de instalar nada de manera local, se puede utilizar el notebook `web_ui.ipynb`, que recibe como input una url a un vídeo de YouTube y transcribe el contenido de este, como si fueran mensajes de una conversación.

## **2. Utilizndo el pipeline**
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
