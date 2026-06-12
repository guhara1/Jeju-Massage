#!/usr/bin/env python3
"""IndexNow 일괄 제출 — 빙·네이버 등 IndexNow 참여 엔진에 색인을 즉시 통보한다.

사용법:
    python3 scripts/indexnow_submit.py            # sitemap.xml 의 전체 URL 제출
    python3 scripts/indexnow_submit.py URL [URL]  # 지정한 URL만 제출 (새 글 등록 시)

api.indexnow.org 로 한 번만 보내면 참여 엔진 전체(빙, 네이버, 얀덱스 등)에
공유되므로 엔진별로 따로 보낼 필요가 없다. 구글은 IndexNow 미참여 —
구글은 Search Console sitemap 제출 + scripts/google_indexing_api.py 참고.
"""
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://api.indexnow.org/indexnow"


def sitemap_urls():
    with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def submit(urls):
    host = BASE_URL.split("//", 1)[1].rstrip("/")
    payload = {
        "host": host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL.rstrip('/')}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            print(f"IndexNow 응답: HTTP {res.status} — {len(urls)}개 URL 제출 완료")
    except urllib.error.HTTPError as e:
        # 200/202 외 응답 코드 안내: 400 잘못된 형식, 403 키 불일치,
        # 422 URL이 host와 불일치, 429 과도한 요청
        print(f"IndexNow 오류: HTTP {e.code} — {e.read().decode('utf-8', 'ignore')}")
        sys.exit(1)


if __name__ == "__main__":
    urls = sys.argv[1:] or sitemap_urls()
    if not urls:
        print("제출할 URL이 없습니다. 먼저 python3 build.py 를 실행하세요.")
        sys.exit(1)
    submit(urls)
