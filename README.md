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

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경
2. `python3 build.py` 재실행 (canonical·sitemap·robots.txt에 반영됨)
3. Google Search Console에 `sitemap.xml` 제출
