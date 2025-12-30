def foo(input):
    print('foo', input)

# __all__ 和 __name__ 属于模块变量
if __name__ == "__main__": #用于调试当前脚本，包调用时不会运行以下代码
    print("run directly")

print("outside")