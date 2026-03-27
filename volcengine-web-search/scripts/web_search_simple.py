#!/usr/bin/env python3
"""
Simple web search without veadk dependency
"""

import os
import json
import hmac
import hashlib
import base64
import urllib.parse
import datetime
import requests

def web_search(query: str) -> list:
    if not query:
        return []

    ak = os.getenv("VOLCENGINE_ACCESS_KEY")
    sk = os.getenv("VOLCENGINE_SECRET_KEY")
    
    # Decode Base64 secret key
    sk = base64.b64decode(sk).decode()
    
    if not ak or not sk:
        print("AK/SK not found")
        return []

    now = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    date = now[:8]
    
    host = "mercury.volcengineapi.com"
    region = "cn-beijing"
    service = "volc_torchlight_api"
    version = "2025-01-01"
    action = "WebSearch"
    
    content = json.dumps({
        "Query": query,
        "SearchType": "web",
        "Count": 5,
        "NeedSummary": True,
    })
    
    headers = {
        'Content-Type': 'application/json',
        'X-Date': now,
        'Host': host,
    }
    
    # Canonical request
    method = 'POST'
    uri = f'/?Action={action}&Version={version}'
    # Parse query string for signing
    canonical_querystring = f"Action={action}&Version={version}"
    
    headers_str = '\n'.join([f"{k.lower()}:{v}" for k, v in sorted(headers.items())])
    signed_headers = ';'.join([k.lower() for k in sorted(headers.keys())])
    payload_hash = hashlib.sha256(content.encode()).hexdigest()
    
    canonical_request = f"{method}\n/\n{canonical_querystring}\n{headers_str}\n\n{signed_headers}\n{payload_hash}"
    hashed_request = hashlib.sha256(canonical_request.encode()).hexdigest()
    
    # String to sign
    algorithm = 'HMAC-SHA256'
    credential_scope = f"{date}/{region}/{service}/request"
    string_to_sign = f"{algorithm}\n{now}\n{credential_scope}\n{hashed_request}"
    
    # Signature
    kdate = hmac.new(sk.encode(), date.encode(), hashlib.sha256).digest()
    kregion = hmac.new(kdate, region.encode(), hashlib.sha256).digest()
    kservice = hmac.new(kregion, service.encode(), hashlib.sha256).digest()
    ksign = hmac.new(kservice, b'request', hashlib.sha256).digest()
    signature = hmac.new(ksign, string_to_sign.encode(), hashlib.sha256).hexdigest()
    
    # Authorization
    authorization = f"{algorithm} Credential={ak}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
    headers['Authorization'] = authorization
    
    try:
        # Put Action and Version in query string
        resp = requests.post(f"https://{host}/?Action={action}&Version={version}", data=content, headers=headers, timeout=30)
        response = resp.json()
        
        if 'Result' in response and 'WebResults' in response['Result']:
            results = response["Result"]["WebResults"]
            final_results = []
            for result in results:
                final_results.append(result["Summary"].strip())
            return final_results
        else:
            print(f"Response: {response}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python web_search_simple.py <query>")
        sys.exit(1)
    
    query = sys.argv[1]
    results = web_search(query)
    for r in results:
        print(r)