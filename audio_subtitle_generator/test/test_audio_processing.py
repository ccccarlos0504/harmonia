# audio_subtitle_generator/test/test_audio_processing.py
import unittest  # 导入 unittest 模块，用于单元测试
import os
from audio_subtitle_generator.audio_processing import convert_audio_to_flac, transcribe_audio, get_transcribed_segments  # 导入被测试的函数


class TestAudioProcessing(unittest.TestCase):
    """测试音频处理模块"""

    def test_convert_audio_to_flac(self):
        """测试音频格式转换"""
        flac_file = convert_audio_to_flac("1.mp3")  # 调用音频转换函数
        self.assertTrue(flac_file.endswith(".flac"))  # 验证转换后的文件扩展名为 .flac
        self.assertTrue(os.path.exists(flac_file))
        os.remove(flac_file) # 删除创建的临时flac文件

    def test_transcribe_audio(self):
        """测试语音识别"""
        response = transcribe_audio("1.mp3")  # 调用语音识别函数
        self.assertIsNotNone(response)  # 验证返回结果不为空
        self.assertTrue(len(response.results)>0)  # 验证返回结果中含有语音识别的结果

    def test_get_transcribed_segments(self):
         """测试提取时间戳和文本"""
         response = transcribe_audio("1.mp3") # 调用语音识别函数
         if response:
            segments = get_transcribed_segments(response) # 获取语音识别结果中的文本和时间戳
            self.assertIsInstance(segments, list) # 验证返回值是一个list
            if len(segments)>0:
                 self.assertIsInstance(segments[0],dict) # 验证list元素是dict

if __name__ == "__main__":
    unittest.main()  # 运行所有测试