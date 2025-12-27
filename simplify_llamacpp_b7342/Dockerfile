# version 1
FROM ubuntu:22.04 AS builder

RUN apt-get update && apt-get install -y \
    build-essential cmake git libomp-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY . .

RUN cmake -S . -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLAMA_BUILD_SERVER=ON \
    -DLLAMA_BUILD_TESTS=OFF \
    -DLLAMA_BUILD_EXAMPLES=OFF \
    -DLLAMA_BUILD_BENCHMARKS=OFF \
    -DLLAMA_CURL=OFF \ 
    && cmake --build build -j$(nproc)

RUN mkdir -p /out/bin /out/lib \
 && find build -type f -name "llama-server" -exec cp {} /out/bin/ \; \
 && find build -type f -name "*.so*" -exec cp -P {} /out/lib/ \;

FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /out/bin/llama-server /usr/local/bin/
COPY --from=builder /out/lib/*.so* /usr/local/lib/

RUN ldconfig


# version 2

# FROM ubuntu:22.04 AS builder

# RUN apt-get update && apt-get install -y \
#     build-essential cmake git libomp-dev \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /src
# COPY . /src

# RUN cmake -B build \
#     -DCMAKE_BUILD_TYPE=Release \
#     -DLLAMA_BUILD_SERVER=ON \
#     -DLLAMA_BUILD_TESTS=OFF \
#     -DLLAMA_BUILD_EXAMPLES=OFF \
#     -DLLAMA_BUILD_BENCHMARKS=OFF \
#     && cmake --build build -j$(nproc) \
#     && cmake --install build

# FROM ubuntu:22.04

# RUN apt-get update && apt-get install -y \
#     libgomp1 \
#     && rm -rf /var/lib/apt/lists/*

# COPY --from=builder /usr/local/bin/llama-server /usr/local/bin/
# COPY --from=builder /usr/local/lib/libllama*.so* /usr/local/lib/
# COPY --from=builder /usr/local/lib/libggml*.so* /usr/local/lib/

# RUN ldconfig



# official version from https://github.com/ggml-org/llama.cpp/blob/b7342/.devops/cpu.Dockerfile

# FROM ubuntu:22.04 AS builder

# ARG TARGETARCH

# RUN apt-get update && \
#     apt-get install -y \
#         build-essential \
#         git \
#         cmake \
#         libcurl4-openssl-dev \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /src
# COPY . .

# RUN if [ "$TARGETARCH" = "amd64" ] || [ "$TARGETARCH" = "arm64" ]; then \
#         cmake -S . -B build \
#           -DCMAKE_BUILD_TYPE=Release \
#           -DGGML_NATIVE=OFF \
#           -DLLAMA_BUILD_SERVER=ON \
#           -DLLAMA_BUILD_TESTS=OFF \
#           -DLLAMA_BUILD_EXAMPLES=OFF \
#           -DLLAMA_BUILD_BENCHMARKS=OFF \
#           -DGGML_BACKEND_DL=ON \
#           -DGGML_CPU_ALL_VARIANTS=ON ; \
#     else \
#         echo "Unsupported architecture: $TARGETARCH" && exit 1 ; \
#     fi && \
#     cmake --build build -j $(nproc)

# FROM ubuntu:22.04
# RUN apt-get update && \
#     apt-get install -y \
#         libgomp1 \
#         curl \
#     && rm -rf /var/lib/apt/lists/*

# COPY --from=builder /src/build/bin/llama-server /usr/local/bin/

# COPY --from=builder /src/build/**/*.so* /usr/local/lib/

# RUN ldconfig

# ENV LLAMA_ARG_HOST=0.0.0.0

# HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1

# ENTRYPOINT ["llama-server"]
