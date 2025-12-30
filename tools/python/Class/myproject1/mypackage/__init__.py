# my_project/
#     ├── package_name/
#     │   ├── __init__.py
#     │   ├── module_a.py
#     │   └── module_b.py
#     └── main.py

# 1.绝对导入
# from package_name.module_name import ClassName

# from mypackage.foo import foo
# from mypackage.bar import bar

# 2.相对导入（不能运行单一文件）

from .foo import foo
from .bar import bar

# 3.通配符wildcard （* ?）导入
# from module_name import *
# __all__是一个字符串列表，显式指定使用 from <module> import * 时，哪些属性会被导入。不指定的话导入所有功能
# 只有在使用 from <module> import * 时才要设置

# __all__ = ['foo','bar']

# 4.导入整个模块，调用时类名前要加模块名
# import module_name; instance = module_name.ClassName()
# 可用别名导入，import module_name as mod; instance = mod.ClassName()