#!/usr/bin/env python3
"""제주 예쁨 마사지 — 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 지역+교통거점+테마 조합 경로는 생성 자체가 불가능한 구조
"""
import html
import json
import os
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.site import (BASE_URL, BRAND, INDEXNOW_KEY, NAV,
                          NAVER_VERIFICATION_CODES, PHONE, PHONE_DISPLAY,
                          RATING_VALUE, REVIEW_COUNT, REVIEWS)

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = BASE_URL.rstrip("/")
MIN_INDEX_CHARS = 2000
BUILD_DT = datetime.now(timezone.utc)


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 요금 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


# ──────────────────────────────────────────────────────────────
# 구조화 데이터(JSON-LD) — 전 페이지 일괄 적용
#   · HealthAndBeautyBusiness + AggregateRating(평점) + Review(후기)
#   · BreadcrumbList (브레드크럼이 있는 페이지)
#   · FAQPage (본문 faq-item 을 자동 추출)
#   · WebSite (메인)
# ──────────────────────────────────────────────────────────────
AREA_RE = re.compile(r"^jeju/(jeju-si|seogwipo-si)/[^/]+/$")
PLACE_RE = re.compile(r"^jeju/places/[^/]+/$")
THEME_RE = re.compile(r"^themes/[^/]+/$")
INFO_LEAF = {"massage/", "courses/", "reservation/", "guide/", "reviews/",
             "support/", "about/"}
_BUSINESS_ID = SITE + "/#business"


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


def short_name(page: dict) -> str:
    bc = page.get("breadcrumb") or []
    return bc[-1][0] if bc else page["h1"]


def area_name(page: dict) -> str:
    bc = page.get("breadcrumb") or []
    if AREA_RE.match(page["path"]) and len(bc) >= 2:
        return f"제주특별자치도 {bc[1][0]} {bc[-1][0]}"
    return "제주특별자치도"


def business_node(area: str, with_reviews: bool) -> dict:
    node = {
        "@type": "HealthAndBeautyBusiness",
        "@id": _BUSINESS_ID,
        "name": BRAND,
        "telephone": PHONE,
        "url": SITE + "/",
        "image": SITE + "/assets/og-image.png",
        "description": "제주 전지역 방문 출장마사지·홈타이 예약 안내",
        "areaServed": {"@type": "AdministrativeArea", "name": area},
        "openingHours": "Mo-Su 00:00-24:00",
        "priceRange": "₩90,000 - ₩180,000",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": str(RATING_VALUE),
            "reviewCount": str(REVIEW_COUNT),
            "bestRating": "5",
            "worstRating": "1",
        },
    }
    if with_reviews:
        node["review"] = [
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": f"{init}님"},
                "reviewRating": {"@type": "Rating", "ratingValue": str(score),
                                 "bestRating": "5", "worstRating": "1"},
                "reviewBody": body,
                "itemReviewed": {"@id": _BUSINESS_ID},
            }
            for init, score, loc, body in REVIEWS
        ]
    return node


def faq_node(body: str):
    items = re.findall(
        r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', body, flags=re.S
    )
    if not items:
        return None
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": strip_tags(q),
             "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in items
        ],
    }


def breadcrumb_node(crumbs, canonical):
    if not crumbs:
        return None
    items = [{"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"}]
    for i, (label, href) in enumerate(crumbs, start=2):
        items.append({
            "@type": "ListItem", "position": i, "name": label,
            "item": (SITE + href) if href else canonical,
        })
    return {"@type": "BreadcrumbList", "itemListElement": items}


def build_jsonld(page: dict, canonical: str) -> str:
    path = page["path"]
    nodes = [business_node(area_name(page), with_reviews=path in ("", "reviews/"))]
    bc = breadcrumb_node(page.get("breadcrumb") or [], canonical)
    if bc:
        nodes.append(bc)
    faq = faq_node(page["body"])
    if faq:
        nodes.append(faq)
    if path == "":
        nodes.append({"@type": "WebSite", "@id": SITE + "/#website",
                      "name": BRAND, "url": SITE + "/", "inLanguage": "ko"})
    graph = {"@context": "https://schema.org", "@graph": nodes}
    return ('<script type="application/ld+json">\n'
            + json.dumps(graph, ensure_ascii=False, indent=2)
            + "\n</script>\n")


# ──────────────────────────────────────────────────────────────
# 내부링크 강화 — 롱테일 주제의 관련 안내 블록을 leaf 페이지마다 자동 생성
# ──────────────────────────────────────────────────────────────
_THEME_PICKS = [
    ("스웨디시", "/themes/swedish/"), ("아로마테라피", "/themes/aroma/"),
    ("타이마사지", "/themes/thai/"), ("홈케어", "/themes/homecare/"),
    ("발마사지", "/themes/foot/"), ("커플 관리", "/themes/couple/"),
    ("호텔식마사지", "/themes/hotel-style/"), ("스포츠·경락", "/themes/sports/"),
    ("로미로미", "/themes/lomilomi/"), ("24시간", "/themes/24hours/"),
]
_INFO_PICKS = [
    ("코스안내", "/courses/"), ("예약안내", "/reservation/"),
    ("이용가이드", "/guide/"), ("이용 후기", "/reviews/"),
]

