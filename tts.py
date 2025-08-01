"""硅基流动TTS组件"""
import asyncio
import logging
import aiohttp
import async_timeout
import base64
import os
from typing import Any

from homeassistant.components.tts import (
    TextToSpeechEntity,
    Voice,
    TtsAudioType,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    API_ENDPOINT,
    DEFAULT_MODEL,
    DEFAULT_VOICE,
    DEFAULT_RESPONSE_FORMAT,
    DEFAULT_SAMPLE_RATE,
    DEFAULT_SPEED,
    DEFAULT_GAIN,
    DEFAULT_STREAM,
    SUPPORTED_FORMATS,
    MIN_SPEED,
    MAX_SPEED,
    MIN_GAIN,
    MAX_GAIN,
    get_voice_options,
    CONF_VOICE,
    CONF_SPEED,
    CONF_SAMPLE_RATE,
    CONF_RESPONSE_FORMAT,
    CONF_GAIN,
)

_LOGGER = logging.getLogger(__name__)

# 支持的语音列表（根据CosyVoice2-0.5B模型的实际语音）
SUPPORTED_VOICES = {
    "zh": [
        Voice("speech:Dahu-HA-Lulu:qc10fwc040:ugmvnfqyesexvqjuneyf", "Lulu"),
    ],
    "en": [
        Voice("speech:Dahu-HA-Lulu:qc10fwc040:ugmvnfqyesexvqjuneyf", "Lulu"),
    ]
}

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """设置TTS实体"""
    async_add_entities([SiliconFlowTTSEntity(config_entry)])

