#!/usr/bin/env python3
"""
Web/Image search using Volcano Engine
"""

import os
import json
import base64
import sys
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo


class TorchlightService(Service):
    def __init__(self, ak, sk):
        service_info = ServiceInfo(
            "mercury.volcengineapi.com",
            {'Content-Type': 'application/json'},
            Credentials(ak, sk, 'volc_torchlight_api', 'cn-beijing'),
            5, 5
        )
        
        api_info = {
            'WebSearch': ApiInfo(
                "POST", 
                "/", 
                {"Action": "WebSearch", "Version": "2025-01-01"}, 
                {}, 
                {}
            ),
        }
        
        super().__init__(service_info, api_info)

    def search(self, query: str, search_type: str = "web", count: int = 5):
        """Search web or image
        
        Args:
            query: search keyword
            search_type: "web" or "image"
            count: number of results
        """
        body = json.dumps({
            'Query': query,
            'SearchType': search_type,
            'Count': count,
            'NeedSummary': True,
        })
        
        response = self.json("WebSearch", {}, body)
        return json.loads(response)


def web_search(query: str, search_type: str = "web", count: int = 5) -> dict:
    """Search and return results
    
    Returns:
        dict with keys: 'web_results' and/or 'image_results'
    """
    ak = os.getenv("VOLCENGINE_ACCESS_KEY")
    sk = os.getenv("VOLCENGINE_SECRET_KEY")
    
    if not ak or not sk:
        print("AK/SK not found")
        return {}

    service = TorchlightService(ak, sk)
    response = service.search(query, search_type, count)
    
    result = {}
    if 'Result' in response:
        if 'WebResults' in response['Result'] and response['Result']['WebResults']:
            result['web_results'] = []
            for r in response['Result']['WebResults']:
                result['web_results'].append(r['Summary'].strip())
        
        if 'ImageResults' in response['Result'] and response['Result']['ImageResults']:
            result['image_results'] = []
            for r in response['Result']['ImageResults']:
                img_info = {
                    'title': r.get('Title', ''),
                    'url': r.get('Image', {}).get('Url', ''),
                    'width': r.get('Image', {}).get('Width', 0),
                    'height': r.get('Image', {}).get('Height', 0),
                }
                result['image_results'].append(img_info)
    
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python web_search_volc.py <query> [web|image]")
        sys.exit(1)
    
    query = sys.argv[1]
    search_type = sys.argv[2] if len(sys.argv) > 2 else "web"
    
    results = web_search(query, search_type)
    
    if 'web_results' in results:
        print("=== Web Results ===")
        for r in results['web_results']:
            print(r)
            print()
    
    if 'image_results' in results:
        print("=== Image Results ===")
        for i, r in enumerate(results['image_results'], 1):
            print(f"{i}. {r['title']}")
            print(f"   Size: {r['width']}x{r['height']}")
            print(f"   URL: {r['url']}")
            print()