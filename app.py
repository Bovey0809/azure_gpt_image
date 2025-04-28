import os
import requests
import base64
from flask import Flask, render_template, request, jsonify, Response
from dotenv import load_dotenv

load_dotenv() # 加载 .env 文件中的环境变量

app = Flask(__name__)

# --- 从环境变量获取配置 ---
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
# 从你的 curl 示例中获取端点和版本
IMAGE_GENERATION_ENDPOINT = "https://imagecoder.openai.azure.com/openai/deployments/gpt-image-1/images/generations?api-version=2025-04-01-preview"
IMAGE_EDIT_ENDPOINT = "https://imagecoder.openai.azure.com/openai/deployments/gpt-image-1/images/edits?api-version=2025-04-01-preview"

if not AZURE_API_KEY:
    raise ValueError("请设置 AZURE_API_KEY 环境变量")

# --- 路由定义 ---

@app.route('/')
def index():
    """渲染主页 HTML"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    """处理图像生成请求"""
    try:
        data = request.json
        prompt = data.get('prompt')
        size = data.get('size', '1024x1024') # 默认尺寸
        quality = data.get('quality', 'medium') # 默认质量
        n = int(data.get('n', 1)) # 默认生成 1 张

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_API_KEY
        }
        payload = {
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "n": n
        }

        response = requests.post(IMAGE_GENERATION_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status() # 如果请求失败 (状态码 >= 400)，则抛出异常

        result = response.json()
        # 假设 API 总是返回至少一张图片的 base64 数据
        b64_json_data = result.get("data", [{}])[0].get("b64_json")

        if not b64_json_data:
             return jsonify({"error": "Failed to get image data from API response"}), 500

        # 直接返回 base64 数据给前端
        return jsonify({"image_b64": b64_json_data})

    except requests.exceptions.RequestException as e:
        # 捕获请求相关的错误 (网络问题、超时、API 错误响应等)
        error_message = f"API request failed: {e}"
        if e.response is not None:
            try:
                # 尝试解析 API 返回的错误详情
                api_error = e.response.json()
                error_message += f" - API Response: {api_error}"
            except ValueError: # JSONDecodeError 的父类
                 error_message += f" - API Response Status: {e.response.status_code}, Body: {e.response.text}"
        app.logger.error(error_message) # 记录详细错误到服务器日志
        return jsonify({"error": "Image generation failed. Check server logs for details."}), 500
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


@app.route('/edit', methods=['POST'])
def edit_image():
    """处理图像编辑请求"""
    try:
        # --- 获取表单数据 ---
        prompt = request.form.get('prompt')
        image_file = request.files.get('image')
        mask_file = request.files.get('mask') # 蒙版是可选的

        if not prompt or not image_file:
            return jsonify({"error": "Prompt and image file are required"}), 400

        headers = {
            "api-key": AZURE_API_KEY
            # Content-Type 会由 requests 库根据 files 参数自动设置为 multipart/form-data
        }

        # --- 准备文件和数据 ---
        files = {
            'image': (image_file.filename, image_file.stream, image_file.mimetype)
        }
        if mask_file:
             files['mask'] = (mask_file.filename, mask_file.stream, mask_file.mimetype)

        data_payload = {
            'prompt': prompt
            # Azure API 可能需要其他参数，根据文档添加
            # 'size': request.form.get('size', '1024x1024'), # 示例：如果 API 支持尺寸
            # 'n': int(request.form.get('n', 1)),       # 示例：如果 API 支持数量
        }

        # --- 发送请求 ---
        response = requests.post(IMAGE_EDIT_ENDPOINT, headers=headers, files=files, data=data_payload)
        response.raise_for_status() # 检查 HTTP 错误

        # --- 处理响应 ---
        result = response.json()
        b64_json_data = result.get("data", [{}])[0].get("b64_json")

        if not b64_json_data:
             return jsonify({"error": "Failed to get edited image data from API response"}), 500

        # 返回 base64 数据
        return jsonify({"image_b64": b64_json_data})

    except requests.exceptions.RequestException as e:
        error_message = f"API request failed: {e}"
        if e.response is not None:
            try:
                api_error = e.response.json()
                error_message += f" - API Response: {api_error}"
            except ValueError:
                 error_message += f" - API Response Status: {e.response.status_code}, Body: {e.response.text}"
        app.logger.error(error_message)
        return jsonify({"error": "Image editing failed. Check server logs for details."}), 500
    except Exception as e:
        app.logger.error(f"An unexpected error occurred during editing: {e}")
        return jsonify({"error": "An internal server error occurred during editing."}), 500


# --- 运行 Flask 应用 ---
if __name__ == '__main__':
    # 使用 host='0.0.0.0' 使其在局域网内可访问
    # debug=True 只在开发时使用，部署时应关闭
    app.run(host='0.0.0.0', port=5002, debug=True)
