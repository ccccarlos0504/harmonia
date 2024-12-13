# audio_subtitle_generator/audio_processing.py
import os  # 导入 os 模块，用于处理文件路径

import whisper
from pydub import AudioSegment  # 导入 pydub 库，用于音频处理


class AudioConversionError(Exception):
    """自定义音频转换错误"""
    pass


class TranscriptionError(Exception):
    """自定义转录错误"""
    pass


def convert_audio_to_wav(audio_file):
    """
    将音频文件转换为单声道, 16000Hz 采样率的 WAV 格式，以供 whisper 使用。
     Args:
        audio_file (str): 输入的音频文件路径。
     Returns:
         str: 转换后的 WAV 文件路径。
     Raises:
         AudioConversionError: 如果音频转换过程中发生错误，抛出此异常。
    """
    try:
        # 使用 pydub 加载音频文件
        sound = AudioSegment.from_file(audio_file)
        # 设置为单声道
        sound = sound.set_channels(1)
        # 设置采样率为 16000 Hz
        sound = sound.set_frame_rate(16000)
        # 构造 WAV 文件名（将原文件扩展名替换为 .wav）
        wav_file = audio_file.replace(os.path.splitext(audio_file)[1], ".wav")
        # 导出为 WAV 格式
        sound.export(wav_file, format="wav")

        return wav_file
    except Exception as e:
        raise AudioConversionError(f"Error during audio conversion: {e}") from e


def transcribe_audio(audio_file):
    """使用 whisper 模型进行语音识别。

    Args:
        audio_file (str): 输入的音频文件路径。

    Returns:
        list: 一个包含文本和时间戳的字典列表。
            例如：
               [
                {'start_time': 0.0, 'end_time': 3.16, 'text': '今天天气真不错'},
                {'start_time': 3.16, 'end_time': 6.0, 'text': '我们一起出去玩吧'}
               ]
      Raises:
           TranscriptionError: 如果转录过程中发生错误，抛出此异常。
    """
    try:
        wav_file = convert_audio_to_wav(audio_file)  # 转换为wav格式
        if not wav_file:
            return None
        model = whisper.load_model("base")  # 加载模型
        result = model.transcribe(wav_file)  # 进行语音识别
        segments = []
        for segment in result['segments']:
            segments.append(
                {
                    "text": segment['text'],  # 提取文本
                    "start_time": segment['start'],  # 提取开始时间
                    "end_time": segment['end']  # 提取结束时间
                }
            )
        os.remove(wav_file)  # 删除临时文件
        return segments
    except Exception as e:
        raise TranscriptionError(f"Error during transcription with whisper: {e}") from e


def get_transcribed_segments(segments):
    """
       提取转录结果中的文本和时间戳，whisper可以直接返回结果，不需要额外的处理
      Args:
        segments (list): whisper返回的识别结果
      Returns:
       list: 一个包含文本和时间戳的字典列表。
         例如：
             [
              {'start_time': 0.0, 'end_time': 3.16, 'text': '今天天气真不错'},
               {'start_time': 3.16, 'end_time': 6.0, 'text': '我们一起出去玩吧'}
              ]
      """
    return segments


if __name__ == "__main__":
    # 测试代码：如果直接运行此模块，会执行以下代码
    try:
        # 使用whisper api
        segments = transcribe_audio("examples/1.mp3")
        if segments:
            print("Transcribed with whisper API:")
            for segment in segments:
                print(segment)

    except (AudioConversionError, TranscriptionError) as e:
        print(f"An error occurred during audio processing: {e}")
