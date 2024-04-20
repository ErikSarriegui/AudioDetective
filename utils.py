"""
Este script tiene varias funciones complementarias.
"""
import os
import pandas as pd



def borrarDirectorio(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)
    print(f"Directorio {path} eliminado correctamente.")



def csv_to_text(
    csv_dir : str
) -> str:
  """
  Esta función transforma el output del .csv en un string que
  se pueda visualizar en gradio.

  Args:
    dir : Es el directorio en el que encontramos el .csv

  Devuelve:
    El .csv en forma de string de la siguiente manera:
        {Speaker 1}: {Texto}

        {Speaker 2}: {Texto}
  """

  csv_path = f"{csv_dir}/{os.listdir(csv_dir)[-1]}"

  conversation_df = pd.DataFrame(
      pd.read_csv(csv_path, encoding = "utf8")
  )

  output_text = ""
  for index, row in conversation_df.iterrows():
      output_text += f"{row['Speaker']}: {row['Text']}\n\n"
  return output_text