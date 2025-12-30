from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import uvicorn
import argparse
from multiprocessing import Process

app = app2 = FastAPI()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

LOCAL_EMBED_PATH = "bge-m3"
LOCAL_RERANK_PATH = "bge-reranker-v2-m3"

embed_model = AutoModel.from_pretrained(LOCAL_EMBED_PATH, return_dict=True)
embed_tokenizer = AutoTokenizer.from_pretrained(LOCAL_EMBED_PATH)
embed_model = embed_model.to(device)

rerank_model = AutoModelForSequenceClassification.from_pretrained(LOCAL_RERANK_PATH)
rerank_model = rerank_model.to(device)

# embedding model
class EmbeddingRequest(BaseModel):
    sentences: list[str]
    max_length: int

@app.post("/embedding")
async def get_embedding(request: EmbeddingRequest):
    try:
        inputs_pt = embed_tokenizer(request.sentences, padding=True, truncation=True, max_length=request.max_length, return_tensors='pt')
        inputs_pt = {k: v.to(device) for k, v in inputs_pt.items()}

        with torch.no_grad():
            outputs_pt = embed_model(**inputs_pt)
        # torch.cuda.empty_cache()
        embedding = outputs_pt.last_hidden_state[:, 0].cpu().detach().numpy()
        norm_arr = np.linalg.norm(embedding, axis=1, keepdims=True)
        embeddings_normalized = embedding / norm_arr

        return {"embeddings": embeddings_normalized.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# rerank model
class InferenceRequest(BaseModel):
    input_ids: list
    attention_mask: list

class InferenceResponse(BaseModel):
    sigmoid_scores: list

@app2.post("/inference", response_model=InferenceResponse)
async def inference(request: InferenceRequest):
    input_ids = torch.tensor(request.input_ids).to(device)
    attention_mask = torch.tensor(request.attention_mask).to(device)
    batch = {'input_ids': input_ids, 'attention_mask': attention_mask}

    with torch.no_grad():
        result = rerank_model(**batch, return_dict=True)
    torch.cuda.empty_cache()
    sigmoid_scores = torch.sigmoid(result.logits.view(-1, )).cpu().detach().numpy().tolist()
    return InferenceResponse(sigmoid_scores=sigmoid_scores)

# 不能直接在 executor.submit 中调用 uvicorn.run 函数，因为这会立即执行，而不是将其提交给线程池执行。
# 相反，你应该传递一个函数对象给 executor.submit。可以将 uvicorn.run 调用包装在一个函数中，然后将这些函数提交给 executor.submit

def run_embed_app():
    uvicorn.run(app, host="0.0.0.0", port=7016)

def run_rerank_app():
    uvicorn.run(app2, host="0.0.0.0", port=7032)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="interface of embedding and rerank models")
    parser.add_argument('--embed', action='store_true', help='use api for embedding model')
    parser.add_argument('--rerank', action='store_true', help='use api for rerank model')

    args = parser.parse_args()

    # 要在同一个脚本中同时运行两个 FastAPI 应用，可以使用多进程，而不是多线程，因为 uvicorn.run 会阻塞线程
    if args.embed and args.rerank:
        embed_process = Process(target=run_embed_app)
        rerank_process = Process(target=run_rerank_app)

        embed_process.start()
        rerank_process.start()
        # join 方法会阻塞主进程，直到调用的子进程完成为止。Process是主进程，embed_process.join() 会阻塞主进程，
        # 直到 embed_process 完成。rerank_process.join() 会阻塞主进程，直到 rerank_process 完成。
        # 这确保了主进程在子进程完成之前不会退出。
        embed_process.join()
        rerank_process.join()
    elif args.embed and not args.rerank:
        run_embed_app()
    elif not args.embed and args.rerank:
        run_rerank_app()
    else:
        print("Please specify '--embed' or '--rerank'")