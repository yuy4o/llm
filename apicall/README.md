启用 [Openai Response API](https://platform.openai.com/docs/api-reference/responses/get?lang=python) 需要在较新版本0.11.2的vllm中开启 --structured-outputs-config.backend xgrammar ，见 [OpenAI-Compatible Server](https://github.com/vllm-project/vllm/blob/bb80f69bc98cbf062bf030cb11185f7ba526e28a/docs/serving/openai_compatible_server.md#responses-api)， 调用方式见 [response.py](response.py)

```bash
CUDA_VISIBLE_DEVICES=0,2 VLLM_USE_V1=0 vllm serve /host/AIBOT/Qwen3-14B --dtype auto --api-key empty --port 12000 --trust-remote-code --tensor-parallel-size 2 --pipeline-parallel-size 1 --served-model-name Qwen3-14B --max-model-len 32768 --structured-outputs-config.backend xgrammar --enable-auto-tool-choice --tool-call-parser hermes --gpu_memory_utilization 0.9

(APIServer pid=127) INFO 12-21 00:22:39 [api_server.py:2052] Starting vLLM API server 0 on http://0.0.0.0:12000
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:38] Available routes are:
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /openapi.json, Methods: GET, HEAD
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /docs, Methods: GET, HEAD
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /docs/oauth2-redirect, Methods: GET, HEAD
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /redoc, Methods: GET, HEAD
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /health, Methods: GET
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /load, Methods: GET
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /tokenize, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /detokenize, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /v1/models, Methods: GET
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /version, Methods: GET
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /v1/responses, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /v1/responses/{response_id}, Methods: GET
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /v1/responses/{response_id}/cancel, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /v1/messages, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /v1/chat/completions, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /v1/completions, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /v1/embeddings, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /pooling, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /classify, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /score, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /v1/score, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /v1/audio/transcriptions, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /v1/audio/translations, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /rerank, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /v1/rerank, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /v2/rerank, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /scale_elastic_ep, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /is_scaling_elastic_ep, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /inference/v1/generate, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /ping, Methods: GET
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /ping, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /invocations, Methods: POST
(APIServer pid=127) INFO 12-21 00:22:39 [launcher.py:46] Route: /metrics, Methods: GET
```
