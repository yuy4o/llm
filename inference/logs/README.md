## 测试记录

| 模型参数量             | 权重文件占用磁盘空间x2| 推理时占用显存空间x4        |备注|
|-----------------------|---------------------|----------------------------|-|
| Qwen3-0.6B            | 1.5G                | 2.12G (1024)               ||
| Qwen3-1.7B            | 3.8G                | 4.88G (1024)               ||
| 7B                    | 14G                 | 28G                        ||
| 8B                    | 16G                 | 32G                        ||
| Qwen3-8B              | 16G                 | 17.10G (512)               ||
| 14B                   | 28G                 | 56G                        ||
| Qwen3-30B-A3B-FP8     | 31G                 | -                          ||
| gemma-3-27b-it        | 52G                 | 63G (--enforce-eager)      ||
| Qwen3-30B-A3B         | 57G                 | 65G (40960)                ||
| Qwen3-30B-A3B-yarn    | 57G                 | 80G (131072)               ||
| Qwen3-32B             | 62G                 | 65G (2048)                 ||
| QwQ-32B               | 61.8G               | 73.5G (2048)               ||
| gpt-oss-20b           | 13.8G很小奇怪        | 73.65G(2048)               |推理速度快|
| Seed-OSS-36B-Instruct | 68.4G               | 73.67G(2048)               ||
| Kimi-Linear-48B-A3B-Instruct | 92G          | -(4096)                    |160G显存sglang, vllm能部署|
| Qwen3-Next-80B-A3B-Instruct | 152G          | 160G (262144)              |160G显存sglang能部署，vllm显存不够|
| gpt-oss-120b          | 62G很小很奇怪        | 160G不够(512)              ||


## vllm 测试命令

docker 镜像拉取：https://hub.docker.com/r/vllm/vllm-openai/tags?page=2
```shell
docker pull vllm/vllm-openai:v0.11.2


docker run -d --gpus all -v /data/jiangyy/dockpath:/dockpath --network=host --entrypoint tail vllm/vllm-openai:v0.11.2 -f /dev/null
```

**gpu_memory_utilization 不能设为1，避免初始化时被驱动预留部分卡死**

```shell
CUDA_VISIBLE_DEVICES=0,1,2,3 VLLM_USE_V1=0 vllm serve /dockpath/Qwen3-Next-80B-A3B-Instruct --dtype auto --api-key empty --port 12001 --trust-remote-code --tensor-parallel-size 4 --pipeline-parallel-size 1 --served-model-name Qwen3-Next --max-model-len 4096 --gpu_memory_utilization 0.95 2>&1 | tee Qwen3-Next-80B-A3B-Instruct.log
```

```shell
CUDA_VISIBLE_DEVICES=5 VLLM_USE_V1=0 vllm serve /data1/llm-models/Qwen3-30B-A3B --dtype auto --api-key empty --port 12001 --gpu_memory_utilization 0.9 --trust-remote-code --tensor-parallel-size 1 --pipeline-parallel-size 1 --rope-scaling '{"rope_type":"yarn","factor":4.0,"original_max_position_embeddings":32768}' --max-model-len 131072
```

容器外运行命令：
```shell
docker exec -it 332f bash -c "CUDA_VISIBLE_DEVICES=2,3 python -m sglang.launch_server --model /dockpath/Qwen3-Coder-30B-A3B-Instruct --trust-remote-code --host 0.0.0.0 --port 12001 --tp 2 --max-running-requests 4 --mem-fraction-static 0.98 --context-length 32768 > /dockpath/Qwen3-Coder-30B-A3B-Instruct.log 2>&1"
```

## sglang 测试命令

aliyun国内镜像加速：https://help.aliyun.com/zh/acr/user-guide/accelerate-the-pulls-of-docker-official-images

配置到`/etc/docker/daemon.json`中 `"registry-mirrors"`

docker 镜像拉取：https://hub.docker.com/r/lmsysorg/sglang/tags?page=3
```shell
docker pull lmsysorg/sglang:latest
docker pull lmsysorg/sglang:v0.5.5.post3-cu129-amd64
```

docker部署，配置NCCL否则报错 `sglang RuntimeError: NCCL error: unhandled system error (run with NCCL_DEBUG=INFO for details)`

```shell
docker run -d --gpus all -v /data/jiangyy/dockpath:/dockpath --network=host \
  -e NCCL_SOCKET_IFNAME=eth0 \
  -e GLOO_SOCKET_IFNAME=eth0 \
  -e NCCL_IB_DISABLE=1 \
  -e NCCL_P2P_LEVEL=SYS \
  -e NCCL_DEBUG=INFO \
  --shm-size=32g \
  --entrypoint tail \
  lmsysorg/sglang:v0.5.5.post3-cu129-amd64 -f /dev/null
```

4*A100 160G显存sglang能部署 Qwen3-Next-80B-A3B-Instruct
```shell
CUDA_VISIBLE_DEVICES=0,1,2,3 python -m sglang.launch_server --model  /dockpath/Qwen3-Next-80B-A3B-Instruct --trust-remote-code --host 0.0.0.0 --port 12001 --tp 4 --max-running-requests 4 --mem-fraction-static 0.98 --context-length 4096
```
