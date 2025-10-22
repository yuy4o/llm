# 资料来源：https://github.com/retepViolet/Transformer-/

import torch, os, math
from torch.utils.data import Dataset
from torch import nn, Tensor
from transformers import BertTokenizer # type: ignore
import string
import argparse

path = os.getcwd()
print(path)


class Tokenizer:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.vocab_size = self.tokenizer.vocab_size
    
    def encode(self, text:str)->list:
        return self.tokenizer(text, return_tensors='pt')['input_ids'][0].tolist()
    
    def decode(self, tokens:list)->str:
        return self.tokenizer.decode(tokens)

tokenizer = Tokenizer()

# text = "你好世界，hello world"
# encoded_input = tokenizer.encode(text)
# print(encoded_input)
# print(tokenizer.decode(encoded_input))

class Transformer_Dataset(Dataset):
    def __init__(self, dir:str):
        self.tokens = ''
        self.vocab_size = tokenizer.vocab_size
        self.data = self.read_file(dir)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]
    
    def one_hot(self, tokens:list, value:float):
        res = []
        for i in tokens:
            vec = torch.full([self.vocab_size], (1-value)/self.vocab_size)
            vec[i] = value
            res.append(vec)
        return torch.stack(res)

    def read_file(self, dir: str):
        data = []
        with open(dir, 'r') as file:
            self.tokens = tokenizer.encode(file.read())
            x = self.one_hot(self.tokens[:-1], 1)
            y = self.one_hot(self.tokens[1:], 1)
            data.append((x, y))
        return data

class self_attention(nn.Module):
    def __init__(self, d, dk): 
        # d 是词向量维度，dk 是映射后的维度
        super().__init__()
        self.dk = dk
        self.q = nn.Linear(d, dk)
        self.k = nn.Linear(d, dk)
        self.v = nn.Linear(d, dk)

    def attention(self, Q:Tensor, K:Tensor, V:Tensor, mask:Tensor):
        return torch.softmax((Q @ K.transpose(-2, -1)) / self.dk**0.5 + mask, dim = -1) @ V
        
    def forward(self, x:tuple):
        x, mask = x
        Q = self.q(x)
        K = self.k(x)
        V = self.v(x)
        return self.attention(Q, K, V, mask)


class decoder(nn.Module):
    def __init__(self, head_num, d, dk, dff):
        super().__init__()
        self.heads = nn.ModuleList()    # 多头注意力机制
        for _ in range(head_num):
            self.heads.append(self_attention(d, dk))
        self.o = nn.Linear(head_num*dk, d)
        self.norm1 = nn.LayerNorm(d)
        self.ffn = nn.Sequential(   # Position-wise Feed-Forward Networks
            nn.Linear(d, dff),
            nn.ReLU(),
            nn.Linear(dff, d),
        )
        self.norm2 = nn.LayerNorm(d)
    
    def forward(self, x:tuple):
        x, mask = x
        heads_res = []
        for head in self.heads: # 可以并行
            heads_res.append(head((x, mask)))
        a = self.o(torch.concat(heads_res, dim = -1))
        b = self.norm1(a+x)
        y = self.norm2(self.ffn(b)+b)   # add & norm
        return (y, mask)


class transformer(nn.Module):
    def __init__(self, decoder_num=6, head_num=8, d=512, dk=64, dff=2048):
        super().__init__()
        self.mask = Tensor()
        self.zero_mask = Tensor()
        self.pos_code = Tensor()
        self.d = d
        self.vocab_size = tokenizer.vocab_size
        self.decoders = nn.Sequential()
        for _ in range(decoder_num):
            self.decoders.append(decoder(head_num, d, dk, dff))
        self.last_linear = nn.Linear(d, self.vocab_size)
        self.softmax = nn.Softmax(dim=-1)

    def get_mask(self, sequence_len): # mask 机制
        if not self.training:
            if sequence_len != len(self.zero_mask):
                self.zero_mask = torch.zeros(sequence_len, sequence_len)
            return self.zero_mask
        if sequence_len != len(self.mask):
            self.mask = torch.zeros(sequence_len, sequence_len)
            for i in range(sequence_len):
                for j in range(sequence_len):
                    if j>i: self.mask[i][j] = -1e9
        return self.mask

    def pos_encode(self, sequence_len): # 位置嵌入
        if len(self.pos_code) == sequence_len:
            return self.pos_code
        self.pos_code = []
        for pos in range(sequence_len): 
            buf = []
            for i in range(self.d):
                value = math.sin(pos/1e4**(i/self.d)) if i % 2 == 0  \
                        else math.cos(pos/1e4**((i-1)/self.d))
                buf.append(value)
            self.pos_code.append(torch.tensor(buf))
        self.pos_code = torch.stack(self.pos_code)
        return self.pos_code

    # x 应是一个tensor，纵向是序列长度，横向是vocab size长度的one hot向量
    def forward(self, x:Tensor):
        sequence_len = x.shape[-2]
        x = x @ self.last_linear.weight  # embedding, share weight matrix     
        x = x * self.d**0.5 + self.pos_encode(sequence_len) # 位置嵌入
        y, _ = self.decoders((x, self.get_mask(sequence_len)))
        y = self.last_linear(y) 
        # 输出的每个 vector 表示对现在位置的下一个词的预测，表示未知的词的只有最后一个vector。
        return y #self.softmax(y)

