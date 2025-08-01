"""硅基流动TTS组件初始化文件"""
import logging
import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_CUSTOM_VOICES, update_voice_options

_LOGGER = logging.getLogger(__name__)

# configuration.yaml 配置架构
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_CUSTOM_VOICES, default={}): vol.Schema(
                    {cv.string: cv.string}
                )
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: dict):
    """设置组件"""
    # 读取用户自定义音色配置
    domain_config = config.get(DOMAIN, {})
    custom_voices = domain_config.get(CONF_CUSTOM_VOICES, {})
    
    if custom_voices:
        _LOGGER.info(f"🎭 加载了 {len(custom_voices)} 个自定义音色: {list(custom_voices.values())}")
        update_voice_options(custom_voices)
    else:
        _LOGGER.debug("未发现自定义音色配置，使用默认音色")
    
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """从配置条目设置组件"""
    await hass.config_entries.async_forward_entry_setups(entry, ["tts"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """卸载配置条目"""
    return await hass.config_entries.async_unload_platforms(entry, ["tts"])