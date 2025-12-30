def bar(input):
    print('call bar function', input)

def main():
    foo("import using relative path")

from .foo import foo
# 单一文件中一定要用 相对路径 导入
# 在project根目录下运行 `python -m mypackage.bar`
if __name__ == '__main__':
    main()