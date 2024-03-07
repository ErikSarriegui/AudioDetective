"""
Este script contiene los siguientes métodos:
    - downloadAndTranscriptAudio(): Este método combina todos los métodos de 
    los demás scripts para convertir un vídeo de una entrevista de YouTube en
    una transcripción distingiendo entre las personas.
    - transcriptAudio(): Este método hace lo mismo, pero, en vez de descargar
    los audios, supone que los tiene en un directorio.
"""

import AudioDownloader, AudioDiarization, AudioTranscription, utils

def transcriptAudio(
        hf_token: str,
        input_audios_dir: str,
        diarization_dir: str,
        transcriptions_output_dir: str,
        diarization_model_id : str = "pyannote/speaker-diarization-3.1",
        whisper_model_id : str = "openai/whisper-large-v3",
        delete_orginal_audio: bool = False,
        delete_diarization_audio: bool = True        
) -> None:
    """
    Este método utiliza los métodos de AudioDiarization, AudioTranscription y utils
    para transcribir los audios de un directorio.

    Args:
    - hf_token (str): Es el token de Huggingface, necesario para utilizar algunos
    modelos de diarización.
    - input_audios_dir (str): Es el directorio en el que se almacenan los audios
    - diarization_dir (str): Es el directorio en el que se almacenan los audios
    recortados tras la diarización.
    - transcriptions_output_dir (str): Es el directorio en el que se descargarán los
    archivos .csv con las transcripciones.
    - delete_orginal_audio (bool): Elimina (True) o no (False) los audios originales y
    el directorio en el que se encuentran.
    - delete_diarization_audio (bool): Elimina (True) o no (False) los audios diarizados
    y el directorio en el que se encuentran.

    Devuelve:
    - Nada, únicamente deja los .csv en el directorio especificado
    """
    AudioDiarization.multipleAudioDiarization(
        audios_dir = input_audios_dir,
        output_dir = diarization_dir,
        hf_token = hf_token,
        diarization_model_id = diarization_model_id
    )

    AudioTranscription.transcriptMultipleAudioPats(
        input_dir = diarization_dir,
        output_dir = transcriptions_output_dir,
        whisper_model_id = whisper_model_id
    )

    if delete_diarization_audio:
        utils.borrarDirectorio(diarization_dir)
    
    if delete_orginal_audio:
        utils.borrarDirectorio(input_audios_dir)    


def downloadAndTranscriptAudio(
        url_list : list,
        hf_token: str,
        downloaded_audios_dir: str,
        diarization_dir: str,
        transcriptions_output_dir: str,
        diarization_model_id : str = "pyannote/speaker-diarization-3.1",
        whisper_model_id : str = "openai/whisper-large-v3",
        delete_orginal_audio: bool = False,
        delete_diarization_audio: bool = True
) -> None:
    """
    Este método utiliza AudioDownloader para descargar el audio de YouTube y
    transcriptAudio para realizar la transcripción.
    
    Args:
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
    - Nada, únicamente deja los .csv en el directorio especificado
    """
    AudioDownloader.downloadYouTubeAudios(
        url_list = url_list,
        output_dir = downloaded_audios_dir
        # filename_template
    )

    AudioDownloader.preProcessAudios(
        audios_path = downloaded_audios_dir
    )

    transcriptAudio(
        hf_token = hf_token,
        input_audios_dir = downloaded_audios_dir,
        diarization_dir = diarization_dir,
        transcriptions_output_dir = transcriptions_output_dir,
        diarization_model_id = diarization_model_id,
        whisper_model_id = whisper_model_id,
        delete_orginal_audio = delete_orginal_audio,
        delete_diarization_audio = delete_diarization_audio
    )