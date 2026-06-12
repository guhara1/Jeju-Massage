# 제주 예쁨 마사지 — 제주 출장마사지·홈타이 안내 사이트

제주특별자치도 전지역 방문 관리(출장마사지·홈타이) 안내용 정적 사이트입니다.
예약전화: **0508-202-4723**

## 구조

- 정적 HTML 사이트 — 어느 호스팅(GitHub Pages, Netlify, 일반 웹서버)에서든 그대로 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`)도 저장소에 포함

```
build.py              # 빌드 스크립트 (레이아웃·글자수 검사·sitemap 생성)
content/
  site.py             # 상호·전화·BASE_URL·메뉴 구조
  main.py             # 메인 페이지 (+ LocalBusiness/FAQPage JSON-LD)
  massage.py          # 제주 출장마사지 안내 페이지
  region_hubs.py      # 지역 허브: 제주 전체 / 제주시 / 서귀포시
  areas_jeju_eup.py   # 제주시 읍·면 7개
  areas_jeju_dong1.py # 제주시 동 8개 (일도~봉개)
  areas_jeju_dong2.py # 제주시 동 7개 (아라~도두)
  areas_seogwipo1.py  # 서귀포 읍·면 5개 + 원도심 동 3개
  areas_seogwipo2.py  # 서귀포 동 9개 (천지~예래)
  places1.py          # 교통거점 허브 + 공항·항만·터미널·중문 8개
  places2.py          # 시청·대학·상권·해변·관광지 거점 10개
  themes1.py          # 테마 허브 + 7개 테마
  themes2.py          # 테마 7개
  info.py             # 코스·예약·가이드·후기·고객센터·약관
  about.py            # 운영자 소개
assets/               # CSS, 모바일 내비 JS, 파비콘·OG 이미지
```

## 빌드

```bash
python3 build.py
```

빌드 시 페이지별 본문 글자수 리포트가 출력됩니다.

## SEO 운영 원칙 (빌드에 강제됨)

- 본문 **2,000자 미만 페이지는 자동 `noindex`** 처리되고 sitemap에서 제외
- 숫자 행정동은 대표 동으로 통합 (일도1·2동→일도동, 이도1·2동→이도동, 삼도1·2동→삼도동, 용담1·2동→용담동) — 숫자 동 개별 페이지 없음
- 지하철역 메뉴 없음 — 공항·항만·버스터미널·관광 생활권 기준 교통거점 페이지로 운영
- **지역+교통거점+테마 조합 페이지 없음** (도어웨이 방지) — 테마는 독립 페이지로만 운영
- 상단/하위 메뉴와 푸터에 키워드·지역명 대량 나열 없음
- 모든 페이지 본문은 페이지별 고유 작성 (지역명만 바꾼 복붙 없음)
- Canonical 자기 자신, Breadcrumb 전체 페이지 적용

## 검색엔진 색인 (네이버·구글)

배포 도메인: `https://jeju-massage.pages.dev` (`content/site.py`의 `BASE_URL`)

빌드 시 자동 생성되는 색인 관련 파일:

- `sitemap.xml` — 인덱스 허용 페이지 전체, `lastmod` 포함
- `rss.xml` — RSS 2.0 피드 (네이버 서치어드바이저 RSS 제출용, 구글도 sitemap으로 인식)
- `robots.txt` — 전체 허용 + Googlebot·Yeti(네이버)·Bingbot 명시 허용, sitemap·rss 선언
- `{INDEXNOW_KEY}.txt` — IndexNow 소유 확인 키 파일

### 가장 빠른 색인 절차

1. **네이버 서치어드바이저** (https://searchadvisor.naver.com)
   - 사이트 등록 → 소유확인(메인페이지 meta 태그 이미 삽입됨)
   - 요청 > 사이트맵 제출: `sitemap.xml`, RSS 제출: `rss.xml`
   - 요청 > 웹 페이지 수집: 메인 URL 즉시 수집 요청
2. **구글 서치 콘솔** (https://search.google.com/search-console)
   - 속성 추가 → `sitemap.xml` 제출 → URL 검사에서 메인 URL "색인 생성 요청"
   - ※ 구글의 sitemap ping 엔드포인트는 2023년 폐지되어 Search Console 제출이 정석
3. **IndexNow 즉시 통보** (빙·네이버 등 참여 엔진, 새 글 올릴 때마다):
   ```bash
   python3 scripts/indexnow_submit.py                     # sitemap 전체 제출
   python3 scripts/indexnow_submit.py https://.../new/    # 특정 URL만
   ```
4. **구글 Indexing API** (보조 수단, 서비스 계정 필요):
   ```bash
   GOOGLE_SERVICE_ACCOUNT_JSON=key.json python3 scripts/google_indexing_api.py
   ```
   설정 방법은 `scripts/google_indexing_api.py` 상단 주석 참고.

## 도메인 변경 시

1. `content/site.py`의 `BASE_URL` 변경
2. `python3 build.py` 재실행 (canonical·sitemap·rss·robots.txt에 반영됨)
3. 위 색인 절차 다시 진행
