# audio_subtitle_generator/test/test_subtitle_generation.py
import unittest  # 导入 unittest 模块，用于单元测试
import os

from audio_subtitle_generator.subtitle_generation import (
    generate_srt,
    format_timestamp,
)  # 导入被测试的函数


class TestSubtitleGeneration(unittest.TestCase):
    """测试字幕生成模块"""
    def test_format_timestamp(self):
        """测试时间戳格式化"""
        timestamp = format_timestamp(123.456) # 调用时间戳格式化函数
        self.assertEqual(timestamp, "00:02:03,456") # 验证格式化后的时间字符串是否正确
        timestamp = format_timestamp(1.123) # 调用时间戳格式化函数
        self.assertEqual(timestamp, "00:00:01,123") # 验证格式化后的时间字符串是否正确
        timestamp = format_timestamp(3661.123) # 调用时间戳格式化函数
        self.assertEqual(timestamp, "01:01:01,123") # 验证格式化后的时间字符串是否正确

    def test_generate_srt(self):
        """测试字幕文件生成"""
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
        generate_srt(segments, "test_output.srt") # 调用字幕生成函数
        self.assertTrue(os.path.exists("test_output.srt")) # 验证字幕文件是否生成
        with open("test_output.srt","r", encoding="utf-8") as f:
             content = f.read()
             self.assertTrue("1\n00:00:00,120 --> 00:00:00,700\n你好世界\n\n2\n00:00:01,000 --> 00:00:01,400\n今天天气\n\n" == content)
        os.remove("test_output.srt") # 删除测试生成的字幕文件

if __name__ == "__main__":
    unittest.main()  # 运行所有测试