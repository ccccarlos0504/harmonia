# audio_subtitle_generator/test/test_text_processing.py
import unittest  # 导入 unittest 模块，用于单元测试
from audio_subtitle_generator.text_processing import (
    load_text,
    preprocess_text,
    match_text_with_segments,
)  # 导入被测试的函数


class TestTextProcessing(unittest.TestCase):
    """测试文本处理模块"""

    def test_load_text(self):
        """测试加载文本文件"""
        text = load_text("1.txt")  # 调用加载文本函数
        self.assertIsInstance(text, str)  # 验证返回结果是字符串类型
        self.assertTrue(len(text) > 0) # 验证返回结果不为空

    def test_preprocess_text(self):
         """测试文本预处理函数"""
         test_text = "你好！，世界？123"
         processed_text = preprocess_text(test_text)
         self.assertEqual(processed_text, "你好世界123") # 验证去除标点，并转换为小写

    def test_match_text_with_segments(self):
        """测试文本匹配"""
        text = "你好世界今天天气"  # 测试文本
        segments = [
            {"text": "你好", "start_time": 0.12, "end_time": 0.42},
            {"text": "世界", "start_time": 0.5, "end_time": 0.7},
            {"text": "今天", "start_time": 1.0, "end_time": 1.2},
            {"text": "天气", "start_time": 1.2, "end_time": 1.4},
        ]
        matched_segments = match_text_with_segments(
            text, segments, max_distance=5
        )  # 调用文本匹配函数
        self.assertIsInstance(matched_segments, list) # 验证返回结果为list类型
        self.assertTrue(len(matched_segments) == 2) # 验证匹配结果数量为2个
        self.assertEqual(matched_segments[0]["text"],"你好世界") # 验证匹配的文本是否正确
        self.assertEqual(matched_segments[1]["text"], "今天天气") # 验证匹配的文本是否正确
if __name__ == "__main__":
    unittest.main()  # 运行所有测试