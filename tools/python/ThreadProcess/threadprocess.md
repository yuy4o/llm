# https://en.wikipedia.org/wiki/Intel_Core
# 12 Alder Lake 10nm
# 13 Raptor Lake 10nm
# Meteor Lake 7nm   Lunar Lake
# cpu 的大小核（12代Alder lake引入） - Performance core 性能核（要求单线程性能高） Efficient core 能效核（多线程，高并发的小任务）
# 线程数 = 2*P + E  超线程仅适用性能核 - 1个核心对应2个线程
# 进程process 是运行程序的实例，是内存的基本单位unit/子集，共享内存的资源分配
# 线程thread 是进程的执行单元unit/子集，共享进程的资源分配。
#            因为有独立的执行栈和程序计数器，是cpu调度的基本单位

# 进程创建和切换开销大，要分配独立的内存空间和资源如句柄，内存，线程
# 线程创建和切换开销小，只要分配栈和寄存器，可以共享进程的内存和资源如全局变量
# 进程间相对独立，一个任务崩溃不会影响其他进程 - 隔离性和稳定性 适合相对独立的任务
# 线程间互相影响 - 高并发和共享性 适合频繁通信和数据共享的任务


# logistic processor（硬件决定的并行执行单元） 区别于 进程数（软件创建的并发执行单元）。虽然逻辑处理器数目限制了能够同时执行的硬件线程数，
# 但程序可以创建比逻辑处理器更多的线程。操作系统通过时间片轮转（time slicing）和上下文切换（context switching）来管理它们。
# 例如，你可以在具有16个逻辑处理器的系统上运行几百甚至几千个线程，但实际并行运行的线程数不会超过16个。其余的线程将在调度时被暂时挂起

# Python使用threading模块可以创建许多线程，但由于GIL（全局解释器锁），多线程在CPU密集型任务中不会真正并行执行。
# 在I/O密集型任务中，Python线程可以在等待I/O操作时让出GIL，从而允许其他线程运行。

# GIL（全局解释器锁）
# Python的标准实现（CPython）有一个全局解释器锁（GIL），这意味着在任何时刻只有一个线程在执行Python字节码。这限制了Python线程在多核CPU上的并行执行。
# 尽管如此，Python线程在I/O操作（如文件读写、网络请求）期间可以释放GIL，从而允许其他线程运行，这使得多线程在I/O密集型任务中仍然有用。

# 创建大量线程
```python
import threading

def worker(num):
    """线程工作函数"""
    print(f'Worker: {num}')

threads = []
for i in range(1000):  # 创建1000个线程
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()  # 等待所有线程完成
```

# 处理大量并发任务时，建议使用多进程或异步编程。这样可以更有效地利用系统资源，克服GIL的限制，并避免因过多线程导致的开销和性能问题。

# 多进程 使用multiprocessing模块可以绕过GIL限制，因为每个进程都有自己的Python解释器和GIL。多进程适用于CPU密集型任务。
```python
from multiprocessing import Process

def worker(num):
    """进程工作函数"""
    print(f'Worker: {num}')

processes = []
for i in range(1):  # 创建1000个进程
    p = Process(target=worker, args=(i,))
    processes.append(p)
    p.start()

for p in processes:
    p.join()  # 等待所有进程完成
```

# 异步编程 对于I/O密集型任务，可以使用asyncio模块实现异步编程，从而避免大量线程的开销

```python
import asyncio
async def worker(num):
    """异步工作函数"""
    print(f'Worker: {num}')

async def main():
    tasks = []
    for i in range(1000):  # 创建1000个异步任务
        tasks.append(asyncio.create_task(worker(i)))
    await asyncio.gather(*tasks)  # 等待所有任务完成

asyncio.run(main())
```
# CPU密集型任务（如计算密集的算法、图像处理等）在Python中不适合使用多线程，因为GIL限制了并行执行。对于这类任务，可以使用多进程（multiprocessing模块），因为每个进程都有独立的GIL
# 线程数通常不会超过逻辑处理器数，否则会引起频繁的上下文切换，导致性能下降
```python
from multiprocessing import Process

def cpu_bound_task(number):
    # 假设这是一个CPU密集型任务
    result = sum(i*i for i in range(number))
    print(result)

processes = []
for i in range(16):  # 创建16个进程
    p = Process(target=cpu_bound_task, args=(10000000,))
    processes.append(p)
    p.start()

for p in processes:
    p.join()
```
# I/O密集型任务（如网络请求、文件读写等）适合使用多线程或异步编程。多线程可以利用等待I/O操作的时间执行其他线程的代码。
# 可以创建比逻辑处理器数更多的线程，从而有效利用等待I/O的时间执行其他任务。
```python
import threading

def io_bound_task(number):
    # 假设这是一个I/O密集型任务
    import time
    time.sleep(number)
    print(f"Task {number} done")

threads = []
for i in range(100):  # 创建100个线程
    t = threading.Thread(target=io_bound_task, args=(1,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```