# SiliconFlow TTS 组件

这是一个基于硅基流动API的Home Assistant TTS组件，支持CosyVoice2-0.5B模型。

## 功能特性

- 🎭 **动态音色配置** - 在 `configuration.yaml` 中自定义音色，无需修改代码
- 🎵 内置音色：阿狸、露露、索拉卡、扎克、吴楠
- 🎚️ **前端可视化配置** - 在 Home Assistant 界面中实时调整参数
- 🎧 支持多种音频格式：mp3, wav, opus, pcm
- ⚡ 支持语速调节（0.25-4.0倍速）
- 🔊 支持音量增益调节（-10到+10 dB）
- 😊 支持情感表达
- 📊 支持多种采样率（最高44.1kHz）
- 🔄 **无需重启** - 配置更改立即生效
- 🛠️ **兼容性强** - 支持媒体界面和服务调用

## 安装

1. 将 `siliconflow_tts` 文件夹复制到你的 `custom_components` 目录
2. 重启 Home Assistant
3. 在配置文件中添加以下配置：

```yaml
# configuration.yaml
siliconflow_tts:
  api_key: "your_api_key_here"
  # 可选：自定义音色选项
  custom_voices:
    "speech:Dahu-HA-MyVoice:qc10fwc040:customid123": "我的专属音色"
    "speech:Dahu-HA-BossVoice:qc10fwc040:customid456": "老板音色"
    "speech:your-custom-voice-id": "自定义名称"
```

## 配置选项

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `api_key` | string | 是 | 硅基流动API密钥 |
| `custom_voices` | dict | 否 | 自定义音色选项（音色ID: 显示名称） |

## 🎭 自定义音色配置

您可以在 `configuration.yaml` 中添加自定义音色，这样就不需要修改代码：

### 基础配置
```yaml
siliconflow_tts:
  custom_voices:
    "speech:Dahu-HA-MyCustom:qc10fwc040:uniqueid123": "我的音色"
    "speech:Dahu-HA-Family:qc10fwc040:uniqueid456": "家人音色"
```

### 完整配置示例
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

### 使用自定义音色
配置后，您可以在前端配置界面中选择这些音色，也可以在服务调用中使用：

```yaml
service: tts.speak
data:
  entity_id: tts.siliconflow_tts
  message: "你好，我是专业播音音色"
  voice: "speech:Dahu-HA-Professional:qc10fwc040:prof001"
```

## 使用方法

### 在自动化中使用

```yaml
automation:
  - alias: "TTS测试"
    trigger:
      platform: state
      entity_id: input_boolean.tts_test
    action:
      - service: tts.siliconflow_say
        data:
          message: "你好，这是TTS测试"
          voice: "anna"
          speed: 1.2
          gain: 2
```

### 在脚本中使用

```yaml
script:
  tts_demo:
    sequence:
      - service: tts.siliconflow_say
        data:
          message: "今天天气很好"
          voice: "bella"
          emotion: "happy"
          speed: 1.0
          gain: 0
```

### 使用自定义音色

```yaml
# 使用预设语音
script:
  preset_voice_demo:
    sequence:
      - service: tts.siliconflow_say
        data:
          message: "你能用高兴的情感说吗？<|endofprompt|>今天真是太开心了！"
          voice: "FunAudioLLM/CosyVoice2-0.5B:anna"
          speed: 1.0
          gain: 0

# 使用自定义音色URI
script:
  custom_voice_demo:
    sequence:
      - service: tts.siliconflow_say
        data:
          message: "你能用高兴的情感说吗？<|endofprompt|>这是使用自定义音色的测试！"
          reference_audio: "speech:Dahu-HA-Ari:qc10fwc040:jxlvonagnnzdvbotrmrr"
          speed: 1.0
          gain: 0
```

## 支持的参数

### voice（预设语音）
- `FunAudioLLM/CosyVoice2-0.5B:alex` - Alex (男声)
- `FunAudioLLM/CosyVoice2-0.5B:anna` - Anna (女声)
- `FunAudioLLM/CosyVoice2-0.5B:bella` - Bella (女声)
- `FunAudioLLM/CosyVoice2-0.5B:benjamin` - Benjamin (男声)
- `FunAudioLLM/CosyVoice2-0.5B:charles` - Charles (男声)
- `FunAudioLLM/CosyVoice2-0.5B:claire` - Claire (女声)
- `FunAudioLLM/CosyVoice2-0.5B:david` - David (男声)
- `FunAudioLLM/CosyVoice2-0.5B:diana` - Diana (女声)

### reference_audio（自定义音色）
- 类型：string（URI格式）
- 描述：使用上传后获得的URI作为自定义音色
- 格式：speech:custom-name:model-id:unique-id
- 注意：与voice参数互斥，同时使用时会优先使用reference_audio
- 推荐：使用upload_voice.py脚本先上传音频文件获取URI

### response_format（音频格式）
- `mp3` - MP3格式（默认）
- `wav` - WAV格式
- `opus` - Opus格式
- `pcm` - PCM格式

### speed（语速）
- 范围：0.25 - 4.0
- 默认：1.0

### gain（音量增益）
- 范围：-10 - +10
- 默认：0

### sample_rate（采样率）
- mp3: 32000, 44100 Hz
- wav/pcm: 8000, 16000, 24000, 32000, 44100 Hz
- opus: 48000 Hz

### emotion（情感）
- 支持各种情感描述，如：happy, sad, angry, excited等
- 会自动添加API所需的特殊标记格式

## 自定义音色使用指南

### 方法一：使用本地音频文件

#### 音频文件要求
1. **格式**：支持mp3, wav, opus, pcm格式
2. **时长**：建议5-30秒，太短可能影响音色提取效果
3. **质量**：建议使用清晰、无噪音的音频
4. **内容**：建议包含完整的句子，避免背景音乐

#### 文件路径
- 可以使用绝对路径：`/config/custom_components/siliconflow_tts/Ari.mp3`
- 也可以使用相对路径（相对于Home Assistant配置目录）

### 方法二：使用上传的URI参考音频

#### 上传步骤
1. 使用提供的`upload_voice.py`脚本上传音频文件
2. 脚本会返回一个URI格式的字符串
3. 在TTS配置中直接使用这个URI

#### 使用示例
```bash
# 运行上传脚本
python3 upload_voice.py

# 脚本会输出类似这样的URI：
# speech:Dahu-HA-Ari:qc10fwc040:jxlvonagnnzdvbotrmrr
```

### 使用示例

```yaml
# 使用预设语音
- service: tts.siliconflow_say
  data:
    message: "你能用高兴的情感说吗？<|endofprompt|>使用预设语音测试！"
    voice: "FunAudioLLM/CosyVoice2-0.5B:anna"

# 使用自定义音色URI
- service: tts.siliconflow_say
  data:
    message: "你能用高兴的情感说吗？<|endofprompt|>使用自定义音色测试！"
    reference_audio: "speech:Dahu-HA-Ari:qc10fwc040:jxlvonagnnzdvbotrmrr"
```

## 故障排除

1. **API密钥错误**：确保API密钥正确且有效
2. **网络连接问题**：检查网络连接是否正常
3. **参数范围错误**：确保speed和gain参数在有效范围内
4. **音频格式不支持**：确保选择的音频格式和采样率组合有效
5. **自定义音色文件不存在**：检查音频文件路径是否正确
6. **自定义音色编码失败**：检查音频文件是否损坏或格式不支持

## 日志

组件会记录详细的日志信息，可以在Home Assistant的开发者工具中查看：

```yaml
logger:
  custom_components.siliconflow_tts: debug
```

## 许可证

MIT License 