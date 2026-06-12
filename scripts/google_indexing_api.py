#!/usr/bin/env python3
"""구글 Indexing API 제출 스크립트.

주의: 구글 Indexing API 는 공식적으로 채용공고(JobPosting)·실시간 방송
(BroadcastEvent) 페이지용입니다. 일반 페이지는 Search Console 에
sitemap.xml 을 제출하는 것이 정석이며, 이 스크립트는 보조 수단입니다.

준비:
 1. Google Cloud 콘솔에서 프로젝트 생성 → "Web Search Indexing API" 사용 설정
 2. 서비스 계정 생성 후 JSON 키 다운로드
 3. Search Console 의 해당 속성에 서비스 계정 이메일을 "소유자"로 추가
 4. pip install google-auth
 5. 환경변수 GOOGLE_SERVICE_ACCOUNT_JSON 에 키 파일 경로 지정

사용법:
    GOOGLE_SERVICE_ACCOUNT_JSON=key.json python3 scripts/google_indexing_api.py            # sitemap 전체
    GOOGLE_SERVICE_ACCOUNT_JSON=key.json python3 scripts/google_indexing_api.py URL [URL]  # 지정 URL만
"""
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPE = "https://www.googleapis.com/auth/indexing"


def sitemap_urls():
    with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def get_token(key_path):
    try:
        from google.auth.transport.requests import Request
        from google.oauth2 import service_account
    except ImportError:
        print("google-auth 가 필요합니다: pip install google-auth")
        sys.exit(1)
    creds = service_account.Credentials.from_service_account_file(
        key_path, scopes=[SCOPE])
    creds.refresh(Request())
    return creds.token


def publish(url, token):
    body = json.dumps({"url": url, "type": "URL_UPDATED"}).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            print(f"OK  {url} (HTTP {res.status})")
            return True
    except urllib.error.HTTPError as e:
        print(f"ERR {url} (HTTP {e.code}) {e.read().decode('utf-8', 'ignore')[:200]}")
        return False


if __name__ == "__main__":
    key_path = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not key_path or not os.path.exists(key_path):
        print(__doc__)
        print("환경변수 GOOGLE_SERVICE_ACCOUNT_JSON 에 서비스 계정 키 경로를 지정하세요.")
        sys.exit(1)
    urls = sys.argv[1:] or sitemap_urls()
    token = get_token(key_path)
    ok = sum(publish(u, token) for u in urls)
    print(f"\n{ok}/{len(urls)} 제출 완료 (기본 할당량: 1일 200건)")
