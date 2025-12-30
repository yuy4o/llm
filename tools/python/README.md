### 让某个文件夹永远能被 Python import 到

1. 临时修改： 在代码中使用 sys.path.append("/your/path")
2. 使用 PYTHONPATH： 在 .bashrc 中写入 export PYTHONPATH=$PYTHONPATH:/your/path
3. 使用 .pth 文件： 在 Python 的 site-packages 文件夹下创建一个 .pth 后缀的文件，写入路径