def train(epoch:int):
    loss_fn = nn.CrossEntropyLoss()
    model.train() # 设置为训练模式
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
    for i in range(epoch):
        loss = 0
        for x, y in data:
            pred = model(x)
            loss = loss_fn(pred, y)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        if (i+1) % 10 == 0:
            print(f'Epoch: {i+1}; Loss: {loss.item()}')
            
def run_model(input:str):
    tokens = tokenizer.encode(input)[:-1]
    pred, cnt = 101, 0
    while pred!=102 and cnt<=500:
        x = data.one_hot(tokens, 1)
        pred = runner(x)[-1].argmax(dim = -1).item()

        word = tokenizer.decode([pred])
        if word.find('##') == -1 and word[0] not in string.punctuation:
            print(' ' + word, end='')
        else: print(word.replace('##', ''), end='')

        tokens.append(pred)
        cnt += 1
        if cnt % 20 == 0:
            print('')
    # print(tokenizer.decode(tokens))

# x, y = data[0]
# tokenizer.decode(runner(x).argmax(dim = -1))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="training and inference phase for gpt")
    parser.add_argument('--train', action='store_true', help='run training')
    parser.add_argument('--infer', action='store_true', help='run inference')

    args = parser.parse_args()
    data = Transformer_Dataset(path+'/content.txt')
    
    if args.train and args.infer:
        # 模型训练
        model = transformer(decoder_num=3, head_num=4, d = 256, dk = 64, dff = 512)
        train(100)
        torch.save(model.state_dict(), 'weights.pth')
        # 模型推理
        runner = transformer(decoder_num=3, head_num=4, d = 256, dk = 64, dff = 512)
        runner.load_state_dict(torch.load('weights.pth'))
        runner.eval()
        run_model('')
    elif args.train:
        model = transformer(decoder_num=3, head_num=4, d = 256, dk = 64, dff = 512)
        train(100)
        torch.save(model.state_dict(), 'weights.pth')
    elif args.infer:
        runner = transformer(decoder_num=3, head_num=4, d = 256, dk = 64, dff = 512)
        runner.load_state_dict(torch.load('weights.pth'))
        runner.eval()
        run_model('')
    else:
        print("Please specify --train or --infer")


# # print(tokenizer.decode(data.tokens[:10]))


# ## 敏感性分析
# 
# ### 参数一
# decoder_num=3, head_num=4, d=256, dk=64, dff=512
# 
# Adam, lr=0.0003, epoch=100
# 
# Loss: 0.0015870328061282635
# 
# 准确输出文章全部内容
# 
# ### 参数二
# decoder_num=3, head_num=4, d=64, dk=16, dff=128
# 
# Loss: 0.032027047127485275
# 
# 内容输出较为准确，有些许误差
# 
# ### 参数三
# decoder_num=2, head_num=2, d=32, dk=16, dff=64
# 
# Loss: 0.51451575756073
# 
# 无法输出正常内容
# 
# 
# ### 去除位置编码
# 使用参数一
# 
# Loss: 0.04319296404719353
# 
# 输出内容很不准确
# 
# ### 去除 mask
# 使用参数一
# 
# Loss: 0.0039401608519256115
# 
# 输出内容准确，怀疑是过拟合导致的
# 
# 使用参数二
# 
# Loss: 0.0312423724681139
# 
# 虽然 Loss 和有 mask 时几乎一致，但输出内容很不准确
# 
# ### Q、K、V 共享线性层
# 使用参数一
# 
# Loss: 0.0018703739624470472
# 
# 输出内容非常准确
# 
# 使用参数二
# 
# Loss: 0.03298478573560715
# 
# 输出内容非常准确
# 
# ### 去除 softmax 中的除以 $\sqrt d$
# 使用参数二
# 
# Loss: 0.037089236080646515
# 
# 输出内容有很多误差，梯度消失
# 
# ### 去除位置编码前的乘以 $\sqrt d$
# 使用参数二
# 
# Loss: 0.036799754947423935
# 
# 输出很准确，过拟合导致
# 
# ### 去除残差
# 使用参数二
# 
# Loss: 4.3070549964904785
# 
# 无法正常输出
# 
# ### 去除标准化
# 使用参数二
# 
# Loss: 0.0009859238052740693
# 
# 无法正常输出，原因是超级过拟合，当设置成训练模式时就可以了
# 
# ### 去除 ffn
# 使用参数二
# 
# Loss: 0.09225127100944519
# 
# 无法正常输出，欠拟合