# 지역·거점·테마 형제 페이지 묶음(부모 경로 → [(이름, href)])
_SIBLINGS = {}
for _p in PAGES:
    _path = _p["path"]
    if AREA_RE.match(_path) or PLACE_RE.match(_path) or THEME_RE.match(_path):
        _parent = _path.rsplit("/", 2)[0] + "/"
        _SIBLINGS.setdefault(_parent, []).append((short_name(_p), "/" + _path))


def _rotate(items, seed):
    if not items:
        return items
    off = sum(ord(c) for c in seed) % len(items)
    return items[off:] + items[:off]


def _grid(links):
    cells = "".join(
        f'<li><a href="{h}">{html.escape(t)}</a></li>' for t, h in links
    )
    return f'<ul class="card-grid">{cells}</ul>'


def render_related(page: dict) -> str:
    path = page["path"]
    self_href = "/" + path
    name = short_name(page)
    intro = ""
    groups = []  # (소제목, [(텍스트, href)])

    if AREA_RE.match(path):
        parent = path.rsplit("/", 2)[0] + "/"
        sibs = [(t, h) for t, h in _SIBLINGS.get(parent, []) if h != self_href]
        sibs = _rotate(sibs, path)[:6]
        intro = (f"{name} 출장마사지·홈타이 예약 전, 가까운 지역과 인기 관리 테마, "
                 f"예약·이용 안내를 함께 확인해 보세요.")
        groups = [
            (f"{name} 주변 지역 출장마사지", [(f"{t} 출장마사지", h) for t, h in sibs]),
            (f"{name}에서 많이 찾는 관리 테마", _rotate(_THEME_PICKS, path)[:6]),
            ("예약·이용 안내", _INFO_PICKS),
        ]
    elif PLACE_RE.match(path):
        parent = "jeju/places/"
        # 일부 거점 라벨은 이미 '인근'을 포함하므로 중복을 막기 위해 정규화한다.
        def _nearby(label):
            return re.sub(r"\s*인근$", "", label).strip() + " 인근"
        base = re.sub(r"\s*인근$", "", name).strip()
        sibs = [(t, h) for t, h in _SIBLINGS.get(parent, []) if h != self_href]
        sibs = _rotate(sibs, path)[:6]
        intro = (f"{base} 인근 출장마사지·홈타이 방문 전, 가까운 교통거점과 관리 테마, "
                 f"지역별 안내를 함께 살펴보세요.")
        groups = [
            (f"{base} 주변 교통거점 안내", [(_nearby(t), h) for t, h in sibs]),
            ("거점 인근 인기 관리 테마", _rotate(_THEME_PICKS, path)[:6]),
            ("지역·예약 안내", [
                ("제주시 출장마사지", "/jeju/jeju-si/"),
                ("서귀포시 출장마사지", "/jeju/seogwipo-si/"),
                ("예약안내", "/reservation/"), ("이용 후기", "/reviews/")]),
        ]
    elif THEME_RE.match(path):
        parent = "themes/"
        sibs = [(t, h) for t, h in _SIBLINGS.get(parent, []) if h != self_href]
        sibs = _rotate(sibs, path)[:8]
        intro = (f"{name} 외에 제주 출장마사지·홈타이에서 고를 수 있는 다른 관리 테마와 "
                 f"지역·거점별 안내, 코스·예약 정보를 함께 확인해 보세요.")
        groups = [
            ("다른 관리 테마 둘러보기", sibs),
            ("지역·거점별 출장마사지 안내", [
                ("제주시 출장마사지", "/jeju/jeju-si/"),
                ("서귀포시 출장마사지", "/jeju/seogwipo-si/"),
                ("교통거점별 안내", "/jeju/places/")]),
            ("코스·예약 안내", [
                ("코스안내", "/courses/"), ("예약안내", "/reservation/"),
                ("이용가이드", "/guide/")]),
        ]
    elif path in INFO_LEAF:
        intro = ("제주 출장마사지·홈타이 예약 전, 지역별·테마별 안내와 코스·예약 정보를 "
                 "함께 확인하시면 더 빠르게 결정하실 수 있습니다.")
        groups = [
            ("제주 지역·테마별 출장마사지 안내", [
                ("제주시 출장마사지", "/jeju/jeju-si/"),
                ("서귀포시 출장마사지", "/jeju/seogwipo-si/"),
                ("교통거점별 안내", "/jeju/places/"),
                ("테마별 안내", "/themes/")]),
            ("예약 전 함께 보기", [
                ("제주 출장마사지 안내", "/massage/"), ("코스안내", "/courses/"),
                ("예약안내", "/reservation/"), ("이용가이드", "/guide/"),
                ("이용 후기", "/reviews/")]),
        ]
    else:
        return ""  # 메인·허브·noindex 페이지는 이미 충분한 내부링크 보유

    parts = ['<section class="related-links"><h2>함께 보면 좋은 안내</h2>']
    if intro:
        parts.append(f"<p>{html.escape(intro)}</p>")
    for sub, links in groups:
        links = [(t, h) for t, h in links if h != self_href]
        if not links:
            continue
        parts.append(f"<h3>{html.escape(sub)}</h3>")
        parts.append(_grid(links))
    parts.append("</section>")
    return "".join(parts)


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path

    # 히어로가 있는 페이지(메인)는 H1을 히어로 안에서 출력한다.
    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    # 내부링크 강화 블록(롱테일 관련 안내)을 본문 끝에 덧붙인다.
    body = body + render_related(page)

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    # 네이버 소유확인(메인 전용) + 구조화 데이터(전 페이지)
    naver = ""
    if path == "":
        naver = "".join(
            f'<meta name="naver-site-verification" content="{c}">\n'
            for c in NAVER_VERIFICATION_CODES
        )
    jsonld = build_jsonld(page, canonical)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0a1120">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{naver}{extra_head}{jsonld}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">J</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> 제주 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">제주 전지역 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 제주특별자치도 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="서비스 안내">
      <p class="footer-title">서비스</p>
      <ul>
        <li><a href="/massage/">제주 출장마사지</a></li>
        <li><a href="/jeju/">지역별 안내</a></li>
        <li><a href="/jeju/places/">교통거점별 안내</a></li>
        <li><a href="/themes/">테마별 안내</a></li>
        <li><a href="/courses/">코스안내</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/reservation/">예약안내</a></li>
        <li><a href="/guide/">이용가이드</a></li>
        <li><a href="/reviews/">이용 후기</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/support/#faq">자주 묻는 질문</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/about/">운영자 소개</a></li>
        <li><a href="/support/privacy/">개인정보처리방침</a></li>
        <li><a href="/support/terms/">이용약관</a></li>
        <li><a href="/guide/#hygiene">위생·안전 기준</a></li>
        <li><a href="/guide/#prohibited">금지행위 안내</a></li>
        <li><a href="/support/#biz">제휴·기업 문의</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <a class="footer-made" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow">웹사이트 제작문의 ↗</a>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


