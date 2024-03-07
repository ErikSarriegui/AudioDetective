"""
Este script se encarga de dividir archivos de audio en segmentos según la persona que esté hablando. Lo hace empleando los siguiente métodos:
  - cleanDf: Modifica el df que se crea con el output del pipeline para que cumpla los requesitos necesarios antes de dividir el audio.
  - singleAudioDivider: Esta función recibe la ruta de un archivo de audio y la separa en segmentos según el speaker que se detecte en cada momento.
  - multipleAudioDivider: Esta función utiliza la función anterior para procesar todos los archivos mp3 que se encuentren dentro de un directorio.
En resumen, el script permite separar automáticamente audios con varias personas hablando en archivos individuales para cada participante de la conversación.
"""

from pyannote.audio import Pipeline
from pydub import AudioSegment

import torch
import pandas as pd
import os

def cleanDf(df : pd.DataFrame) -> pd.DataFrame:
  """
  Es un método que limpia el DataFrame que contiene los datos
  de diarización realizando las siguientes operaciones:
    1. Calcula una columna con la duración del apartado en
    el que está hablando una persona y se queda con los
    apartados de más de un 1.3 segundos de duración.
    2. Combina las partes consecutivas en las que habla un
    mismo speaker. La diarización registra los momentos en
    los que habla cada uno, pero, si hay silencios tras los
    que habla la misma persona los divide, aquí los juntamos
    para operar con el menos número de audios posibles.
  
  Args:
  - df (pd.DataFrame): Es el DataFrame sobre el que realizar
  los cambios

  Devuelve:
  - pd.DataFrame: Con los cambios realizados
  """
  df['duration'] = df['end_time'] - df['start_time']
  df = df[df['duration'] >= 1.3]

  unified_speakers_data = {
      'start_time': [],
      'end_time': [],
      'label': []
  }

  current_speaker = None
  current_start_time = None

  for _, row in df.iterrows():
      if row['label'] != current_speaker:
          if current_speaker is not None:
              unified_speakers_data['start_time'].append(current_start_time)
              unified_speakers_data['end_time'].append(previous_end_time)
              unified_speakers_data['label'].append(current_speaker)

          current_speaker = row['label']
          current_start_time = row['start_time']

      previous_end_time = row['end_time']

  unified_speakers_data['start_time'].append(current_start_time)
  unified_speakers_data['end_time'].append(previous_end_time)
  unified_speakers_data['label'].append(current_speaker)

  return pd.DataFrame(unified_speakers_data)

def singleAudioDiarization(
    audio_path: str,
    output_dir: str,
    pipeline: Pipeline,
) -> None:
  """
  Es un método que recibe como input el path de un audio, y lo divide en los
  momentos en los que hablan los diferentes "speakers".

  Args:
  - audio_path (str): Es la ruta al audio que se quiere dividir
  - output_dir (str): Es el directorio en el que se quieren los audios cortados
  - device (torch.device): Es el dispositivo en el que se va a ejecutar la IA
  - pipeline (pyannote.audio.Pipeline): Es la propia IA de diarización

  Devuelve:
  - Nada, deja los audios divididos en el directorio especificado
  """
  diarization = pipeline(audio_path)

  # Diarization to df
  diarization_data_list = []
  for segment, track_id, speaker_label in diarization.itertracks(yield_label=True):
    diarization_data_list.append({
        "start_time": segment.start,
        "end_time": segment.end,
        "track_id": track_id,
        "label": speaker_label
    })


  cleaned_diarization_df = cleanDf(pd.DataFrame(diarization_data_list))

  audio = AudioSegment.from_mp3(audio_path)
  audio_name = os.path.basename(audio_path)[:-4] # -4 por el .mp3

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  if not os.path.exists(f"{output_dir}/{audio_name}"):
    os.makedirs(f"{output_dir}/{audio_name}")

  for index, (_, row) in enumerate(cleaned_diarization_df.iterrows()):
      spearker_talking_start = int(row['start_time']) * 1000
      spearker_talking_end= int(row['end_time']) * 1000

      cutted_audio = audio[spearker_talking_start : spearker_talking_end]

      cutted_audio.export(f"{output_dir}/{audio_name}/{index}.mp3", format="mp3")

  return cleaned_diarization_df



def multipleAudioDiarization(
    audios_dir: str,
    output_dir: str,
    hf_token: str,
    diarization_model_id: str = "pyannote/speaker-diarization-3.1",
    device : torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
) -> None:
  """
  Utiliza el método singleAudioDiarization para dividir todos los audios según el
  spreaker de un directorio.

  Args:
  - audios_dir (str): Es el directorio en el que encontramos todos los .mp3 que
  queremos dividir.
  - output_dir (str): Es el directorio en el que vamos a dejar los audios cortados.
  Se creará una carpeta con el nombre del audio y dentro todos los audios
  divididos y en orden.
  - hf_token: Es necesario para poder utilizar el modelo por defecto.
  - diarization_model_id: El id en Huggingface del modelo que queremos utilizar,
  en nuestro caso (y por defecto) es "pyannote/speaker-diarization-3.1".
  - device (torch.device): Es el dispositivo en el que se va a ejecutar la inferencia.
  - pipeline (pyannote.audio.Pipeline): Es la propia IA de diarización

  Devuelve:
  -  Nada, deja los audios divididos en sus correspondientes directorios,
  dentro del output_dir especificado

  Ejemplo de uso:
  """

  diarization_pipeline = Pipeline.from_pretrained(
    diarization_model_id,
    use_auth_token = hf_token
  )

  print(f"[INFO] You are currently running on: {device.type.upper()}"  + (" || enable CUDA to go brrr" if device.type == "cpu" else ""))
  mp3_files = [file for file in os.listdir(audios_dir) if file.endswith('.mp3')]

  for audio_file in mp3_files:
    singleAudioDiarization(
        audio_path = f"{audios_dir}/{audio_file}",
        output_dir = output_dir,
        pipeline = diarization_pipeline.to(device)
    )
