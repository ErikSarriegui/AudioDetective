"""
Este script se encarga de transcribir archivos de audio a csv manteniendo el taggeo de las personas. Lo hace en dos pasos:
  - transcriptSingleAudioParts: Esta función recibe la ruta de un directorio de archivos de audio, los transcribe y lo guarda en un directorio.
  - transcriptMultipleAudioPats: Esta función utiliza la función anterior para procesar todos los directorios con sus correspondientes archivos
  mp3 para guardar sus transcripciones.

"""

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import pandas as pd
import numpy as np
import os

def transcriptSingleAudioParts(
    audios_dir: str,
    output_dir: str,
    whisper_pipeline: pipeline
) -> None:
  """
  Este es un método que transcribe los audios divididos de un directorio y 
  registra el texto en un .csv, manteniendo del orden de la conversación.

  Args:
  - audios_dir (str): Es el directorio en el que se encuentran los audios
  a transcribir. 
  - output_dir (str): Es la dirección donde se dejarán los .csv
  - whisper_pipeline (transformers.pipeline): Es el objeto que hace las
  inferencias sobre los audios.

  Devuelve:
  - Nada, únicamente deja los .csv en la ubicación especificada
  """
  mp3_files = sorted([f"{audios_dir}/{file}" for file in os.listdir(audios_dir) if file.endswith('.mp3')])
  transcripted_audios_json = whisper_pipeline(mp3_files)

  processed_transcripted_list = []
  for person_dialogue in transcripted_audios_json:
    processed_transcripted_list.append(person_dialogue["text"])

  structured_df_data = np.array([["Unknown" for dummy_element in range(len(processed_transcripted_list))], processed_transcripted_list]).T
  transcripted_data_df = pd.DataFrame(structured_df_data, columns = ["Speaker", "Text"])

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  transcripted_data_df.to_csv(f"{output_dir}/{ os.path.basename(audios_dir)}.csv")



def transcriptMultipleAudioPats(
    input_dir: str,
    output_dir: str,
    whisper_model_id: str = "openai/whisper-large-v3",
    device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
) -> None:
  """
  Este es un médodo que utiliza el método transcriptSingleAudioParts() para
  realizar la inferencia y la transcripción de más de un conjunto de audios.
  Es decir, transcribe todos los audios que hay dentro de un conjunto de carpetas:
      
    data
    ├── entrevista_1
    │   ├── audio_1
    │   ├── audio_2
    │   └── ...
    └── entrevista_2
        ├── audio_1
        ├── audio_2
        └── ...
  
  Args:
  - input_dir (str): Es el directorio general, dentro de este se encuentras los
  directorios que hacen referencia a cada grabación con sus audios dentro. Sería
  "data" en el caso de la representación de arriba
  - output_dir (str): Es el directorio donde se dejarán los .csv
  - whisper_model_id (str): Es el id de Hugginface del modelo de whisper que queremos utilizar
  para realizar la inferencia.
  - device (torch.device): Es el dispositivo en el que queremos que se haga la inferencia
  - torch_dtype: Es el tipo de dato que vamos a utilizar en la inferencia.

  Devuelve:
  - Nada, al igual que transcriptSingleAudioParts() deja los .csv en el directorio 
  especificado.
  """
  model = AutoModelForSpeechSeq2Seq.from_pretrained(
      whisper_model_id, torch_dtype=torch_dtype, use_safetensors=True
  ).to(device)

  processor = AutoProcessor.from_pretrained(whisper_model_id)

  model_pipeline = pipeline(
      "automatic-speech-recognition",
      model=model,
      tokenizer=processor.tokenizer,
      feature_extractor=processor.feature_extractor,
      torch_dtype=torch_dtype,
      device=device,
  )

  for audios_directory in os.listdir(input_dir):
    full_audios_path_path = os.path.join(input_dir, audios_directory)

    if os.path.isdir(full_audios_path_path) and not os.path.isfile(full_audios_path_path):
      transcriptSingleAudioParts(
          audios_dir = full_audios_path_path,
          output_dir = output_dir,
          whisper_pipeline = model_pipeline
      )
