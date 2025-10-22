# CUDA_VISIBLE_DEVICES=0,1 nohup python -m vllm.entrypoints.openai.api_server --model Qwen1.5-0.5B --host 0.0.0.0 --port 1234 --trust-remote-code --dtype float16 --tensor-parallel-size 2 --api-key LLMSec189! --max-model-len 8192 > nohup.out &

# >> ${PWD}/runtime.log 2>&1

CUDA_VISIBLE_DEVICES=0,1 nohup python -m vllm.entrypoints.openai.api_server --model glm-4-9b-chat --host 0.0.0.0 --port 1234 --trust-remote-code --dtype float16 --tensor-parallel-size 2 --api-key LLMSec189! --max-model-len 8192 > nohup.out &
