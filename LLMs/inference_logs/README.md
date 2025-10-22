## 测试记录

| 模型参数量             | 权重文件占用磁盘空间x2| 推理时占用显存空间x4        |
|-----------------------|---------------------|----------------------------|
| Qwen3-0.6B            | 1.5G                | 2.12G (1024)               |
| Qwen3-1.7B            | 3.8G                | 4.88G (1024)               |
| 7B                    | 14G                 | 28G                        |
| 8B                    | 16G                 | 32G                        |
| Qwen3-8B              | 16G                 | 17.10G (512)               |
| 14B                   | 28G                 | 56G                        |
| Qwen3-30B-A3B-FP8     | 31G                 | -                          |
| gemma-3-27b-it        | 52G                 | 63G (--enforce-eager)      |
| Qwen3-30B-A3B         | 57G                 | 65G (40960)                |
| Qwen3-30B-A3B-yarn    | 57G                 | 80G (131072)               |
| Qwen3-32B             | 62G                 | 65G (2048)                 |


## vllm 测试命令
```shell
CUDA_VISIBLE_DEVICES=2 VLLM_USE_V1=0 vllm serve /data/jiangyy/models/Qwen3-32B --dtype auto --api-key empty --port 12000 --gpu_memory_utilization 0.97 --trust-remote-code --tensor-parallel-size 1 --pipeline-parallel-size 1 --max-model-len 8192 | tee /data/jiangyy/Qwen3-32B.log
```
