## Basic Use

`Dockerfile` is used to build the minimum llama.cpp server image.

`llama-server` command related params: https://github.com/ggml-org/llama.cpp/tree/b7342/tools/server

### CPU: [llama.cpp:server-b7342](https://github.com/ggml-org/llama.cpp/pkgs/container/llama.cpp/605770709?tag=server-b7342)

```shell
docker build -t llama.cpp:server-b7342 .

# 先创建容器，进入容器拉起服务
docker run -d -p 5001:5001 -v /workspaces/yuy4o:/app llama.cpp:server-b7342 tail -f /dev/null
llama-server -m /app/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf --port 5006 --host 0.0.0.0

# 创建容器同时拉起服务
docker run -d \
  --name llama-server \
  -p 5006:5006 \
  -v /data1/jiangyy/2llamacpp-b7342/2llamacpp-b7342/llama.cpp:/app \
  llamacppserver:v2 \
  llama-server \
  -m /app/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf \
  --host 0.0.0.0 \
  --port 5006

# 容器外查看模型日志 
docker logs -f llama-server
```

```shell
curl -X POST http://localhost:5006/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf",
        "messages": [
          {
            "role": "system",
            "content": "你是一个有帮助的 AI 助手。"
          },
          {
            "role": "user",
            "content": "帮我生成一个随机数，直接返回我数字"
          }
        ],
        "max_tokens": 512,
        "temperature": 0,
        "top-p": 0.9,
        "repeat-penalty": 1.1,
        "stream": false
      }'

```

### CUDA: [llama.cpp:server-cuda-b7342](https://github.com/ggml-org/llama.cpp/pkgs/container/llama.cpp/605803160?tag=server-cuda-b7342)

```bash
docker pull ghcr.io/ggml-org/llama.cpp:server-cuda-b7342

# 覆盖镜像中的 entrypoint 运行
docker run -d \
  --gpus '"device=0,1,2,3"' \
  --network host \
  -v /data1/jiangyy/models:/models \
  --entrypoint tail \
  llama.cpp:server-cuda-b7342 \
  -f /dev/null

# 容器内运行模型
CUDA_VISIBLE_DEVICES=2 \
./llama-server \
  --model /models/Qwen3-Coder-30B-A3B-Instruct-Q8_0.gguf \
  --host 0.0.0.0 \
  --port 5006 \
  --ctx-size 65536
```

