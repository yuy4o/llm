| input_video_length | model | talker_max_new_tokens | vram | output_audio_length |
|------------|-------|--------------|------|----------------|
| 60s        | Qwen2.5-Omni-7B   | 1024   | 38G  | 15s      |


command:
```python
python qwen2_5omni_offline.py
```

log:
```shell
Unrecognized keys in `rope_scaling` for 'rope_type'='default': {'mrope_section'}
You are attempting to use Flash Attention 2 without specifying a torch dtype. This might lead to unexpected behaviour
Qwen2_5OmniToken2WavModel must inference with fp32, but flash_attention_2 only supports fp16 and bf16, attention implementation of Qwen2_5OmniToken2WavModel will fallback to sdpa.
Loading checkpoint shards: 100%|███████████████████████████████████████████████████████████████| 5/5 [00:29<00:00,  5.80s/it]
The image processor of type `Qwen2VLImageProcessor` is now loaded as a fast processor by default, even if the model checkpoint was saved with a slow processor. This is a breaking change and may produce slightly different outputs. To continue using the slow processor, instantiate this class with `use_fast=False`. Note that this behavior will be extended to all models in a future release.
/data1/jiangyy/miniconda3/lib/python3.10/site-packages/qwen_omni_utils/v2_5/audio_process.py:85: UserWarning: PySoundFile failed. Trying audioread instead.
  librosa.load(
/data1/jiangyy/miniconda3/lib/python3.10/site-packages/librosa/core/audio.py:184: FutureWarning: librosa.core.audio.__audioread_load
        Deprecated as of librosa version 0.10.0.
        It will be removed in librosa version 1.0.
  y, sr_native = __audioread_load(path, offset, duration, dtype)
qwen-vl-utils using torchvision to read video.
Token indices sequence length is longer than the specified maximum sequence length for this model (46785 > 32768). Running this sequence through the model will result in indexing errors
Setting `pad_token_id` to `eos_token_id`:8292 for open-end generation.
This is a friendly reminder - the current text generation call will exceed the model's predefined maximum length (32768). Depending on the model, you may observe exceptions, performance degradation, or nothing at all.
['system\nYou are Qwen, a virtual human developed by the Qwen Team, Alibaba Group, capable of perceiving auditory and visual inputs, as well as generating text and speech.\nuser\n使用一句话总结视频内容\nassistant\n嗯…这个视频内容是关于ChatGPT的年度回顾，有2025年三大亮点，聊天统计数据，还有年度专属奖品等信息。你要是还有啥想法或者问题，随时跟我说哈。']
```