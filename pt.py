import torch
import torch.nn as nn
from torch.nn import functional as F

# 一

t = torch.tensor([0,2,3,1,4])

onehot = F.one_hot(t)

x = torch.randn(5,5)

softmax = torch.exp(x)/torch.sum(torch.exp(x), dim=1).reshape(-1,1)

logsoftmax = torch.log(softmax)

llloss = -torch.sum(onehot*logsoftmax)/t.shape[0]

print(llloss)

# 二

logsoftmax = F.log_softmax(x, dim=1)

nllloss = F.nll_loss(logsoftmax,t)

print(nllloss)


# 三

crossentropy = F.cross_entropy(x,t)

print(crossentropy)


try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, Dataset
except ModuleNotFoundError as e:
    print("Error: Required module not found.")
    print("Please ensure that PyTorch is installed in your environment.")
    raise e


class SimpleDataset(Dataset):
    def __init__(self, size):
        self.size = size
        self.data = torch.randn(size, 10)  # 随机生成输入数据，每个样本10维
        self.labels = torch.randint(0, 2, (size,))  # 二分类标签 0 或 1

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        return {"inputs": self.data[index], "labels": self.labels[index]}


class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(10, 50),
            nn.ReLU(),
            nn.Linear(50, 2)
        )

    def forward(self, x):
        return self.fc(x)

ss = SimpleModel()
print(ss.forward(torch.randint(10,(8,10)).float()))

devices = [0, 1]
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if device.type == "cuda":
    torch.cuda.set_device(devices[1])

print(torch.cuda.current_device())

# 初始化数据集和数据加载器
data_size = 1000
batch_size = 64
num_epochs = 5

# # 将数据集按显卡数量划分
# num_gpus = len(devices)
# dataset_per_gpu = [SimpleDataset(data_size // num_gpus) for _ in range(num_gpus)]
# data_loader_per_gpu = [
#     DataLoader(dataset, batch_size=batch_size, shuffle=True) for dataset in dataset_per_gpu
# ]

# # 初始化模型和优化器
# model = SimpleModel()
# model = nn.DataParallel(model, device_ids=devices)  # 使用 DataParallel 包装模型
# model = model.to(device)

# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=0.001)

# # 训练循环
# for epoch in range(num_epochs):
#     print(f"Epoch {epoch + 1}/{num_epochs}")
#     for data_loader in data_loader_per_gpu:
#         for batch in data_loader:
#             # 数据分发到主设备
#             inputs = batch['inputs'].to(device)
#             labels = batch['labels'].to(device)

#             # 前向传播
#             outputs = model(inputs)
#             loss = criterion(outputs, labels)

#             # 反向传播
#             optimizer.zero_grad()
#             loss.backward()

#             # 更新参数
#             optimizer.step()

#     print(f"Epoch {epoch + 1} completed.")

# print("Training completed!")