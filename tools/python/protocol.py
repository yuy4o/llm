def code_version_1():
    class Greeter:
        def greet(self) -> str:
            ...

    class EnglishGreeter(Greeter):
        def greet(self) -> str:
            return "Hello!"

    class SpanishGreeter(Greeter):
        def greet(self) -> str:
            return "¡Hola!"

    def greet_someone(greeter: Greeter) -> str:
        return greeter.greet()

    # 实例化具体的 Greeter 类
    english_greeter = EnglishGreeter()
    spanish_greeter = SpanishGreeter()

    # 使用 greet_someone 函数
    print(greet_someone(english_greeter))  # 输出: Hello!
    print(greet_someone(spanish_greeter))  # 输出: ¡Hola!
def code_version_2():
    from typing import Protocol  # 允许我们定义和使用灵活的、松耦合的接口，使代码更加模块化和可扩展
    # 定义一个协议
    class Greeter(Protocol):
        def greet(self) -> str:
            ...
    #... Ellipsis，用于表示未实现的功能或占位符。它可以用于不同的上下文，在定义协议（Protocol）或抽象基类
    # （Abstract Base Classes,ABC）时，... 表示一个方法的声明，但不提供具体的实现

    # 定义一个类，实现 Greeter 协议
    class EnglishGreeter:
        def greet(self) -> str:
            return "Hello!"

    # 定义另一个类，实现 Greeter 协议
    class SpanishGreeter:
        def greet(self) -> str:
            return "¡Hola!"

    # 定义一个函数，接受任何实现了 Greeter 协议的对象
    def greet_someone(greeter: Greeter) -> str:
        return greeter.greet()

    # 实例化具体的 Greeter 类
    english_greeter = EnglishGreeter()
    spanish_greeter = SpanishGreeter()

    # 使用 greet_someone 函数
    print(greet_someone(english_greeter))  # 输出: Hello!
    print(greet_someone(spanish_greeter))  # 输出: ¡Hola!


if __name__ == "__main__":
    # 1，交互输入
    version = input("Enter version to run (1 or 2): ")
    if version == "1":
        print("Abstract Base Class Usage:")
        code_version_1()
    elif version == "2":
        print("Protocol Usage:")
        code_version_2()
    else:
        print("Invalid version.")

    # 2，命令行参数
    # import sys
    # print(sys.argv)
    # if len(sys.argv) != 2:
    #     print("Usage: python switch_code.py <version>")
    #     sys.exit(1)
    #
    # version = sys.argv[1]
    # if version == "1":
    #     print("Abstract Base Class Usage:")
    #     code_version_1()
    # elif version == "2":
    #     print("Protocol Usage:")
    #     code_version_2()
    # else:
    #     print("Invalid version.")