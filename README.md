# harmonia

这是一个用于音频转字幕的 Python 项目。

## 功能

*   使用 whisper 进行语音识别。
*   将识别结果与文本进行匹配。
*   生成 SRT 字幕文件。

## 安装

1.  创建虚拟环境: `python -m venv venv`
2.  激活虚拟环境:  `source venv/bin/activate` 或 `venv\Scripts\activate`
3.  安装依赖: `pip install -r requirements.txt`
4.  配置 `.env` 文件
5.  运行 `python main.py`