"""硅基流动TTS组件常量定义"""

DOMAIN = "siliconflow_tts"
DEFAULT_NAME = "SiliconFlow TTS"

# API配置
API_BASE_URL = "https://api.siliconflow.cn/v1"
API_ENDPOINT = f"{API_BASE_URL}/audio/speech"

# 默认配置
DEFAULT_MODEL = "FunAudioLLM/CosyVoice2-0.5B"
DEFAULT_VOICE = "speech:Dahu-HA-Ari:qc10fwc040:jxlvonagnnzdvbotrmrr"
DEFAULT_RESPONSE_FORMAT = "mp3"
DEFAULT_SAMPLE_RATE = 44100  # 更高的采样率，减少切断问题
DEFAULT_SPEED = 1.0  # 正常语速，避免因语速过快导致切断
DEFAULT_GAIN = -2  # 稍微降低增益，避免音频削峰导致的切断
DEFAULT_STREAM = False  # 不使用流式传输，确保最快响应

# 支持的音频格式
SUPPORTED_FORMATS = ["mp3", "wav", "opus", "pcm"]

# 支持的采样率
SUPPORTED_SAMPLE_RATES = {
    "opus": [48000],
    "wav": [8000, 16000, 24000, 32000, 44100],
    "pcm": [8000, 16000, 24000, 32000, 44100],
    "mp3": [32000, 44100]
}

# 速度范围
MIN_SPEED = 0.25
MAX_SPEED = 4.0

# 增益范围
MIN_GAIN = -10
MAX_GAIN = 10

# 默认音色选项（内置）
DEFAULT_VOICE_OPTIONS = {
    "speech:Dahu-HA-Ari:qc10fwc040:jxlvonagnnzdvbotrmrr": "阿狸",
    "speech:Dahu-HA-Lulu:qc10fwc040:ugmvnfqyesexvqjuneyf": "露露",
    "speech:Dahu-HA-Soraka:qc10fwc040:ezxwqvmnazypoekujait": "索拉卡",
    "speech:Dahu-HA-Zac:qc10fwc040:smplyqhoxcxwepjavhci": "扎克"
}

# 全局变量存储合并后的音色选项（默认 + 用户自定义）
_VOICE_OPTIONS = DEFAULT_VOICE_OPTIONS.copy()

def get_voice_options():
    """获取当前可用的所有音色选项（默认 + 用户自定义）"""
    return _VOICE_OPTIONS.copy()

def update_voice_options(custom_voices: dict):
    """更新音色选项，将用户自定义音色与默认音色合并"""
    global _VOICE_OPTIONS
    _VOICE_OPTIONS = DEFAULT_VOICE_OPTIONS.copy()
    if custom_voices:
        _VOICE_OPTIONS.update(custom_voices)

# configuration.yaml 配置键名
CONF_CUSTOM_VOICES = "custom_voices"

# 配置选项的键名
CONF_VOICE = "voice"
CONF_SPEED = "speed"
CONF_SAMPLE_RATE = "sample_rate"
CONF_RESPONSE_FORMAT = "response_format"
CONF_GAIN = "gain" 