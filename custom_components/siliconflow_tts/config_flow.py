"""SiliconFlow TTS配置流程"""
import asyncio
import logging
from typing import Any

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DOMAIN,
    DEFAULT_VOICE,
    DEFAULT_SPEED,
    DEFAULT_SAMPLE_RATE,
    DEFAULT_RESPONSE_FORMAT,
    DEFAULT_GAIN,
    MIN_SPEED,
    MAX_SPEED,
    MIN_GAIN,
    MAX_GAIN,
    SUPPORTED_FORMATS,
    SUPPORTED_SAMPLE_RATES,
    get_voice_options,
    CONF_VOICE,
    CONF_SPEED,
    CONF_SAMPLE_RATE,
    CONF_RESPONSE_FORMAT,
    CONF_GAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("api_key"): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    api_key = data["api_key"]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "FunAudioLLM/CosyVoice2-0.5B",
        "input": "测试",
        "voice": "FunAudioLLM/CosyVoice2-0.5B:anna",
        "response_format": "mp3",
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(10):
                async with session.post(
                    "https://api.siliconflow.cn/v1/audio/speech",
                    headers=headers,
                    json=payload
                ) as response:
                    _LOGGER.debug(f"TTS API验证响应状态: {response.status}")
                    if response.status == 401:
                        _LOGGER.error("TTS API密钥无效")
                        raise InvalidAuth
                    elif response.status == 403:
                        _LOGGER.error("TTS API密钥权限不足")
                        raise InvalidAuth
                    elif response.status >= 500:
                        _LOGGER.error(f"TTS服务器错误: {response.status}")
                        raise CannotConnect
                    # 200, 400等其他状态码都表示API密钥有效
                    _LOGGER.info("TTS API密钥验证成功")
    except aiohttp.ClientError as e:
        _LOGGER.error(f"TTS网络连接错误: {e}")
        raise CannotConnect
    except asyncio.TimeoutError:
        _LOGGER.error("TTS API请求超时")
        raise CannotConnect
    except Exception as e:
        _LOGGER.error(f"TTS验证过程中出现未知错误: {e}")
        raise CannotConnect

    # Return info that you want to store in the config entry.
    return {"title": "SiliconFlow TTS"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SiliconFlow TTS."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            _LOGGER.info(f"开始验证TTS配置，API密钥长度: {len(user_input.get('api_key', ''))}")
            try:
                info = await validate_input(self.hass, user_input)
                _LOGGER.info("TTS配置验证成功")
            except CannotConnect:
                _LOGGER.error("TTS配置验证失败: 无法连接")
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                _LOGGER.error("TTS配置验证失败: API密钥无效")
                errors["base"] = "invalid_auth"
            except Exception as e:  # pylint: disable=broad-except
                _LOGGER.exception(f"TTS配置验证时出现未知异常: {e}")
                errors["base"] = "unknown"
            else:
                _LOGGER.info(f"TTS集成配置成功: {info['title']}")
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for SiliconFlow TTS."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # 获取当前配置的值，如果没有则使用默认值
        current_voice = self._config_entry.options.get(CONF_VOICE, DEFAULT_VOICE)
        current_speed = self._config_entry.options.get(CONF_SPEED, DEFAULT_SPEED)
        current_sample_rate = self._config_entry.options.get(CONF_SAMPLE_RATE, DEFAULT_SAMPLE_RATE)
        current_response_format = self._config_entry.options.get(CONF_RESPONSE_FORMAT, DEFAULT_RESPONSE_FORMAT)
        current_gain = self._config_entry.options.get(CONF_GAIN, DEFAULT_GAIN)

        # 根据选择的格式获取支持的采样率
        available_sample_rates = SUPPORTED_SAMPLE_RATES.get(current_response_format, [DEFAULT_SAMPLE_RATE])
        
        # 获取当前可用的音色选项（默认 + 用户自定义）
        voice_options = get_voice_options()
        _LOGGER.debug(f"当前可用音色选项: {len(voice_options)} 个")

        options_schema = vol.Schema(
            {
                vol.Optional(CONF_VOICE, default=current_voice): vol.In(voice_options),
                vol.Optional(CONF_SPEED, default=current_speed): vol.All(
                    vol.Coerce(float), vol.Range(min=MIN_SPEED, max=MAX_SPEED)
                ),
                vol.Optional(CONF_RESPONSE_FORMAT, default=current_response_format): vol.In(SUPPORTED_FORMATS),
                vol.Optional(CONF_SAMPLE_RATE, default=current_sample_rate): vol.In(available_sample_rates),
                vol.Optional(CONF_GAIN, default=current_gain): vol.All(
                    vol.Coerce(int), vol.Range(min=MIN_GAIN, max=MAX_GAIN)
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""