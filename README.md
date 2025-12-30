# Joy of LLM

### DeepSeek UE8M0 FP8

以[DeepSeek-V3.1](https://huggingface.co/deepseek-ai/DeepSeek-V3.1/blob/main/model.safetensors.index.json)为例，不同数值精度参考 [Using FP8 and FP4 with Transformer Engine](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/fp8_primer.html#)：
```
model.layers.0.mlp.down_proj.weight	[7 168, 18 432]	F8_E4M3
model.layers.0.mlp.down_proj.weight_scale_inv	[56, 144]	F32
```

H100上进行FP8推理时，`weight_scale_inv` 由F32 解码为 UE8M0，降低 **scale而非weight** 的精度，因为对于scale而言指数位exponent相比尾数位mantissa更显著，且F32和UE8M0都具有8位exponent

`weight_scale_inv`作为指数级缩放因子为2^-k，可以作用在任何数值类型，但比较适合FP8/FP4动态范围小的类型上。并不真正参与计算。UE8M0 是scale的硬件编码格式，PyTorch / safetensors 不支持 UE8M0，因此模型文件中用 F32存储，推理时会
```
k = round(-log2(weight_scale_inv_f32))
weight_scale_inv = 2^-k   # UE8M0
real_weight = quantized_weight / weight_scale_inv = quantized_weight * weight_scale
```

```
checkpoint / PyTorch            H100 / FP8 kernel
───────────────────             ──────────────────
BF16 scale_inv   ──►  log2 / round  ──►  指数提取k
                                            │
                                            ▼
                                           量化
                                    UE8M0 scale = 2^k
                                    UE8M0 scale_inv = 2^-k
                                            │
                                            ▼
                                    FP8 Tensor Core GEMM
```

A100上不支持FP8，会将**权重/激活** F8_E4M3 升精/反量化为 BF16（优先于FP16）运算，方法为多余位补零