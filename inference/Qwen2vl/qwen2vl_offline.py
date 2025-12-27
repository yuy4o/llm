from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch

# qwen2-vl-2B 44bit 3.5G显存  8bit 4.2G显存   16bit 6G显存   32bit 11.5G显存

# ################# CUDA_VISIBLE_DEVICES=2 python qwen2vl.py 外部指定能看到哪几张卡 #################
# # 4bit quantization
# from transformers import BitsAndBytesConfig
# quant_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
# model = Qwen2VLForConditionalGeneration.from_pretrained(
#     "/data1/jiangyy/imagemodels/Qwen2-VL-2B-Instruct",
#     quantization_config=quant_config,
#     device_map="auto",
# )

# # 8bit quantization
model = Qwen2VLForConditionalGeneration.from_pretrained(
   "/data1/jiangyy/imagemodels/Qwen2-VL-2B-Instruct",
   load_in_8bit=True,
   device_map="auto"
)

# default: Load the model on the available device(s)
# model = Qwen2VLForConditionalGeneration.from_pretrained(
#    "/data1/jiangyy/imagemodels/Qwen2-VL-2B-Instruct", torch_dtype=torch.bfloat16, device_map="auto"
# )

# We recommend enabling flash_attention_2 for better acceleration and memory saving, especially in multi-image and video scenarios.
# model = Qwen2VLForConditionalGeneration.from_pretrained(
#     "/data1/jiangyy/imagemodels/Qwen2-VL-2B-Instruct",
#     torch_dtype=torch.bfloat16,
#     attn_implementation="flash_attention_2",
#     device_map="auto",
# )

# default processer
processor = AutoProcessor.from_pretrained("/data1/jiangyy/imagemodels/Qwen2-VL-2B-Instruct")

# The default range for the number of visual tokens per image in the model is 4-16384. You can set min_pixels and max_pixels according to your needs, such as a token count range of 256-1280, to balance speed and memory usage.
# min_pixels = 256*28*28
# max_pixels = 1280*28*28
# processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-2B-Instruct", min_pixels=min_pixels, max_pixels=max_pixels)

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "file:///data1/jiangyy/models/example.png",
            },
            {"type": "text", "text": "中文解释这张图片内容"},
        ],
    }
]

# Preparation for inference
text = processor.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
image_inputs, video_inputs = process_vision_info(messages)
inputs = processor(
    text=[text],
    images=image_inputs,
    videos=video_inputs,
    padding=True,
    return_tensors="pt",
)

inputs = inputs.to("cuda")

# Inference: Generation of the output
generated_ids = model.generate(**inputs, max_new_tokens=512)
generated_ids_trimmed = [
    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
]
output_text = processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)
print(output_text)


# ################# python qwen2vl.py 代码内部指定设备 #################
# model = Qwen2VLForConditionalGeneration.from_pretrained(
#    "/data1/jiangyy/imagemodels/Qwen2-VL-2B-Instruct", torch_dtype=torch.bfloat16
# ).to(torch.device("cuda:2"))

# processor = AutoProcessor.from_pretrained("/data1/jiangyy/imagemodels/Qwen2-VL-2B-Instruct")

# messages = [
#     {
#         "role": "user",
#         "content": [
#             {
#                 "type": "image",
#                 "image": "file:///data1/jiangyy/models/example.png",
#             },
#             {"type": "text", "text": "中文解释这张图片内容"},
#         ],
#     }
# ]

# # Preparation for inference
# text = processor.apply_chat_template(
#     messages, tokenize=False, add_generation_prompt=True
# )
# image_inputs, video_inputs = process_vision_info(messages)
# inputs = processor(
#     text=[text],
#     images=image_inputs,
#     videos=video_inputs,
#     padding=True,
#     return_tensors="pt",
# )
# inputs = inputs.to(torch.device("cuda:2"))

# generated_ids = model.generate(**inputs, max_new_tokens=64)
# generated_ids_trimmed = [
#     out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
# ]
# output_text = processor.batch_decode(
#     generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
# )
# print(output_text)