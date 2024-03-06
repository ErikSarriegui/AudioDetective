"""
Este script contiene un método que se utiliza para descargar
los audios de YouTube contenidos en una lista de urls de esta
plataforma.
"""
from pytube import YouTube

def downloadYouTubeAudios(
  url_list : list,
  output_dir : str = "/content/audio",
  filename_template: str = "audio{index}.mp3"
):
  """
  Es un método para descargar los audios de YouTube contenidos en
  una lista de urls de esta plataforma.

  Args:
  - url_list (list): Una lista que contiene los urls que queremos
  descargar.
  - output_dir (str): Es el directorio de salida en el que queremos
  almacenar los audios que hayamos descargado.
  """
  url_list_length = len(url_list)
  for index, url in enumerate(url_list):
    yt_url_object = YouTube(url)

    url_audio = yt_url_object.streams.filter(only_audio=True).first()

    url_audio.download(
      output_path = output_dir,
      filename = filename_template.format(index = index)
    )
    print(f"Descarga {index + 1}/{url_list_length} completa")

  print("¡Audios descargados exitosamente!")