def build() -> None:
    report = []
    sitemap_urls = []

    indexable_pages = []
    for page in PAGES:
        path = page["path"]  # "" 또는 "jeju/jeju-si/yeon-dong/" 형태
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            sitemap_urls.append(path)
            indexable_pages.append(page)
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    base = BASE_URL.rstrip("/")
    lastmod = BUILD_DT.strftime("%Y-%m-%d")

    # sitemap.xml — lastmod·priority·changefreq 포함 (네이버·구글 색인 우선순위 명시)
    def sitemap_meta(p):
        if p == "":
            return "1.0", "daily"
        if p in ("jeju/", "jeju/jeju-si/", "jeju/seogwipo-si/", "jeju/places/",
                 "themes/", "massage/"):
            return "0.9", "weekly"
        if AREA_RE.match(p) or PLACE_RE.match(p) or THEME_RE.match(p):
            return "0.8", "weekly"
        return "0.7", "monthly"

    url_entries = []
    for p in sitemap_urls:
        prio, freq = sitemap_meta(p)
        url_entries.append(
            f"  <url><loc>{base}/{p}</loc><lastmod>{lastmod}</lastmod>"
            f"<changefreq>{freq}</changefreq><priority>{prio}</priority></url>"
        )
    urls = "\n".join(url_entries)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n"
        )

    # rss.xml — 네이버 서치어드바이저 RSS 제출용 (구글도 sitemap으로 인식)
    pub_date = BUILD_DT.strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = []
    for page in indexable_pages:
        loc = base + "/" + page["path"]
        items.append(
            "  <item>\n"
            f"    <title>{html.escape(page['title'])}</title>\n"
            f"    <link>{loc}</link>\n"
            f"    <guid isPermaLink=\"true\">{loc}</guid>\n"
            f"    <description>{html.escape(page['desc'])}</description>\n"
            f"    <pubDate>{pub_date}</pubDate>\n"
            "  </item>"
        )
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0">\n'
            "<channel>\n"
            f"  <title>{html.escape(BRAND)}</title>\n"
            f"  <link>{base}/</link>\n"
            "  <description>제주 전지역 방문 출장마사지·홈타이 예약 안내</description>\n"
            "  <language>ko</language>\n"
            f"  <lastBuildDate>{pub_date}</lastBuildDate>\n"
            + "\n".join(items)
            + "\n</channel>\n</rss>\n"
        )

    # robots.txt — 전체 허용 + 네이버(Yeti)·구글(Googlebot)·빙 명시 허용
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\n"
            "Allow: /\n\n"
            "User-agent: Googlebot\n"
            "Allow: /\n\n"
            "User-agent: Yeti\n"
            "Allow: /\n\n"
            "User-agent: Bingbot\n"
            "Allow: /\n\n"
            f"Sitemap: {base}/sitemap.xml\n"
            f"Sitemap: {base}/rss.xml\n"
        )

    # IndexNow 키 파일 — 빙·네이버 즉시 색인 통보용 소유 확인 파일
    with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

    # .nojekyll (GitHub Pages)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(sitemap_urls)} in sitemap.")


if __name__ == "__main__":
    build()
