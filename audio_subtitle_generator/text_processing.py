# audio_subtitle_generator/text_processing.py
import re  # 导入 re 模块，用于正则表达式
from Levenshtein import distance  # 导入 Levenshtein 距离算法
import os

def load_text(text_file):
    """
    加载文本文件，并进行预处理。

    Args:
        text_file (str): 输入的文本文件路径。

    Returns:
        str: 预处理后的文本内容。
"""
    try:
        encodings = ["utf-8", "gbk", "gb2312"]  # 尝试多种编码
        for encoding in encodings:
            try:
                with open(text_file, "r", encoding=encoding) as f:
                    print(f"Successfully loaded text file with encoding: {encoding}")
                    text = f.read()  # 读取文本文件内容
                    return preprocess_text(text)  # 对文本进行预处理
            except UnicodeDecodeError:
                continue # 如果使用此编码无法读取，则尝试下一种编码
        else:
            print(f"Error: Unable to decode text file using utf-8, gbk, or gb2312 encoding.")
            return ""
    except Exception as e:
        print(f"Error loading text file: {e}")
        return ""  # 如果发生错误，返回空字符串

def preprocess_text(text):
    """
        文本预处理，去除标点符号、发言者标识、和换行符，并将文本转换为小写。

    Args:
        text (str): 输入的文本内容。

    Returns:
        str: 预处理后的文本内容。
    """
# 使用正则表达式去除所有非字母和数字字符，发言者标识和换行符
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"^[A-Z]:\s*", "", text, flags=re.MULTILINE)  #去除发言者标识
    text = text.replace("\n", " ") # 将换行符替换为空格
    return text.lower()  # 将文本转换为小写


def match_text_with_segments(text, segments, max_distance=15): # 修改默认的最大编辑距离为 15
    """
    将文本与语音识别结果进行匹配。

    Args:
        text (str): 预处理后的文本内容。
        segments (list): 一个包含文本和时间戳的字典列表。
        max_distance (int): 最大编辑距离。

    Returns:
        list: 一个包含匹配的文本片段、时间戳和文本起始索引的字典列表。
    例如：
        [
            {
                'text': '你好世界',
                'start_time': 0.12,
                'end_time': 0.7,
            'index_start': 0
            },
            {
            'text': '今天天气',
            'start_time': 1.0,
            'end_time': 1.4,
                'index_start': 6
            }
        ]
    """
    matched_segments = []  # 初始化匹配的片段列表
    text_index = 0  # 初始化文本索引
    for i in range(len(segments)):
        segment = segments[i]  # 获取当前的语音识别片段
        text_index_start = text_index # 记录匹配的片段在文本中开始的索引
        # 遍历文本，查找与当前语音识别片段匹配的文本
        while text_index < len(text):
            # 计算当前文本片段和语音识别片段的编辑距离
            text_segment = text[text_index: ] # 获取当前文本片段到末尾
            words = segment['text'].split() # 分割单词
            matched_text = ""
            matched = False
            for word in words:
                start_index = text_segment.find(word) #查找单词在文本中的位置
                if start_index == -1:
                    break # 没有找到则跳过
                else:
                    matched_text += text_segment[:start_index + len(word)] # 将匹配的单词加入匹配结果中
                    text_segment = text_segment[start_index + len(word):] # 更新文本片段
                    matched = True
        if matched:
            edit_distance = distance(segment['text'], matched_text)
            print(f"Comparing '{segment['text']}' with '{matched_text}', edit_distance: {edit_distance}")  # 加入调试信息

            if edit_distance <= max_distance:
                matched_segments.append({
                    "text": text[text_index_start: text_index_start + len(matched_text)],  # 匹配的文本
                    "start_time": segment["start_time"],  # 匹配的语音片段的开始时间
                        "end_time": segment["end_time"],  # 匹配的语音片段的结束时间
                        "index_start": text_index_start  # 匹配的文本在原文本的起始索引
                })
                text_index += len(matched_text) #更新文本索引
                break

        else:
            text_index += 1  # 更新文本索引

    return matched_segments

if __name__ == "__main__":
    # 测试代码：如果直接运行此模块，会执行以下代码
    text = load_text("examples/1.txt")  # 加载文本文件 "1.txt"
# 测试用的文本识别结果
    segments = [
    {"text": "hello", "start_time": 0.12, "end_time": 0.42},
    {"text": "my", "start_time": 0.5, "end_time": 0.7},
    {"text": "name", "start_time": 1.0, "end_time": 1.2},
    {"text": "is", "start_time": 1.2, "end_time": 1.4},
    ]
    match_segments = match_text_with_segments(text, segments)  # 进行文本匹配
    for segment in match_segments:
        print(segment)  # 打印匹配的片段