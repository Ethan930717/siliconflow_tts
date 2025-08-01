# SiliconFlow TTS/STT 组件安装指南

## 安装步骤

### 1. 重启Home Assistant
修改了组件文件后，需要重启Home Assistant以加载新的组件。

### 2. 添加集成
重启后，按以下步骤添加集成：

1. 进入 **设置** > **设备与服务**
2. 点击右下角的 **添加集成** 按钮
3. 搜索 **SiliconFlow**
4. 你应该能看到两个集成：
   - **SiliconFlow TTS**
   - **SiliconFlow STT**

### 3. 配置TTS
1. 选择 **SiliconFlow TTS**
2. 输入你的硅基流动API密钥
3. 点击提交

### 4. 配置STT
1. 选择 **SiliconFlow STT**
2. 输入你的硅基流动API密钥
3. 点击提交

### 5. 配置语音助手
配置完成后：

1. 进入 **设置** > **语音助手**
2. 在 **文本转语音** 中选择 **SiliconFlow TTS**
3. 在 **语音转文本** 中选择 **SiliconFlow STT**

## 故障排除

### 找不到集成
如果在添加集成页面找不到SiliconFlow：
1. 确保已重启Home Assistant
2. 检查日志是否有错误信息
3. 确认文件结构正确

### API密钥验证失败
如果API密钥验证失败：
1. 检查API密钥是否正确
2. 确认网络连接正常
3. 检查硅基流动服务状态

### 语音助手中找不到选项
如果在语音助手设置中找不到对应选项：
1. 确保两个集成都已成功配置
2. 重新加载集成
3. 重启Home Assistant

## 使用方法

配置完成后，你可以：

### 在自动化中使用TTS
```yaml
action:
  - service: tts.speak
    target:
      entity_id: tts.siliconflow_tts
    data:
      message: "你能用高兴的情感说吗？<|endofprompt|>Hello World!"
```

### 在脚本中使用
```yaml
script:
  test_tts:
    sequence:
      - service: tts.speak
        target:
          entity_id: tts.siliconflow_tts
        data:
          message: "测试消息"
          options:
            voice: "FunAudioLLM/CosyVoice2-0.5B:anna"
```

### 使用自定义音色
```yaml
script:
  custom_voice:
    sequence:
      - service: tts.speak
        target:
          entity_id: tts.siliconflow_tts
        data:
          message: "自定义音色测试"
          options:
            reference_audio: "speech:your-voice-uri"
```