#!/usr/bin/env python3
"""
火山引擎图片识别脚本
用法: python recognize.py <图片路径或URL> [--model 模型名称]
"""

import os
import sys
import base64
import argparse
import json
from pathlib import Path

try:
    import requests
except ImportError:
    print("需要安装 requests: pip install requests")
    sys.exit(1)


# 默认使用视觉模型（推荐）
DEFAULT_MODEL = 'doubao-1-5-vision-pro-32k-250115'

# 备用 volc-vision API 模型
VOLC_VISION_MODELS = {
    'general_object_detection': 'GeneralDetection',
    'ocr': 'OCR',
    'scene_classification': 'SceneClassification',
    'face_detection': 'FaceDetection',
}


def get_api_token():
    """获取 API Token"""
    token = os.environ.get('VOLCENGINE_API_TOKEN')
    if not token:
        raise ValueError("请设置环境变量 VOLCENGINE_API_TOKEN")
    return token


def encode_image(image_path: str) -> str:
    """将图片编码为 base64"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def recognize_with_vision_model(image_source: str, prompt: str = "请详细描述这张图片") -> str:
    """使用视觉模型识别图片（推荐）"""
    
    token = get_api_token()
    
    # 确定图片来源类型
    if image_source.startswith(('http://', 'https://')):
        image_url = image_source
    elif Path(image_source).exists():
        image_url = f"data:image/webp;base64,{encode_image(image_source)}"
    else:
        raise ValueError("图片路径无效或不存在")
    
    url = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': DEFAULT_MODEL,
        'messages': [
            {
                'role': 'user',
                'content': [
                    {'type': 'image_url', 'image_url': {'url': image_url}},
                    {'type': 'text', 'text': prompt}
                ]
            }
        ],
        'max_tokens': 500
    }
    
    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    
    result = resp.json()
    return result['choices'][0]['message']['content']


def recognize(image_source: str, mode: str = 'vision', prompt: str = None) -> str:
    """识别图片（默认使用视觉模型）"""
    
    if mode == 'vision':
        return recognize_with_vision_model(image_source, prompt or "请详细描述这张图片")
    else:
        raise ValueError(f"未知模式: {mode}")


def main():
    parser = argparse.ArgumentParser(description='火山引擎图片识别')
    parser.add_argument('image', help='图片路径或URL')
    parser.add_argument('--prompt', '-p', default='请详细描述这张图片', help='识别提示词')
    parser.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    
    try:
        result = recognize(args.image, prompt=args.prompt)
        
        print(result)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"\n结果已保存到: {args.output}")
            
    except Exception as e:
        print(f"识别失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()