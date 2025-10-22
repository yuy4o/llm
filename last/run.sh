CUDA_VISIBLE_DEVICES=0,1 nohup llamafactory-cli train examples/train_lora/qwen2vl_lora_sft.yaml >> output.log 2>&1 & echo $! > output.pid
