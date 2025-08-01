# SiliconFlow TTS for Home Assistant

🎙️ 一个功能强大的 Home Assistant 文本转语音集成，基于 [SiliconFlow](https://siliconflow.cn) 的 CosyVoice2-0.5B 模型。

[![GitHub Release](https://img.shields.io/github/release/your-username/siliconflow-tts-ha)](https://github.com/your-username/siliconflow-tts-ha/releases)
[![License](https://img.shields.io/github/license/your-username/siliconflow-tts-ha)](LICENSE)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-compatible-brightgreen)](https://www.home-assistant.io/)
[![中文文档](https://img.shields.io/badge/文档-中文-blue)](README_OPENSOURCE.md)

## ✨ 功能特性

- 🎭 **动态音色配置** - 在 `configuration.yaml` 中自定义音色，无需修改代码
- 🎵 **内置精品音色** - 阿狸、露露、索拉卡、扎克等精选音色
- 🎚️ **可视化配置界面** - 在 Home Assistant 前端实时调整所有参数
- 🎧 **多种音频格式** - 支持 mp3, wav, opus, pcm
- ⚡ **语速调节** - 0.25-4.0倍速，满足不同场景需求
- 🔊 **音量增益控制** - -10到+10 dB精确调节
- 😊 **情感表达支持** - 让语音更生动自然
- 📊 **高音质采样** - 最高支持 44.1kHz 采样率
- 🔄 **即时生效** - 配置更改无需重启，立即生效
- 🛠️ **完美兼容** - 支持媒体界面和所有服务调用方式
- 🎤 **自定义音色** - 支持上传个人音色文件

## 📦 安装方式

### 方法一：HACS 安装（推荐）

1. 确保已安装 [HACS](https://hacs.xyz/)
2. 进入 HACS → 集成
3. 点击右上角 ⋮ → 自定义存储库
4. 添加此仓库 URL：`https://github.com/your-username/siliconflow-tts-ha`
5. 类别选择"集成"
6. 搜索 "SiliconFlow TTS" 并安装
7. 重启 Home Assistant

### 方法二：手动安装

1. 下载最新版本的压缩包
2. 解压到 `custom_components/siliconflow_tts/`
3. 重启 Home Assistant

## 🚀 快速开始

### 1. 获取 API 密钥

前往 [SiliconFlow 官网](https://cloud.siliconflow.cn/) 注册账号并获取 API 密钥。

### 2. 基础配置

在 Home Assistant 中：
1. 进入 **设置** → **设备与服务**
2. 点击 **添加集成**
3. 搜索 **SiliconFlow TTS**
4. 输入您的 API 密钥

### 3. 使用测试

```yaml
# 在开发者工具中测试
service: tts.speak
data:
  entity_id: tts.siliconflow_tts
  message: "你好，欢迎使用 SiliconFlow TTS"
```

## ⚙️ 高级配置

### 🎭 自定义音色配置

在 `configuration.yaml` 中添加自定义音色：

```yaml
siliconflow_tts:
  custom_voices:
    # 专业音色
    "speech:Dahu-HA-Professional:qc10fwc040:prof001": "专业播音"
    "speech:Dahu-HA-News:qc10fwc040:news001": "新闻主播"
    
    # 个人音色
    "speech:Dahu-HA-Dad:qc10fwc040:family001": "爸爸的声音"
    "speech:Dahu-HA-Mom:qc10fwc040:family002": "妈妈的声音"
    
    # 角色音色
    "speech:Dahu-HA-Robot:qc10fwc040:robot001": "机器人音色"
    "speech:Dahu-HA-Child:qc10fwc040:child001": "儿童音色"
```

配置后重启 Home Assistant，即可在前端配置界面中选择这些音色。

### 🎚️ 前端参数调整

1. 进入 **设置** → **设备与服务**
2. 找到 **SiliconFlow TTS** 集成
3. 点击 **配置** 按钮
4. 在界面中调整：
   - 🎭 选择音色
   - 🚀 调整语速 (0.25-4.0)
   - 🎵 选择音频格式
   - 📊 设置采样率
   - 🔊 调整音量增益

**💡 提示**：所有配置更改立即生效，无需重启！

## 🎤 上传自定义音色教程

### 准备工作

1. **获取 API 密钥**：确保已从 [SiliconFlow](https://cloud.siliconflow.cn/) 获取有效的 API 密钥
2. **准备音频文件**：
   - 格式：wav, mp3, m4a 等常见格式
   - 时长：建议 10-30 秒
   - 内容：清晰的语音，最好包含多种音调
   - 质量：无背景噪音，语音清晰

### 方法一：使用 cURL 命令（推荐）

打开终端，执行以下命令：

```bash
curl --request POST \
  --url https://api.siliconflow.cn/v1/uploads/audio/voice \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: multipart/form-data' \
  --form model=FunAudioLLM/CosyVoice2-0.5B \
  --form customName=my-custom-voice \
  --form 'text=在一无所知中，梦里的一天结束了，一个新的轮回便会开始' \
  --form file=@/path/to/your/audio.wav
```

**参数说明**：
- `YOUR_API_KEY`：替换为您的 SiliconFlow API 密钥
- `customName`：自定义音色名称（英文，无空格）
- `text`：音频对应的文本内容
- `file=@/path/to/your/audio.wav`：音频文件路径

### 方法二：使用 Python 脚本

```python
import requests

def upload_voice(api_key, audio_file_path, custom_name, text):
    url = "https://api.siliconflow.cn/v1/uploads/audio/voice"
    
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    files = {
        'file': open(audio_file_path, 'rb')
    }
    
    data = {
        'model': 'FunAudioLLM/CosyVoice2-0.5B',
        'customName': custom_name,
        'text': text
    }
    
    response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"上传成功！音色 URI: {result['uri']}")
        return result['uri']
    else:
        print(f"上传失败：{response.status_code} - {response.text}")
        return None

# 使用示例
api_key = "your_siliconflow_api_key"
audio_path = "/path/to/your/voice.wav"
voice_name = "my-voice"
voice_text = "这是我的自定义音色测试"

uri = upload_voice(api_key, audio_path, voice_name, voice_text)
```

### 上传成功后的配置

上传成功后，您会收到类似这样的响应：

```json
{
  "uri": "speech:my-custom-voice:qc10fwc040:abc123def456"
}
```

将这个 URI 添加到您的 `configuration.yaml`：

```yaml
siliconflow_tts:
  custom_voices:
    "speech:my-custom-voice:qc10fwc040:abc123def456": "我的专属音色"
```

重启 Home Assistant 后，您就可以在配置界面中选择这个音色了！

### 🔧 故障排除

**上传失败常见原因**：
1. **API 密钥错误**：检查密钥是否正确复制
2. **音频格式不支持**：尝试转换为 wav 格式
3. **文件过大**：建议音频文件小于 10MB
4. **网络问题**：检查网络连接

**音色使用问题**：
1. **音色不显示**：确保已重启 Home Assistant
2. **音色不生效**：检查 URI 是否正确复制
3. **音质不佳**：尝试使用更高质量的源音频

## 📖 使用示例

### 在自动化中使用

```yaml
automation:
  - alias: "门铃提醒"
    trigger:
      platform: state
      entity_id: binary_sensor.doorbell
      to: "on"
    action:
      - service: tts.speak
        data:
          entity_id: tts.siliconflow_tts
          message: "有客人来访，请注意查看"
          # 使用自定义音色
          voice: "speech:my-custom-voice:qc10fwc040:abc123def456"
```

### 在脚本中使用

```yaml
script:
  welcome_home:
    sequence:
      - service: tts.speak
        data:
          entity_id: tts.siliconflow_tts
          message: "欢迎回家，{{ states('sensor.family_member') }}！"
          speed: 1.2
          gain: 2
```

### 在 Node-RED 中使用

```json
{
  "id": "tts_node",
  "type": "api-call-service",
  "name": "TTS 播报",
  "server": "home_assistant_server",
  "service_domain": "tts",
  "service": "speak",
  "data": {
    "entity_id": "tts.siliconflow_tts",
    "message": "这是来自 Node-RED 的消息"
  }
}
```

## 🔧 配置选项

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `voice` | string | 阿狸 | 选择的音色 |
| `speed` | float | 1.0 | 语速 (0.25-4.0) |
| `response_format` | string | mp3 | 音频格式 |
| `sample_rate` | int | 44100 | 采样率 (Hz) |
| `gain` | int | -2 | 音量增益 (dB) |

## 🐛 问题反馈

遇到问题？请通过以下方式反馈：

1. [GitHub Issues](https://github.com/your-username/siliconflow-tts-ha/issues)
2. [Home Assistant 社区论坛](https://bbs.hassbian.com/)

## 🤝 贡献代码

欢迎提交 Pull Request！请确保：

1. 代码符合 Python PEP 8 规范
2. 添加必要的测试用例
3. 更新相关文档

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

## 🙏 致谢

- [SiliconFlow](https://siliconflow.cn/) - 提供优秀的语音合成 API
- [Home Assistant](https://www.home-assistant.io/) - 开源智能家居平台
- 所有贡献者和用户的支持

## 📚 相关资源

- [SiliconFlow API 文档](https://docs.siliconflow.cn/)
- [Home Assistant TTS 文档](https://www.home-assistant.io/integrations/tts/)
- [CosyVoice 项目](https://github.com/FunAudioLLM/CosyVoice)

---

⭐ 如果这个项目对您有帮助，请给我们一个 Star！

🔗 **项目链接**: https://github.com/your-username/siliconflow-tts-ha