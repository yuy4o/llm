from .m1 import foo
from .m2 import bar

# __all__是一个字符串列表，显式指定使用 from <module> import * 时，哪些属性会被导入。
# 不指定的话所有都会被导入
# 只针对from <module> import *表达，无效from mypackage import foo,bar 
# __all__ = ['foo','bar']
