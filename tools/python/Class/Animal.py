#  self 指代/引用 类实例化后的对象
class Animal:
    def __init__(this, name):  # 构造函数，类实例化时 初始化实例的属性
        this.name = name  # 使用 'this' 代替 'self'
        # __init__ 方法不返回值，默认返回 None
    # 此处speak()可以不写，但最好写。这种强制保留接口的设计确保了接口的一致性，所有子类都有相同的接口

    def speak(this):
        raise NotImplementedError("Subclass must implement this method")


class Dog(Animal):
    def __init__(this, name, weight):
        super().__init__(name)  # 继承父类
        this.age = 16
        this.weight = weight*2

    def speakk(this):
        return f"{this.name} says Woof {this.age} with weight {this.weight}!"

    def jump(this):
        return f"{this.name} is jumping"


class Cat(Animal):
    def speak(this):
        return f"{this.name} says Meow!"


# 父类和子类的参数一起传递给子类的 __init__ 方法。在 Dog 类的 __init__ 方法中，首先调用父类 Animal 的 __init__ 方法来初始化 name 属性，然后初始化 weight 属性
# 传参是按照 class Dog(Animal): def __init__(this, name,weight), init里的参数顺序
dog = Dog("Buddy", 120)
cat = Cat("Whiskers")
print(cat.speak())  # 输出：Whiskers says Meow!

print(dog.speakk())  # 输出：Buddy says Woof!
print(dog.jump())
print(dog.speak())# NotImplementedError: Subclass must implement this method 提醒Dog类没有定义speak()函数