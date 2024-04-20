![Robot](https://github.com/ErikSarriegui/ConversationDataMining/blob/main/repo_assets/stable-diffusion-turbo.jpeg)

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
Para poder probar el modelo sin necesidad de instalar nada de manera local, se puede utilizar el notebook `quickstart.ipynb`, que recibe como input una url a un vídeo de YouTube y transcribe el contenido de este, como si fueran mensajes de una conversación.

Para hacer esto...
  1. Abre el notebook [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ErikSarriegui/ConversationDataMining/blob/main/quickstart.ipynb)
  2. Si no estas en colab, comenta las primeras líneas de código e instala dependencias manualmente.
  3. Implementa tu token de huggingface ([puedes conseguirlo aquí]([url](https://huggingface.co/settings/tokens))).

Hay que tener en cuenta:
  * Que la primera inferencia es lenta debido a que es necesario instalar todas las dependencias.
  * Que para acelerar el proceso de forma radical, es recomendable utilizar CUDA.
  * Por motivos que desconozco, una vez se han instalado las dependecias de `requirements.txt` salta un error, para solucionar esto, ejecuta el código de nuevo una o dos veces rápidamente.

# **Tutorial**
Si quieres tener más control, puedes implementar directamente los métodos que se utilizan en `quickstart.ipynb`. El principal método es `downloadAndTranscriptAudio()` de `pipeline.py`. Este método utiliza `AudioDownloader` para descargar el audio de YouTube y
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
