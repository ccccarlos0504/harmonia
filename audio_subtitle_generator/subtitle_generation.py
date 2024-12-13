# audio_subtitle_generator/subtitle_generation.py


def generate_srt(segments, output_file="output.srt"):
    """
    生成 SRT 字幕文件。

    Args:
        segments (list): 一个包含匹配的文本片段、时间戳和文本起始索引的字典列表。
        output_file (str): 输出的 SRT 字幕文件名。
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments):
                #  生成字幕序号
                f.write(f"{i + 1}\n")
                # 生成字幕时间轴
                start_time = format_timestamp(segment["start_time"])
                end_time = format_timestamp(segment["end_time"])
                f.write(f"{start_time} --> {end_time}\n")
                # 生成字幕内容
                f.write(f"{segment['text']}\n\n")
        print(f"srt file generated at: {output_file}") # 输出字幕生成成功提示
    except Exception as e:
        print(f"Error generating SRT file: {e}") # 输出错误信息


def format_timestamp(seconds):
    """
    将时间戳（秒）转换为 SRT 格式的时间字符串。

    Args:
        seconds (float): 输入的时间戳（秒）。

    Returns:
        str: SRT 格式的时间字符串（例如 "00:00:05,000"）。
    """
    # 计算小时，分钟，秒和毫秒
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds_int = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds_int:02d},{milliseconds:03d}"


if __name__ == "__main__":
    # 测试代码：如果直接运行此模块，会执行以下代码
    segments = [
        {
            "text": "你好世界",
            "start_time": 0.12,
            "end_time": 0.7,
            "index_start": 0,
        },
        {
            "text": "今天天气",
            "start_time": 1.0,
            "end_time": 1.4,
            "index_start": 6,
        },
    ]
    generate_srt(segments) # 使用测试数据生成 SRT 字幕文件