
## 部署设备指定

借助 `accelerate` 自动拆到能被 `CUDA_VISIBLE_DEVICES` 看到的多张卡
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
).to(model.device)
```