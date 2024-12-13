# audio_subtitle_generator/main.py
import os
from dotenv import load_dotenv  # 导入 load_dotenv 函数，用于加载 .env 文件

from audio_subtitle_generator.audio_processing import (
    transcribe_audio,
    get_transcribed_segments,
    AudioConversionError,
    TranscriptionError,
)  # 导入音频处理模块中的函数
from audio_subtitle_generator.text_processing import (
    load_text,
    match_text_with_segments,
)  # 导入文本处理模块中的函数
from audio_subtitle_generator.subtitle_generation import (
    generate_srt,
)  # 导入字幕生成模块中的函数


load_dotenv()  # 读取 .env 文件中的环境变量


if __name__ == "__main__":
    # 设置音频和文本文件的路径
    audio_file = os.path.join("examples", "1.mp3")
    text_file = os.path.join("examples", "1.txt")
    output_srt_file = os.environ.get("OUTPUT_SUBTITLE_FILE", "output.srt")  # 从环境变量获取，默认为 "output.srt"
    max_edit_distance = int(os.environ.get("MAX_EDIT_DISTANCE", 5)) # 从环境变量获取， 默认为 5


    try:
        # 1. 语音识别
        segments = transcribe_audio(audio_file)  # 调用音频处理模块的语音识别函数
        if not segments:
             print("Audio transcription failed.")
             exit()  # 终止程序
        segments = get_transcribed_segments(segments)  # 获取语音识别结果中的文本和时间戳

        # 2. 加载文本
        text = load_text(text_file)  # 调用文本处理模块的加载文本函数

        # 3. 文本匹配
        matched_segments = match_text_with_segments(
            text, segments, max_distance = max_edit_distance
        )  # 调用文本处理模块的匹配函数，传入最大编辑距离

        # 4. 生成 SRT 字幕
        generate_srt(matched_segments, output_file = output_srt_file)  # 调用字幕生成模块的生成字幕函数， 传入输出文件名

    except (AudioConversionError, TranscriptionError) as e:
         print(f"An error occurred during audio processing: {e}")
    except Exception as e:
         print(f"An unexpected error occurred: {e}")