```log
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA A100-PCIE-40GB, compute capability 8.0, VMM: yes
load_backend: loaded CUDA backend from /app/libggml-cuda.so
load_backend: loaded CPU backend from /app/libggml-cpu-icelake.so
warn: LLAMA_ARG_HOST environment variable is set, but will be overwritten by command line argument --host
main: setting n_parallel = 4 and kv_unified = true (add -kvu to disable this)
build: 7342 (2fbe3b7bb) with GNU 11.4.0 for Linux x86_64
system info: n_threads = 24, n_threads_batch = 24, total_threads = 48

system_info: n_threads = 24 (n_threads_batch = 24) / 48 | CUDA : ARCHS = 500,610,700,750,800,860,890 | USE_GRAPHS = 1 | PEER_MAX_BATCH_SIZE = 128 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | AVX512 = 1 | AVX512_VBMI = 1 | AVX512_VNNI = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK = 1 | 

init: using 47 threads for HTTP server
start: binding port with default address family
main: loading model
srv    load_model: loading model '/models/Qwen3-Coder-30B-A3B-Instruct-Q8_0.gguf'
llama_model_load_from_file_impl: using device CUDA0 (NVIDIA A100-PCIE-40GB) (0000:00:0c.0) - 39903 MiB free
llama_model_loader: loaded meta data with 44 key-value pairs and 579 tensors from /models/Qwen3-Coder-30B-A3B-Instruct-Q8_0.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = qwen3moe
llama_model_loader: - kv   1:                               general.type str              = model
llama_model_loader: - kv   2:                               general.name str              = Qwen3-Coder-30B-A3B-Instruct
llama_model_loader: - kv   3:                           general.finetune str              = Instruct
llama_model_loader: - kv   4:                           general.basename str              = Qwen3-Coder-30B-A3B-Instruct
llama_model_loader: - kv   5:                       general.quantized_by str              = Unsloth
llama_model_loader: - kv   6:                         general.size_label str              = 30B-A3B
llama_model_loader: - kv   7:                            general.license str              = apache-2.0
llama_model_loader: - kv   8:                       general.license.link str              = https://huggingface.co/Qwen/Qwen3-Cod...
llama_model_loader: - kv   9:                           general.repo_url str              = https://huggingface.co/unsloth
llama_model_loader: - kv  10:                   general.base_model.count u32              = 1
llama_model_loader: - kv  11:                  general.base_model.0.name str              = Qwen3 Coder 30B A3B Instruct
llama_model_loader: - kv  12:          general.base_model.0.organization str              = Qwen
llama_model_loader: - kv  13:              general.base_model.0.repo_url str              = https://huggingface.co/Qwen/Qwen3-Cod...
llama_model_loader: - kv  14:                               general.tags arr[str,2]       = ["unsloth", "text-generation"]
llama_model_loader: - kv  15:                       qwen3moe.block_count u32              = 48
llama_model_loader: - kv  16:                    qwen3moe.context_length u32              = 262144
llama_model_loader: - kv  17:                  qwen3moe.embedding_length u32              = 2048
llama_model_loader: - kv  18:               qwen3moe.feed_forward_length u32              = 5472
llama_model_loader: - kv  19:              qwen3moe.attention.head_count u32              = 32
llama_model_loader: - kv  20:           qwen3moe.attention.head_count_kv u32              = 4
llama_model_loader: - kv  21:                    qwen3moe.rope.freq_base f32              = 10000000.000000
llama_model_loader: - kv  22:  qwen3moe.attention.layer_norm_rms_epsilon f32              = 0.000001
llama_model_loader: - kv  23:                 qwen3moe.expert_used_count u32              = 8
llama_model_loader: - kv  24:              qwen3moe.attention.key_length u32              = 128
llama_model_loader: - kv  25:            qwen3moe.attention.value_length u32              = 128
llama_model_loader: - kv  26:                      qwen3moe.expert_count u32              = 128
llama_model_loader: - kv  27:        qwen3moe.expert_feed_forward_length u32              = 768
llama_model_loader: - kv  28: qwen3moe.expert_shared_feed_forward_length u32              = 0
llama_model_loader: - kv  29:                       tokenizer.ggml.model str              = gpt2
llama_model_loader: - kv  30:                         tokenizer.ggml.pre str              = qwen2
llama_model_loader: - kv  31:                      tokenizer.ggml.tokens arr[str,151936]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  32:                  tokenizer.ggml.token_type arr[i32,151936]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  33:                      tokenizer.ggml.merges arr[str,151387]  = ["Ġ Ġ", "ĠĠ ĠĠ", "i n", "Ġ t",...
llama_model_loader: - kv  34:                tokenizer.ggml.eos_token_id u32              = 151645
llama_model_loader: - kv  35:            tokenizer.ggml.padding_token_id u32              = 151654
llama_model_loader: - kv  36:               tokenizer.ggml.add_bos_token bool             = false
llama_model_loader: - kv  37:                    tokenizer.chat_template str              = {# Copyright 2025-present Unsloth. Ap...
llama_model_loader: - kv  38:               general.quantization_version u32              = 2
llama_model_loader: - kv  39:                          general.file_type u32              = 7
llama_model_loader: - kv  40:                      quantize.imatrix.file str              = Qwen3-Coder-30B-A3B-Instruct-GGUF/ima...
llama_model_loader: - kv  41:                   quantize.imatrix.dataset str              = unsloth_calibration_Qwen3-Coder-30B-A...
llama_model_loader: - kv  42:             quantize.imatrix.entries_count u32              = 384
llama_model_loader: - kv  43:              quantize.imatrix.chunks_count u32              = 154
llama_model_loader: - type  f32:  241 tensors
llama_model_loader: - type q8_0:  338 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q8_0
print_info: file size   = 30.25 GiB (8.51 BPW) 
load: printing all EOG tokens:
load:   - 151643 ('<|endoftext|>')
load:   - 151645 ('<|im_end|>')
load:   - 151662 ('<|fim_pad|>')
load:   - 151663 ('<|repo_name|>')
load:   - 151664 ('<|file_sep|>')
load: special tokens cache size = 26
load: token to piece cache size = 0.9311 MB
print_info: arch             = qwen3moe
print_info: vocab_only       = 0
print_info: n_ctx_train      = 262144
print_info: n_embd           = 2048
print_info: n_embd_inp       = 2048
print_info: n_layer          = 48
print_info: n_head           = 32
print_info: n_head_kv        = 4
print_info: n_rot            = 128
print_info: n_swa            = 0
print_info: is_swa_any       = 0
print_info: n_embd_head_k    = 128
print_info: n_embd_head_v    = 128
print_info: n_gqa            = 8
print_info: n_embd_k_gqa     = 512
print_info: n_embd_v_gqa     = 512
print_info: f_norm_eps       = 0.0e+00
print_info: f_norm_rms_eps   = 1.0e-06
print_info: f_clamp_kqv      = 0.0e+00
print_info: f_max_alibi_bias = 0.0e+00
print_info: f_logit_scale    = 0.0e+00
print_info: f_attn_scale     = 0.0e+00
print_info: n_ff             = 5472
print_info: n_expert         = 128
print_info: n_expert_used    = 8
print_info: n_expert_groups  = 0
print_info: n_group_used     = 0
print_info: causal attn      = 1
print_info: pooling type     = 0
print_info: rope type        = 2
print_info: rope scaling     = linear
print_info: freq_base_train  = 10000000.0
print_info: freq_scale_train = 1
print_info: n_ctx_orig_yarn  = 262144
print_info: rope_finetuned   = unknown
print_info: model type       = 30B.A3B
print_info: model params     = 30.53 B
print_info: general.name     = Qwen3-Coder-30B-A3B-Instruct
print_info: n_ff_exp         = 768
print_info: vocab type       = BPE
print_info: n_vocab          = 151936
print_info: n_merges         = 151387
print_info: BOS token        = 11 ','
print_info: EOS token        = 151645 '<|im_end|>'
print_info: EOT token        = 151645 '<|im_end|>'
print_info: PAD token        = 151654 '<|vision_pad|>'
print_info: LF token         = 198 'Ċ'
print_info: FIM PRE token    = 151659 '<|fim_prefix|>'
print_info: FIM SUF token    = 151661 '<|fim_suffix|>'
print_info: FIM MID token    = 151660 '<|fim_middle|>'
print_info: FIM PAD token    = 151662 '<|fim_pad|>'
print_info: FIM REP token    = 151663 '<|repo_name|>'
print_info: FIM SEP token    = 151664 '<|file_sep|>'
print_info: EOG token        = 151643 '<|endoftext|>'
print_info: EOG token        = 151645 '<|im_end|>'
print_info: EOG token        = 151662 '<|fim_pad|>'
print_info: EOG token        = 151663 '<|repo_name|>'
print_info: EOG token        = 151664 '<|file_sep|>'
print_info: max token length = 256
load_tensors: loading model tensors, this can take a while... (mmap = true)
load_tensors: offloading 48 repeating layers to GPU
load_tensors: offloading output layer to GPU
load_tensors: offloaded 49/49 layers to GPU
load_tensors:   CPU_Mapped model buffer size =   315.30 MiB
load_tensors:        CUDA0 model buffer size = 30658.12 MiB
....................................................................................................
llama_context: constructing llama_context
llama_context: n_seq_max     = 4
llama_context: n_ctx         = 65536
llama_context: n_ctx_seq     = 65536
llama_context: n_batch       = 2048
llama_context: n_ubatch      = 512
llama_context: causal_attn   = 1
llama_context: flash_attn    = auto
llama_context: kv_unified    = true
llama_context: freq_base     = 10000000.0
llama_context: freq_scale    = 1
llama_context: n_ctx_seq (65536) < n_ctx_train (262144) -- the full capacity of the model will not be utilized
llama_context:  CUDA_Host  output buffer size =     2.32 MiB
llama_kv_cache:      CUDA0 KV buffer size =  6144.00 MiB
llama_kv_cache: size = 6144.00 MiB ( 65536 cells,  48 layers,  4/1 seqs), K (f16): 3072.00 MiB, V (f16): 3072.00 MiB
llama_context: Flash Attention was auto, set to enabled
llama_context:      CUDA0 compute buffer size =   300.75 MiB
llama_context:  CUDA_Host compute buffer size =   132.01 MiB
llama_context: graph nodes  = 3031
llama_context: graph splits = 2
common_init_from_params: added <|endoftext|> logit bias = -inf
common_init_from_params: added <|im_end|> logit bias = -inf
common_init_from_params: added <|fim_pad|> logit bias = -inf
common_init_from_params: added <|repo_name|> logit bias = -inf
common_init_from_params: added <|file_sep|> logit bias = -inf
common_init_from_params: setting dry_penalty_last_n to ctx_size = 65536
common_init_from_params: warming up the model with an empty run - please wait ... (--no-warmup to disable)
srv          init: initializing slots, n_slots = 4
slot         init: id  0 | task -1 | new slot, n_ctx = 65536
slot         init: id  1 | task -1 | new slot, n_ctx = 65536
slot         init: id  2 | task -1 | new slot, n_ctx = 65536
slot         init: id  3 | task -1 | new slot, n_ctx = 65536
srv          init: prompt cache is enabled, size limit: 8192 MiB
srv          init: use `--cache-ram 0` to disable the prompt cache
srv          init: for more info see https://github.com/ggml-org/llama.cpp/pull/16391
srv          init: thinking = 0
init: chat template, chat_template: {# Copyright 2025-present Unsloth. Apache 2.0 License. Unsloth Chat template fixes #}
{% macro render_item_list(item_list, tag_name='required') %}
    {%- if item_list is defined and item_list is iterable and item_list | length > 0 %}
        {%- if tag_name %}{{- '\n<' ~ tag_name ~ '>' -}}{% endif %}
            {{- '[' }}
                {%- for item in item_list -%}
                    {%- if loop.index > 1 %}{{- ", "}}{% endif -%}
                    {%- if item is string -%}
                        {{ "`" ~ item ~ "`" }}
                    {%- else -%}
                        {{ item }}
                    {%- endif -%}
                {%- endfor -%}
            {{- ']' }}
        {%- if tag_name %}{{- '</' ~ tag_name ~ '>' -}}{% endif %}
    {%- endif %}
{% endmacro %}

{%- if messages[0]["role"] == "system" %}
    {%- set system_message = messages[0]["content"] %}
    {%- set loop_messages = messages[1:] %}
{%- else %}
    {%- set loop_messages = messages %}
{%- endif %}

{%- if not tools is defined %}
    {%- set tools = [] %}
{%- endif %}

{%- if system_message is defined %}
    {{- "<|im_start|>system\n" + system_message }}
{%- else %}
    {%- if tools is iterable and tools | length > 0 %}
        {{- "<|im_start|>system\nYou are Qwen, a helpful AI assistant that can interact with a computer to solve tasks." }}
    {%- endif %}
{%- endif %}
{%- if tools is iterable and tools | length > 0 %}
    {{- "\n\nYou have access to the following functions:\n\n" }}
    {{- "<tools>" }}
    {%- for tool in tools %}
        {%- if tool.function is defined %}
            {%- set tool = tool.function %}
        {%- endif %}
        {{- "\n<function>\n<name>" ~ tool.name ~ "</name>" }}
        {{- '\n<description>' ~ (tool.description | trim) ~ '</description>' }}
        {{- '\n<parameters>' }}
        {%- for param_name, param_fields in tool.parameters.properties|items %}
            {{- '\n<parameter>' }}
            {{- '\n<name>' ~ param_name ~ '</name>' }}
            {%- if param_fields.type is defined %}
                {{- '\n<type>' ~ (param_fields.type | string) ~ '</type>' }}
            {%- endif %}
            {%- if param_fields.description is defined %}
                {{- '\n<description>' ~ (param_fields.description | trim) ~ '</description>' }}
            {%- endif %}
            {{- render_item_list(param_fields.enum, 'enum') }}
            {%- set handled_keys = ['type', 'description', 'enum', 'required'] %}
            {%- for json_key, json_value in param_fields|items %}
                {%- if json_key not in handled_keys %}
                    {%- set normed_json_key = json_key|string %}
                    {%- if json_value is mapping %}
                        {{- '\n<' ~ normed_json_key ~ '>' ~ (json_value | tojson | safe) ~ '</' ~ normed_json_key ~ '>' }}
                    {%- else %}
                        {{- '\n<' ~ normed_json_key ~ '>' ~ (json_value | string) ~ '</' ~ normed_json_key ~ '>' }}
                    {%- endif %}
                {%- endif %}
            {%- endfor %}
            {{- render_item_list(param_fields.required, 'required') }}
            {{- '\n</parameter>' }}
        {%- endfor %}
        {{- render_item_list(tool.parameters.required, 'required') }}
        {{- '\n</parameters>' }}
        {%- if tool.return is defined %}
            {%- if tool.return is mapping %}
                {{- '\n<return>' ~ (tool.return | tojson | safe) ~ '</return>' }}
            {%- else %}
                {{- '\n<return>' ~ (tool.return | string) ~ '</return>' }}
            {%- endif %}
        {%- endif %}
        {{- '\n</function>' }}
    {%- endfor %}
    {{- "\n</tools>" }}
    {{- '\n\nIf you choose to call a function ONLY reply in the following format with NO suffix:\n\n<tool_call>\n<function=example_function_name>\n<parameter=example_parameter_1>\nvalue_1\n</parameter>\n<parameter=example_parameter_2>\nThis is the value for the second parameter\nthat can span\nmultiple lines\n</parameter>\n</function>\n</tool_call>\n\n<IMPORTANT>\nReminder:\n- Function calls MUST follow the specified format: an inner <function=...></function> block must be nested within <tool_call></tool_call> XML tags\n- Required parameters MUST be specified\n- You may provide optional reasoning for your function call in natural language BEFORE the function call, but NOT after\n- If there is no function call available, answer the question like normal with your current knowledge and do not tell the user about function calls\n</IMPORTANT>' }}
{%- endif %}
{%- if system_message is defined %}
    {{- '<|im_end|>\n' }}
{%- else %}
    {%- if tools is iterable and tools | length > 0 %}
        {{- '<|im_end|>\n' }}
    {%- endif %}
{%- endif %}
{%- for message in loop_messages %}
    {%- if message.role == "assistant" and message.tool_calls is defined and message.tool_calls is iterable and message.tool_calls | length > 0 %}
        {{- '<|im_start|>' + message.role }}
        {%- if message.content is defined and message.content is string and message.content | trim | length > 0 %}
            {{- '\n' + message.content | trim + '\n' }}
        {%- endif %}
        {%- for tool_call in message.tool_calls %}
            {%- if tool_call.function is defined %}
                {%- set tool_call = tool_call.function %}
            {%- endif %}
            {{- '\n<tool_call>\n<function=' + tool_call.name + '>\n' }}
            {%- if tool_call.arguments is defined %}
                {%- for args_name, args_value in tool_call.arguments|items %}
                    {{- '<parameter=' + args_name + '>\n' }}
                    {%- set args_value = args_value if args_value is string else args_value | string %}
                    {{- args_value }}
                    {{- '\n</parameter>\n' }}
                {%- endfor %}
            {%- endif %}
            {{- '</function>\n</tool_call>' }}
        {%- endfor %}
        {{- '<|im_end|>\n' }}
    {%- elif message.role == "user" or message.role == "system" or message.role == "assistant" %}
        {{- '<|im_start|>' + message.role + '\n' + message.content + '<|im_end|>' + '\n' }}
    {%- elif message.role == "tool" %}
        {%- if loop.previtem and loop.previtem.role != "tool" %}
            {{- '<|im_start|>user\n' }}
        {%- endif %}
        {{- '<tool_response>\n' }}
        {{- message.content }}
        {{- '\n</tool_response>\n' }}
        {%- if not loop.last and loop.nextitem.role != "tool" %}
            {{- '<|im_end|>\n' }}
        {%- elif loop.last %}
            {{- '<|im_end|>\n' }}
        {%- endif %}
    {%- else %}
        {{- '<|im_start|>' + message.role + '\n' + message.content + '<|im_end|>\n' }}
    {%- endif %}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|im_start|>assistant\n' }}
{%- endif %}
{# Copyright 2025-present Unsloth. Apache 2.0 License. Unsloth Chat template fixes #}, example_format: '<|im_start|>system
You are a helpful assistant<|im_end|>
<|im_start|>user
Hello<|im_end|>
<|im_start|>assistant
Hi there<|im_end|>
<|im_start|>user
How are you?<|im_end|>
<|im_start|>assistant
'
main: model loaded
main: server is listening on http://0.0.0.0:12005
main: starting the main loop...
srv  update_slots: all slots are idle
srv    operator(): operator(): cleaning up before exit...
Received second interrupt, terminating immediately.
```

