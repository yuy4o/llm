from transformers import AutoModel
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained("/data/wenhr/modelhub/QwQ-32B-Preview")
# model = AutoModel.from_pretrained("/data/wenhr/modelhub/QwQ-32B-Preview")
print(model)
# for name, param in model.named_parameters():
#     print(name)
#     print(param.dtype)
model.save_pretrained_gguf("model",tokenizer,quantization_method="f16")
