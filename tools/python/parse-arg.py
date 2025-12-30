import argparse

def main():
    # 创建解析器对象
    parser = argparse.ArgumentParser(description="处理终端传递的参数")

    # 添加参数
    parser.add_argument('--file', type=str, help="输入文件的路径")
    parser.add_argument('--number', type=int, help="一个整数参数")

    # 解析参数
    args = parser.parse_args()

    # 打印参数值
    print(f"文件路径: {args.file}")
    print(f"整数参数: {args.number}")


main()
