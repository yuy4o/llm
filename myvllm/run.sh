# CUDA_VISIBLE_DEVICES=0,1 nohup python -m vllm.entrypoints.openai.api_server --model Qwen1.5-0.5B --host 0.0.0.0 --port 1234 --trust-remote-code --dtype float16 --tensor-parallel-size 2 --api-key LLMSec189! --max-model-len 8192 > nohup.out &

# >> ${PWD}/runtime.log 2>&1

export VLLM_WORKER_MULTIPROC_METHOD=spawn

CUDA_VISIBLE_DEVICES=0 nohup python -m vllm.entrypoints.openai.api_server --model /data/jiangyy/qwen2-0.5b --host 0.0.0.0 --port 1234 --trust-remote-code --tensor-parallel-size 1 --api-key 'LLMSec189!' --max-model-len 8012 --gpu-memory-utilization 0.6 --dtype half  > nohup.out &
