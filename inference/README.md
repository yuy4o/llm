## 部署设备指定

#### 模型：

`device_map` 本质是：模块 -> 设备 的一对一映射表，一个模块只能映射到一张卡上：

`device_map={"": 0}`：所有模块对应GPU0

`device_map = {"thinker": 0,"talker": 1,"audio_decoder": 1,"vision_tower": 0,"model.embed_tokens": 0,"lm_head": 0}`：不同模块对应不同GPU

`device_map="auto"`：交给`accelerate` 自动分配

`device_map="balanced"`：多 GPU 显存均衡

`device_map={"vision_tower": 0, "": "auto"}`：除了vision_tower模块对应GPU0，剩下模块自动分配

借助 `accelerate` 自动拆到能被 `CUDA_VISIBLE_DEVICES` 看到的多张卡, [官方参数解释](https://github.com/huggingface/transformers/blob/a7f29523361b2cc12e51c1f5133d95f122f6f45c/src/transformers/modeling_utils.py#L3676)
```python
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "/data1/jiangyy/imagemodels/Qwen2-VL-2B-Instruct",
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
    device_map="auto",
)
```

只能单卡，`to("cuda")` 等价于 `to("cuda:0")`，前提还要通过 `CUDA_VISIBLE_DEVICES` 指定能看到哪几张卡
```python
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "/data1/jiangyy/imagemodels/Qwen2-VL-2B-Instruct",
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
).to("cuda:3")
```

#### 数据：
```python
# 默认在cpu 等价于 .to("cpu")
inputs = processor(
    text=[text],
    images=image_inputs,
    videos=video_inputs,
    padding=True,
    return_tensors="pt",
)

# 推荐写法  .to(model.device)等价于 .to("cuda")
inputs = processor(
    text=[text],
    images=image_inputs,
    videos=video_inputs,
    padding=True,
    return_tensors="pt",
).to(model.device).to(model.dtype)
```

#### 经验：

运行`CUDA_VISIBLE_DEVIECES=0,2 python call_omni.py` 时只能看到物理GPU0，2。CUDA_VISIBLE_DEVICES之后，GPU被“重新编号”，报错信息中的GPU1 对应 物理GPU2
```
CUDA_VISIBLE_DEVICES=0,2

物理 GPU:     [0]        [2]
程序视角:    cuda:0    cuda:1

torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 316.00 MiB. GPU 1 has a total capacity of 39.38 GiB of which 293.81 MiB is free. Process 643064 has 33.81 GiB memory in use. Including non-PyTorch memory, this process has 5.25 GiB memory in use. Of the allocated memory 4.54 GiB is allocated by PyTorch, and 221.75 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
```