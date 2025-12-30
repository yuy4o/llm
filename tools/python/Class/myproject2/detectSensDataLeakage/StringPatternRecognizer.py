from abc import ABC, abstractmethod

class StringPatternRecognizer(ABC):
    """
    Abstract Base Class for recognizing string patterns. 抽象基类
    """
    @abstractmethod
    def find_pattern(self, text: str): # type lint类型注解是可选的，不写的话python会自动类型推断
        # 类型注解只是一个提示，不能强制改变变量类型。如 a:int = 10.65 输出a为10.65
        """find target patterns in given string data. 

        Args:
            text (str): input string
        """
        # pass
        return text
    
    @abstractmethod
    def get_pattern(self):
        """initialize target patterns. 
        """
        pass
    
    @abstractmethod
    def describe(self):
        """provide description of methods and patterns used. e.g. use regular expression or AC automation to implement pattern matching. 
        """
        pass

# 抽象基类 StringPatternRecognizer 的主要作用是定义接口，确保子类实现特定的方法
# 子类必须实现抽象基类中的所有抽象方法，否则无法实例化该子类。如果一个类继承自抽象基类（使用 ABC 作为基类）
# 并且没有实现所有的抽象方法，尝试实例化这个子类会引发 TypeError
# 此处子类 SimplePatternRecognizer 直接实现抽象基类 StringPatternRecognizer 所有的抽象方法，没有依赖父类的实现。因此没有用到 super()
class SimplePatternRecognizer(StringPatternRecognizer):
    def __init__(self, pattern: str): #初始化
        self._pattern = pattern

    def find_pattern(self, text: str) -> bool: #type lint，即使不规定->bool，python会根据函数的实际返回值来决定返回类型
        return self._pattern in text

    def get_pattern(self) -> str:
        return self._pattern
    
    def describe(self) -> str:
        return "this is a simple pattern recognizer"

    def replace_pattern(self, text: str, replacement: str) -> str:
        return text.replace(self._pattern, replacement)

if __name__ == "__main__":
    recognizer = SimplePatternRecognizer("hello") #实例化时的传参看初始化__init__(self, pattern: str)
    text = "hello world"
    
    if recognizer.find_pattern(text):
        print("Pattern found!")
    else:
        print("Pattern not found.")
    
    print("Original text:", text)
    new_text = recognizer.replace_pattern(text, "hi")
    print("Modified text:", new_text)
    print("Recognizer Description:", recognizer.describe())