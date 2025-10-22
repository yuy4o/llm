
#  self 指代/引用 类实例化后的对象
class Animal:
    def __init__(this, name): # 构造函数，类实例化时 初始化实例的属性
        this.name = name  # 使用 'this' 代替 'self'
        # __init__ 方法不返回值，默认返回 None
    # 此处speak()可以不写，但最好写。这种强制保留接口的设计确保了接口的一致性，所有子类都有相同的接口
    def speak(this):
        raise NotImplementedError("Subclass must implement this method")

class Dog(Animal):
    def speakk(this):
        return f"{this.name} says Woof!"
    def jump(this):
        return f"{this.name} is jumping"
        

class Cat(Animal):
    def speak(this):
        return f"{this.name} says Meow!"

dog = Dog("Buddy")
cat = Cat("Whiskers")

print(dog.speakk())  # 输出：Buddy says Woof!
print(cat.speak())  # 输出：Whiskers says Meow!
print(dog.jump()) 
print(dog.speak()) # NotImplementedError: Subclass must implement this method 提醒Dog类没有定义speak()函数