class SiliconFlowTTSEntity(TextToSpeechEntity):
    """硅基流动TTS实体"""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """初始化TTS实体"""
        self._config_entry = config_entry
        self._attr_name = "SiliconFlow TTS"
        self._attr_unique_id = f"siliconflow_tts_{config_entry.entry_id}"

    @property
    def supported_languages(self) -> list[str]:
        """返回支持的语言列表"""
        return list(SUPPORTED_VOICES.keys())

    def get_supported_voices(self, language: str) -> list[Voice] | None:
        """获取指定语言支持的语音（动态加载所有可用音色）"""
        # 从动态音色选项中生成Voice对象列表
        voice_options = get_voice_options()
        voices = []
        for voice_id, voice_name in voice_options.items():
            voices.append(Voice(voice_id, voice_name))
        _LOGGER.debug(f"为语言 '{language}' 提供 {len(voices)} 个音色选项")
        return voices

    @property
    def default_language(self) -> str:
        """返回默认语言"""
        return "zh"

    @property
    def supported_audio_codecs(self) -> list[str]:
        """返回支持的音频编解码器"""
        return SUPPORTED_FORMATS

    def _encode_audio_file(self, file_path: str) -> str | None:
        """将音频文件编码为base64字符串"""
        try:
            if not os.path.exists(file_path):
                _LOGGER.error(f"音频文件不存在: {file_path}")
                return None
            
            with open(file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
                
                # 检查文件大小，如果太大则截取前100KB
                if len(audio_data) > 100 * 1024:  # 100KB
                    _LOGGER.warning(f"音频文件较大 ({len(audio_data)} bytes)，截取前100KB")
                    audio_data = audio_data[:100 * 1024]
                
                encoded_audio = base64.b64encode(audio_data).decode('utf-8')
                _LOGGER.debug(f"成功编码音频文件: {file_path}, 大小: {len(audio_data)} bytes")
                return encoded_audio
        except Exception as e:
            _LOGGER.error(f"编码音频文件失败: {e}")
            return None

    def _is_uri_reference(self, reference: str) -> bool:
        """检查是否为URI格式的参考音频"""
        return reference.startswith("speech:")

    async def async_get_tts_audio(
        self,
        message: str,
        language: str,
        options: dict[str, Any] | None = None,
    ) -> TtsAudioType:
        """获取TTS音频"""
        
        api_key = self._config_entry.data.get("api_key")
        if not api_key:
            _LOGGER.error("未找到API密钥")
            return None

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            # 从配置条目的选项中获取参数，优先级：service call options > config entry options > defaults
            config_options = self._config_entry.options
            _LOGGER.debug(f"配置选项: {config_options}")
            _LOGGER.debug(f"服务调用选项: {options}")
            
            # 优化参数获取逻辑，确保正确处理None值
            response_format = (
                options.get("response_format") if options and "response_format" in options
                else config_options.get(CONF_RESPONSE_FORMAT, DEFAULT_RESPONSE_FORMAT)
            )
            speed = (
                options.get("speed") if options and "speed" in options
                else config_options.get(CONF_SPEED, DEFAULT_SPEED)
            )
            sample_rate = (
                options.get("sample_rate") if options and "sample_rate" in options
                else config_options.get(CONF_SAMPLE_RATE, DEFAULT_SAMPLE_RATE)
            )
            gain = (
                options.get("gain") if options and "gain" in options
                else config_options.get(CONF_GAIN, DEFAULT_GAIN)
            )

            # 验证参数范围
            speed = max(MIN_SPEED, min(MAX_SPEED, speed))
            gain = max(MIN_GAIN, min(MAX_GAIN, gain))

            # 构建输入文本，根据API文档添加特殊标记，并解决语音切断问题
            input_text = message.strip()
            
            # 解决语音切断问题：在文本末尾添加适当的标点符号和停顿
            if not input_text.endswith(('.', '。', '!', '！', '?', '？', '，', ',', '、')):
                input_text += "。"  # 添加句号确保语音完整
            
            # 添加轻微的停顿来避免切断（使用标点符号）
            input_text += "  "  # 两个空格提供自然的停顿
            
            if options and "emotion" in options:
                emotion = options["emotion"]
                input_text = f"Can you say it with a {emotion} emotion? <|endofprompt|>{input_text}"
            
            _LOGGER.debug(f"处理后的文本: '{input_text}'")

            # 构建payload
            payload = {
                "model": DEFAULT_MODEL,
                "input": input_text,
                "response_format": response_format,
                "speed": speed,
                "sample_rate": sample_rate,
                "gain": gain,
                "stream": DEFAULT_STREAM,  # 显式设置为false，确保最快响应
            }

            # 确定使用的语音，优先级：service call options > config entry options > defaults
            voice = DEFAULT_VOICE
            
            # 检查是否在service call中指定了语音（包括预设语音和自定义音色）
            if options and "voice" in options:
                voice = options["voice"]
                _LOGGER.info(f"使用service call指定的语音: {voice}")
            elif options and "reference_audio" in options:
                # 为了兼容性，仍然支持reference_audio参数
                reference_audio = options["reference_audio"]
                if self._is_uri_reference(reference_audio):
                    voice = reference_audio
                    _LOGGER.info(f"使用reference_audio参数指定的URI音色: {reference_audio}")
                else:
                    _LOGGER.warning(f"本地文件参考音频暂不支持，请先上传获取URI: {reference_audio}")
            elif config_options.get(CONF_VOICE):
                # 使用配置的音色
                voice = config_options.get(CONF_VOICE)
                _LOGGER.info(f"使用配置的语音: {voice}")
            else:
                # 使用全局默认语音
                _LOGGER.info(f"🎭 使用全局默认语音: {voice}")
                
            # 验证选择的音色是否在可用音色列表中
            voice_options = get_voice_options()
            if voice not in voice_options:
                _LOGGER.warning(f"选择的音色 '{voice}' 不在可用列表中，使用默认音色")
                voice = DEFAULT_VOICE

            payload["voice"] = voice
            
            _LOGGER.info(f"TTS配置 - 音色:{voice[-10:]}..., 格式:{response_format}, 采样率:{sample_rate}Hz, 语速:{speed}, 增益:{gain}dB")
            _LOGGER.debug(f"完整音色ID: {voice}")
            _LOGGER.debug(f"完整payload: {payload}")

            async with aiohttp.ClientSession() as session:
                async with async_timeout.timeout(30):
                    async with session.post(API_ENDPOINT, headers=headers, json=payload) as response:
                        if response.status == 200:
                            audio_data = await response.read()
                            _LOGGER.debug(f"TTS成功，音频大小: {len(audio_data)} bytes")
                            return (response_format, audio_data)
                        else:
                            error_text = await response.text()
                            _LOGGER.error(f"TTS API错误 {response.status}: {error_text}")
                            return None

        except asyncio.TimeoutError:
            _LOGGER.error("TTS请求超时")
            return None
        except Exception as e:
            _LOGGER.error(f"TTS处理错误: {e}")
            return None