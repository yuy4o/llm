https://github.com/Wan-Video/Wan2.1/tree/ae487cc653b4a1791fec8201af20d2102a2514f3

command:
```python
python generate.py \
  --task t2v-1.3B \
  --size 832*480 \
  --frame_num 41 \
  --ckpt_dir /data1/jiangyy/imagemodels/Wan2.1-T2V-1.3B \
  --sample_shift 8 \
  --sample_guide_scale 6 \
  --prompt "Two anthropomorphic cats in comfy boxing gear and bright gloves fight intensely on a spotlighted stage."
```

log:
```shell
[2025-12-27 17:53:46,126] INFO: offload_model is not specified, set to True.
[2025-12-27 17:53:46,126] INFO: Generation job args: Namespace(task='t2v-1.3B', size='832*480', frame_num=41, ckpt_dir='/data1/jiangyy/imagemodels/Wan2.1-T2V-1.3B', offload_model=True, ulysses_size=1, ring_size=1, t5_fsdp=False, t5_cpu=False, dit_fsdp=False, save_file=None, src_video=None, src_mask=None, src_ref_images=None, prompt='Two anthropomorphic cats in comfy boxing gear and bright gloves fight intensely on a spotlighted stage.', use_prompt_extend=False, prompt_extend_method='local_qwen', prompt_extend_model=None, prompt_extend_target_lang='zh', base_seed=3766484517603319279, image=None, first_frame=None, last_frame=None, sample_solver='unipc', sample_steps=50, sample_shift=8.0, sample_guide_scale=6.0)
[2025-12-27 17:53:46,126] INFO: Generation model config: {'__name__': 'Config: Wan T2V 1.3B', 't5_model': 'umt5_xxl', 't5_dtype': torch.bfloat16, 'text_len': 512, 'param_dtype': torch.bfloat16, 'num_train_timesteps': 1000, 'sample_fps': 16, 'sample_neg_prompt': '色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走', 't5_checkpoint': 'models_t5_umt5-xxl-enc-bf16.pth', 't5_tokenizer': 'google/umt5-xxl', 'vae_checkpoint': 'Wan2.1_VAE.pth', 'vae_stride': (4, 8, 8), 'patch_size': (1, 2, 2), 'dim': 1536, 'ffn_dim': 8960, 'freq_dim': 256, 'num_heads': 12, 'num_layers': 30, 'window_size': (-1, -1), 'qk_norm': True, 'cross_attn_norm': True, 'eps': 1e-06}
[2025-12-27 17:53:46,126] INFO: Input prompt: Two anthropomorphic cats in comfy boxing gear and bright gloves fight intensely on a spotlighted stage.
[2025-12-27 17:53:46,126] INFO: Creating WanT2V pipeline.
[2025-12-27 17:54:43,664] INFO: loading /data1/jiangyy/imagemodels/Wan2.1-T2V-1.3B/models_t5_umt5-xxl-enc-bf16.pth
[2025-12-27 17:54:51,240] INFO: loading /data1/jiangyy/imagemodels/Wan2.1-T2V-1.3B/Wan2.1_VAE.pth
[2025-12-27 17:54:51,600] INFO: Creating WanModel from /data1/jiangyy/imagemodels/Wan2.1-T2V-1.3B
[2025-12-27 17:54:54,371] INFO: Generating video ...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████| 50/50 [01:25<00:00,  1.71s/it]
[2025-12-27 17:56:36,101] INFO: Saving generated video to t2v-1.3B_832*480_1_1_Two_anthropomorphic_cats_in_comfy_boxing_gear_and__20251227_175636.mp4
raw video shape: torch.Size([3, 41, 480, 832])
frames shape: (41, 480, 832, 3)
[2025-12-27 17:56:37,105] INFO: Finished.
(base) [jiangyy@youln-a100-4 Wan2.1-main]$ ffprobe -v error -select_streams v:0 -show_entries stream=avg_frame_rate,duration -of default=noprint_wrappers=1 t2v-1.3B_*.mp4
avg_frame_rate=16/1
duration=2.562500
```