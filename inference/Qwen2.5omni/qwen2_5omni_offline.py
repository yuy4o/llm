import soundfile as sf
from transformers import Qwen2_5OmniForConditionalGeneration, Qwen2_5OmniProcessor
from qwen_omni_utils import process_mm_info
import torch
# PreTrainedModel.from_pretrained中搜不到 load_in_8bit/4bits, bitsandbytes 库动态注入
from transformers import BitsAndBytesConfig

quant_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)

# We recommend enabling flash_attention_2 for better acceleration and memory saving.
model = Qwen2_5OmniForConditionalGeneration.from_pretrained("/data1/jiangyy/models/Qwen2.5-Omni-7B", quantization_config=quant_config, device_map={"": 0},attn_implementation="flash_attention_2")

# processor把各种模态的模型输入转为 Tensor，把模型输出转为人类可读内容；input 模型生成
processor = Qwen2_5OmniProcessor.from_pretrained("/data1/jiangyy/models/Qwen2.5-Omni-7B")

conversation = [
    {
        "role": "system",
        "content": [
            {"type": "text", "text": "You are Qwen, a virtual human developed by the Qwen Team, Alibaba Group, capable of perceiving auditory and visual inputs, as well as generating text and speech."}
        ],
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "使用一句话总结视频内容"},
            # {"type": "video", "video": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2.5-Omni/draw.mp4"},
            {"type": "video", "video": "/data1/jiangyy/models/20251223_201754.mp4"}, # 需要将视频下载到本地
        ],
    },
]

# 从视频中抽取音频，输入包含多帧 image tokens 和 一整段 audio waveform
USE_AUDIO_IN_VIDEO = True

# Preparation for inference
text = processor.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
audios, images, videos = process_mm_info(conversation, use_audio_in_video=USE_AUDIO_IN_VIDEO)
inputs = processor(text=text, audio=audios, images=images, videos=videos, return_tensors="pt", padding=True, use_audio_in_video=USE_AUDIO_IN_VIDEO)
inputs = inputs.to(model.device).to(model.dtype)

# 生成语音时，audio decoder 一步步 autoregressive,kv cache持续增长
text_ids, audio = model.generate(**inputs,thinker_max_new_tokens=1024, talker_max_new_tokens=1024,use_audio_in_video=USE_AUDIO_IN_VIDEO)

text = processor.batch_decode(text_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
print(text)
sf.write(
    "output.wav",
    audio.reshape(-1).detach().cpu().numpy(),
    samplerate=24000,
)
