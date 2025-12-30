# # 使用一个基础的Docker镜像，可以根据你的需求选择合适的镜像
# FROM continuumio/miniconda3

# # 设置pip主要源和备用源(切换为国内源，如不是在国内请忽略)
# RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
#     pip config set global.extra-index-url https://pypi.org/simple/

# # 设置工作目录
# WORKDIR /app

# # 复制Conda环境的配置文件（environment.yml）到容器中
# COPY env.yml .

# # 使用Conda创建环境
# RUN conda env create -f env.yml

# # 激活Conda环境
# RUN echo "source activate my_conda_env" > ~/.bashrc
# ENV PATH /data/jiangyy/miniconda3/envs/my_conda_env/bin:$PATH

# # 添加你的应用程序代码和文件到容器中
# COPY . .

# # 定义容器启动时运行的命令
# CMD ["python", "your_script.py"]

# -----------------------
# 1.执行python文件
# FROM continuumio/miniconda3
# COPY environment.yml /tmp/environment.yml
# RUN conda env create -f /tmp/environment.yml
# SHELL ["conda", "run", "-n", "test", "/bin/bash", "-c"]
# COPY your_script.py /your_script.py
# ENTRYPOINT ["conda", "run", "-n", "test", "--no-capture-output", "python", "/your_script.py"]
# -----------------------

# -----------------------
# 2.执行带python的sh文件
# FROM continuumio/miniconda3
# COPY environment.yml /tmp/environment.yml
# RUN conda env create -f /tmp/environment.yml
# SHELL ["conda", "run", "-n", "test", "/bin/bash", "-c"]
# start.sh 会调用 your_script.py，不能忘记 COPY
# COPY your_script.py /your_script.py
# COPY start.sh /start.sh
# ENTRYPOINT ["conda", "run", "-n", "test", "--no-capture-output", "/bin/bash", "/start.sh"]
# -----------------------


# 3.打包环境 交互式shell
FROM continuumio/miniconda3
COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml
# 失败ENTRYPOINT ["conda", "run", "-n", "test", "--no-capture-output", "/bin/bash"]
ENTRYPOINT ["/bin/bash", "-c", "source activate test && exec bash"]