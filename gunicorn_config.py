# Gunicorn 配置文件
# 增加超时时间以避免 WORKER TIMEOUT 错误

# 工作进程数，通常设置为 CPU 核心数的 2-4 倍
workers = 4

# 工作进程类型
worker_class = 'sync'

# 工作进程超时时间（秒），默认是 30 秒
# 增加到 300 秒 (5 分钟) 以适应长时间运行的请求
timeout = 300

# 绑定的 IP 和端口
bind = '0.0.0.0:8000'

# 日志级别
loglevel = 'info'

# 访问日志格式
accesslog = '-'  # 输出到标准输出
errorlog = '-'   # 错误日志输出到标准错误