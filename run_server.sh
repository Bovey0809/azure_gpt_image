#!/bin/bash

# 启动 Gunicorn 服务器，使用更长的超时设置
# 确保已安装 gunicorn: pip install gunicorn

# 激活虚拟环境（如果使用）
# source .venv/bin/activate

# 使用配置文件启动 Gunicorn
echo "Starting Gunicorn server with extended timeout (300s)..."
exec gunicorn --config gunicorn_config.py app:app