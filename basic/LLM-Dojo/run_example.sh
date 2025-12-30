DATA_PATH='/data/jiangyy/LLM-Dojo/data/sft_data.jsonl'
OUTPUT_PATH="."
MODEL_PATH="/data/jiangyy/LLM-Dojo/Qwen2-7B"

# task_type:[sft]  pretrain正在开发
# train_mode:[qlora, lora, full]
# train_args_path: [sft_args,dpo_args]

# deepspeed 启动
deepspeed --master_port 29507 --include localhost:1,2,3 main_train.py\
    --train_data_path "$DATA_PATH" \
    --model_name_or_path "$MODEL_PATH" \
    --max_len 1024 \
    --num_train_epochs 604800 \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 4 \
    --task_type "sft" \
    --train_mode "qlora" \
    --output_dir "$OUTPUT_PATH" \
    --save_strategy "steps" \
    --save_steps 500 \
    --save_total_limit 5 \
    --learning_rate 2e-6 \
    --warmup_steps 10 \
    --logging_steps 1 \
    --lr_scheduler_type "cosine_with_min_lr" \
    --gradient_checkpointing True \
    --report_to "wandb" \
    --deepspeed './train_args/deepspeed_config/ds_config_zero2.json' \
    --bf16 True \

# python main_train.py --train_data_path 数据集路径 --model_name_or_path 模型路径 ......同上述传入参数


# ---------------------------------报错 untimeError: chunk expects at least a 1-dimensional tensor
# CUDA_VISIBLE_DEVICES=2,3 python main_train.py \
#     --train_data_path '/data/jiangyy/LLM-Dojo/data/sft_data.jsonl' \
#     --model_name_or_path '/data/jiangyy/Qwen2-7B' \
#     --output_dir "." \
#     --max_len 1024 \
#     --num_train_epochs 1 \
#     --per_device_train_batch_size 8 \
#     --per_device_eval_batch_size 1 \
#     --gradient_accumulation_steps 4 \
#     --task_type "sft" \
#     --train_mode "qlora" \
#     --save_strategy "steps" \
#     --save_steps 500 \
#     --save_total_limit 5 \
#     --learning_rate 2e-4 \
#     --warmup_steps 10 \
#     --logging_steps 1 \
#     --lr_scheduler_type "cosine_with_min_lr" \
#     --gradient_checkpointing True \
#     --report_to "wandb" \
#     --deepspeed './train_args/deepspeed_config/ds_config_zero2.json' \
#     --bf16 True


# conda activate dojo 
# sh run_example.sh
