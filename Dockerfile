# syntax=docker/dockerfile:1

###################################
# Stage 1: Builder
###################################
FROM python:3.11-slim AS builder

# 设置工作目录为 /app
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir --target /app/deps -r requirements.txt

# 复制所有源代码到 /app/src
COPY src/ /app/src

###################################
# Stage 2: Distroless
###################################
FROM python:3.11-slim

# 设置工作目录为 /app
WORKDIR /app

# 从 builder 阶段复制依赖和源代码
COPY --from=builder /app/deps /app/deps
COPY --from=builder /app/src /app/src

# 设置环境变量和 PYTHONPATH
ENV PYTHONPATH=/app/deps
EXPOSE 8080

# 启动 Flask 应用
CMD ["python3", "/app/src/app.py"]