## Function Calling

use `--jinja -fa on --chat-template-file /app/Qwen3-Coder.jinja` to open function calling: https://github.com/ggml-org/llama.cpp/blob/b7342/docs/function-calling.md

`Qwen3-Coder.jinja` is the template for the interface function calling: https://github.com/ggml-org/llama.cpp/blob/b7342/models/templates/Qwen3-Coder.jinja

```shell
docker run -d \
  --name llama-server \
  -p 5006:5006 \
  -v /data1/jiangyy/2llamacpp-b7342/2llamacpp-b7342/llama.cpp:/app \
  llamacppserver:v2 \
  llama-server \
  --jinja \
  -fa on \
  -m /app/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf \
  --chat-template-file /app/Qwen3-Coder.jinja \
  --host 0.0.0.0 \
  --port 5006
```

大模型工具调用是在用户两次（或多次）请求大模型中间，加上自定义函数处理，将处理结果作为第二次大模型的输入得到最终答案。这个过程有点像 rag，函数处理结果类似检索出的知识库内容，作为额外信息提交给模型

还会在提示词中加入[工具调用的提示词](https://huggingface.co/deepseek-ai/DeepSeek-V3.1#toolcall)，帮助模型被请求后**自发**地确定是否调用工具或检索知识库

第一次调用：
```shell
curl http://localhost:5006/v1/chat/completions -d '{
    "model": "Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf",
    "messages": [
        {"role": "system", "content": "You are a chatbot that uses tools/functions. Dont overthink things."},
        {"role": "user", "content": "What is the weather in Istanbul?"}
    ],
    "tools": [{
        "type":"function",
        "function":{
            "name":"get_current_weather",
            "description":"Get the current weather in a given location",
            "parameters":{
                "type":"object",
                "properties":{
                    "location":{
                        "type":"string",
                        "description":"The city and country/state, e.g. `San Francisco, CA`, or `Paris, France`"
                    }
                },
                "required":["location"]
            }
        }
    }]
}'

# {"choices":[{"finish_reason":"tool_calls","index":0,"message":{"role":"assistant","content":null,"tool_calls":[{"type":"function","function":{"name":"get_current_weather","arguments":"{\"location\":\"Istanbul\"}"},"id":"iPsUCwl1rBHV3C2nxJdqIlju7oLGJSX6"}]}}],"created":1765875493,"model":"Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf","system_fingerprint":"b0-unknown","object":"chat.completion","usage":{"completion_tokens":24,"prompt_tokens":309,"total_tokens":333},"id":"chatcmpl-AXxYMparoHy2RK67FTYzT7JRJZCa2qXn","timings":{"cache_n":308,"prompt_n":1,"prompt_ms":57.488,"prompt_per_token_ms":57.488,"prompt_per_second":17.39493459504592,"predicted_n":24,"predicted_ms":1079.521,"predicted_per_token_ms":44.980041666666665,"predicted_per_second":22.232082562543944}}
```

传入工具执行结果第二次调用：
```shell
curl http://localhost:5006/v1/chat/completions -d '{
  "model": "Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf",
  "messages": [
    {"role":"user","content":"What is the weather in Istanbul?"},
    {
      "role":"assistant",
      "tool_calls":[
        {
          "id":"iPsUCwl1rBHV3C2nxJdqIlju7oLGJSX6",
          "type":"function",
          "function":{
            "name":"get_current_weather",
            "arguments":"{\"location\":\"Istanbul\"}"
          }
        }
      ]
    },
    {
      "role":"tool",
      "tool_call_id":"iPsUCwl1rBHV3C2nxJdqIlju7oLGJSX6",
      "content":"{\"temperature\":\"18°C\",\"condition\":\"Partly cloudy\"}"
    }
  ]
}'


# {"choices":[{"finish_reason":"stop","index":0,"message":{"role":"assistant","content":"The current weather in Istanbul is 18°C with partly cloudy conditions."}}],"created":1765875707,"model":"Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_M.gguf","system_fingerprint":"b0-unknown","object":"chat.completion","usage":{"completion_tokens":16,"prompt_tokens":65,"total_tokens":81},"id":"chatcmpl-TzYjHTUauZ0hKmOJX6haDYmCF5fVwmvK","timings":{"cache_n":64,"prompt_n":1,"prompt_ms":49.496,"prompt_per_token_ms":49.496,"prompt_per_second":20.203652820429934,"predicted_n":16,"predicted_ms":615.282,"predicted_per_token_ms":38.455125,"predicted_per_second":26.004336223065195}}
```

完整流程见 [tool_call.py](tool_call.py)