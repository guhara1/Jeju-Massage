# 메인 페이지 — 허브 역할. 키워드를 몰아넣지 않고 상세 페이지로 연결한다.
from .site import BASE_URL, BRAND, PHONE, PHONE_DISPLAY
from .pricing import PRICING

_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HealthAndBeautyBusiness",
  "name": "{BRAND}",
  "telephone": "{PHONE}",
  "url": "{BASE_URL}/",
  "image": "{BASE_URL}/assets/og-image.png",
  "description": "제주 전지역 방문 출장마사지·홈타이 예약 안내",
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "제주특별자치도"
  }},
  "openingHours": "Mo-Su 00:00-24:00",
  "priceRange": "₩90,000 - ₩180,000"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "제주 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "제주시와 서귀포시 39개 읍면동을 기준으로 안내하며, 예약 시간과 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 추자면·우도면 같은 도서 지역은 배편 사정이 있어 사전 협의가 필요합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "제주공항이나 중문관광단지 근처 숙소도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "공항, 항만, 터미널, 주요 관광지 인근은 교통거점별 안내 페이지에서 주변 숙소 환경과 함께 설명합니다. 정확한 가능 여부는 예약 시 숙소 위치를 기준으로 확인합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "일도1동과 일도2동은 왜 따로 없나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "일도1·2동, 이도1·2동처럼 숫자로 나뉜 행정동은 대표 동 페이지에서 통합 안내하여 비슷한 내용이 반복되는 중복 페이지를 만들지 않습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "당일 예약도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "가능할 수 있지만 저녁 시간대와 주말, 관광 성수기에는 문의가 몰릴 수 있어 사전 예약을 권장합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "테마별 관리는 어디에서 확인하나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "스웨디시, 로미로미, 호텔식마사지 등 테마별 안내 페이지에서 관리별 특징과 추천 대상을 확인할 수 있습니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 제주 전지역</p>
    <h1>제주 출장마사지·홈타이<br>예약 안내</h1>
    <p class="hero-lead">호텔·펜션·자택 어디든, 계신 곳으로 찾아가는 프리미엄 방문 관리.<br>여행의 피로도 일상의 피로도 전화 한 통이면 예약이 끝납니다.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/courses/">코스 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>39개</strong><span>지역 안내</span></li>
      <li><strong>18개</strong><span>교통거점</span></li>
      <li><strong>14개</strong><span>관리 테마</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="service">
<h2>제주 출장마사지·홈타이 서비스 안내</h2>
<p>제주에서 방문 마사지와 홈타이 예약을 찾는 분들을 위해 가능 지역, 예약 절차, 코스 선택 기준을 한곳에 정리했습니다. 이 페이지는 제주 전체 구조를 보여주는 허브이며, 자세한 내용은 지역별·교통거점별·테마별 안내 페이지에서 이어집니다. {BRAND}는 예약 확인부터 방문 관리까지 정해진 절차에 따라 진행해, 처음 이용하시는 분도 어렵지 않게 예약하실 수 있습니다.</p>
</section>

<section id="coverage">
<h2>제주 전지역 방문 가능 안내</h2>
<p>방문 범위는 제주특별자치도 전지역입니다. 지역 안내는 제주시 22개, 서귀포시 17개 읍면동 기준으로 구성했고, 일도1·2동을 일도동으로 묶는 것처럼 숫자로 나뉜 행정동은 대표 동 페이지에서 통합해 안내합니다. 같은 생활권을 잘게 쪼개기보다 동 단위로 묶어 설명하는 편이 정확하기 때문입니다. 추자면·우도면 같은 도서 지역은 배편 일정에 따라 사전 협의 후 진행됩니다.</p>
</section>

<section id="jeju-si">
<h2>제주시 지역 안내</h2>
<p>공항과 원도심, 신제주 상권, 읍면 지역까지 거주하시거나 머무시는 곳을 선택해 주세요.</p>
<ul class="card-grid">
<li><a href="/jeju/jeju-si/hanlim-eup/">한림읍</a></li>
<li><a href="/jeju/jeju-si/aewol-eup/">애월읍</a></li>
<li><a href="/jeju/jeju-si/gujwa-eup/">구좌읍</a></li>
<li><a href="/jeju/jeju-si/jocheon-eup/">조천읍</a></li>
<li><a href="/jeju/jeju-si/hangyeong-myeon/">한경면</a></li>
<li><a href="/jeju/jeju-si/chuja-myeon/">추자면</a></li>
<li><a href="/jeju/jeju-si/udo-myeon/">우도면</a></li>
<li><a href="/jeju/jeju-si/ildo-dong/">일도동</a></li>
<li><a href="/jeju/jeju-si/ido-dong/">이도동</a></li>
<li><a href="/jeju/jeju-si/samdo-dong/">삼도동</a></li>
<li><a href="/jeju/jeju-si/yongdam-dong/">용담동</a></li>
<li><a href="/jeju/jeju-si/geonip-dong/">건입동</a></li>
<li><a href="/jeju/jeju-si/hwabuk-dong/">화북동</a></li>
<li><a href="/jeju/jeju-si/samyang-dong/">삼양동</a></li>
<li><a href="/jeju/jeju-si/bonggae-dong/">봉개동</a></li>
<li><a href="/jeju/jeju-si/ara-dong/">아라동</a></li>
<li><a href="/jeju/jeju-si/ora-dong/">오라동</a></li>
<li><a href="/jeju/jeju-si/yeon-dong/">연동</a></li>
<li><a href="/jeju/jeju-si/nohyeong-dong/">노형동</a></li>
<li><a href="/jeju/jeju-si/oedo-dong/">외도동</a></li>
<li><a href="/jeju/jeju-si/iho-dong/">이호동</a></li>
<li><a href="/jeju/jeju-si/dodu-dong/">도두동</a></li>
</ul>
</section>

<section id="seogwipo">
<h2>서귀포시 지역 안내</h2>
<p>중문관광단지와 올레시장 일대, 동서부 읍면 지역 중 숙소가 있는 동을 골라 확인해 보세요.</p>
<ul class="card-grid">
<li><a href="/jeju/seogwipo-si/daejeong-eup/">대정읍</a></li>
<li><a href="/jeju/seogwipo-si/namwon-eup/">남원읍</a></li>
<li><a href="/jeju/seogwipo-si/seongsan-eup/">성산읍</a></li>
<li><a href="/jeju/seogwipo-si/andeok-myeon/">안덕면</a></li>
<li><a href="/jeju/seogwipo-si/pyoseon-myeon/">표선면</a></li>
<li><a href="/jeju/seogwipo-si/songsan-dong/">송산동</a></li>
<li><a href="/jeju/seogwipo-si/jeongbang-dong/">정방동</a></li>
<li><a href="/jeju/seogwipo-si/jungang-dong/">중앙동</a></li>
<li><a href="/jeju/seogwipo-si/cheonji-dong/">천지동</a></li>
<li><a href="/jeju/seogwipo-si/hyodon-dong/">효돈동</a></li>
<li><a href="/jeju/seogwipo-si/yeongcheon-dong/">영천동</a></li>
<li><a href="/jeju/seogwipo-si/donghong-dong/">동홍동</a></li>
<li><a href="/jeju/seogwipo-si/seohong-dong/">서홍동</a></li>
<li><a href="/jeju/seogwipo-si/daeryun-dong/">대륜동</a></li>
<li><a href="/jeju/seogwipo-si/daecheon-dong/">대천동</a></li>
<li><a href="/jeju/seogwipo-si/jungmun-dong/">중문동</a></li>
<li><a href="/jeju/seogwipo-si/yerae-dong/">예래동</a></li>
</ul>
</section>

<section id="places">
<h2>교통거점별 안내</h2>
<p>지하철이 없는 제주에서는 공항, 항만, 터미널, 주요 관광지가 위치 기준이 됩니다. 숙소에서 가까운 거점을 선택해 주세요.</p>
<ul class="card-grid">
<li><a href="/jeju/places/jeju-airport/">제주공항</a></li>
<li><a href="/jeju/places/jeju-port/">제주항</a></li>
<li><a href="/jeju/places/jeju-bus-terminal/">제주시외버스터미널</a></li>
<li><a href="/jeju/places/seogwipo-bus-terminal/">서귀포버스터미널</a></li>
<li><a href="/jeju/places/seongsan-port/">성산항</a></li>
<li><a href="/jeju/places/moseulpo-port/">모슬포항</a></li>
<li><a href="/jeju/places/hanlim-port/">한림항</a></li>
<li><a href="/jeju/places/jungmun-tourist-complex/">중문관광단지</a></li>
<li><a href="/jeju/places/jeju-city-hall/">제주시청 인근</a></li>
<li><a href="/jeju/places/seogwipo-city-hall/">서귀포시청 인근</a></li>
<li><a href="/jeju/places/jeju-university/">제주대학교 인근</a></li>
<li><a href="/jeju/places/nohyeong-five-way/">노형오거리 인근</a></li>
<li><a href="/jeju/places/nuwemaru-street/">누웨마루거리 인근</a></li>
<li><a href="/jeju/places/aewol-coastal-road/">애월해안도로 인근</a></li>
<li><a href="/jeju/places/hamdeok-beach/">함덕해수욕장 인근</a></li>
<li><a href="/jeju/places/hyeopjae-beach/">협재해수욕장 인근</a></li>
<li><a href="/jeju/places/seongsan-ilchulbong/">성산일출봉 인근</a></li>
<li><a href="/jeju/places/pyoseon-beach/">표선해수욕장 인근</a></li>
</ul>
</section>

<section id="themes">
<h2>테마별 관리 안내</h2>
<p>테마별 안내에서는 관리 유형별 특징과 추천 대상, 예약 전 확인사항을 설명합니다. 테마는 각각 독립 페이지로 운영하고, 지역·거점 페이지에서는 관련 테마로 연결만 합니다.</p>
<ul class="card-grid">
<li><a href="/themes/swedish/">스웨디시</a></li>
<li><a href="/themes/lomilomi/">로미로미</a></li>
<li><a href="/themes/thai/">타이마사지</a></li>
<li><a href="/themes/chinese/">중국마사지</a></li>
<li><a href="/themes/aroma/">아로마테라피</a></li>
<li><a href="/themes/homecare/">홈케어</a></li>
<li><a href="/themes/hotel-style/">호텔식마사지</a></li>
<li><a href="/themes/foot/">발마사지</a></li>
<li><a href="/themes/sports/">스포츠·경락</a></li>
<li><a href="/themes/skincare/">스킨케어</a></li>
<li><a href="/themes/waxing/">왁싱</a></li>
<li><a href="/themes/couple/">커플 관리</a></li>
<li><a href="/themes/24hours/">24시간</a></li>
<li><a href="/themes/overnight/">수면 가능</a></li>
</ul>
</section>

<section id="course">
<h2>코스 선택 안내</h2>
<p>코스는 이용 목적과 그날의 컨디션으로 정하시면 됩니다. 올레길 걷기나 한라산 산행 뒤 다리 회복이 필요한 분, 비행과 운전의 피로를 풀고 싶은 분, 커플이 함께 받고 싶은 분까지 상황별 선택 기준을 <a href="/courses/">코스안내</a>에서 자세히 다룹니다. 고민되시면 예약 전화에서 상태를 말씀해 주세요.</p>
</section>

<section id="how">
<h2>예약 진행 방식</h2>
<p>예약은 다섯 단계로 진행됩니다. 먼저 방문할 지역 또는 거점 인근 위치를 확인하고, 희망 시간을 확인한 뒤, 코스와 인원을 정하고, 방문 가능 여부를 안내받은 다음 예약을 확정합니다. 저녁 시간대와 주말, 관광 성수기에는 문의가 몰릴 수 있어 한두 시간 이상 여유를 두시기를 권장합니다. 자세한 절차는 <a href="/reservation/">예약안내</a>에 있습니다.</p>
</section>

<section id="check">
<h2>이용 전 확인사항</h2>
<p>원활한 방문을 위해 정확한 주소 또는 숙소명과 호실, 공동현관이나 로비 출입 방법, 주차 가능 여부, 조용한 공간 확보 여부를 미리 확인해 주세요. 준비사항 전체는 <a href="/guide/">이용가이드</a>에 정리되어 있습니다.</p>
</section>

<section id="hotel">
<h2>호텔·숙소 방문 안내</h2>
<p>제주는 호텔, 리조트, 펜션, 풀빌라 등 숙소로 출장마사지를 요청하시는 비중이 특히 높은 지역입니다. 숙소 방문 시에는 외부인 출입 절차가 숙소마다 달라 예약 단계에서 숙소명과 호실, 프런트 경유 여부를 함께 확인합니다. 세부 기준은 <a href="/reservation/#hotel">호텔·숙소 방문 안내</a>를 참고하세요.</p>
</section>

<section id="safety">
<h2>위생 및 안전 안내</h2>
<p>건전하고 안전한 방문 관리를 위해 위생 기준, 개인정보 보호, 금지행위 안내를 명확히 제공합니다. 불법적이거나 무리한 요청은 어떤 경우에도 진행하지 않으며, 예약 정보는 방문 목적 외에 사용하지 않습니다.</p>
</section>

<section id="faq">
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>제주 전지역 방문이 가능한가요?</h3>
<p>제주시와 서귀포시 39개 읍면동을 기준으로 안내하며, 예약 시간과 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 추자면·우도면 같은 도서 지역은 배편 사정이 있어 사전 협의가 필요합니다.</p>
</div>
<div class="faq-item">
<h3>제주공항이나 중문관광단지 근처 숙소도 가능한가요?</h3>
<p>공항, 항만, 터미널, 주요 관광지 인근은 교통거점별 안내 페이지에서 주변 숙소 환경과 함께 설명합니다. 정확한 가능 여부는 예약 시 숙소 위치를 기준으로 확인합니다.</p>
</div>
<div class="faq-item">
<h3>일도1동과 일도2동은 왜 따로 없나요?</h3>
<p>일도1·2동, 이도1·2동처럼 숫자로 나뉜 행정동은 대표 동 페이지에서 통합 안내하여 비슷한 내용이 반복되는 중복 페이지를 만들지 않습니다.</p>
</div>
<div class="faq-item">
<h3>당일 예약도 가능한가요?</h3>
<p>가능할 수 있지만 저녁 시간대와 주말, 관광 성수기에는 문의가 몰릴 수 있어 사전 예약을 권장합니다.</p>
</div>
<div class="faq-item">
<h3>테마별 관리는 어디에서 확인하나요?</h3>
<p>스웨디시, 로미로미, 호텔식마사지 등 테마별 안내 페이지에서 관리별 특징과 추천 대상을 확인할 수 있습니다.</p>
</div>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "제주 출장마사지·홈타이 | 제주 전지역 방문 마사지 예약 안내",
    "desc": "제주 출장마사지·홈타이 안내 페이지입니다. 제주시, 서귀포시, 제주공항, 중문관광단지, 애월, 성산, 노형동 등 제주 주요 지역과 교통거점 인근 예약 정보를 확인해보세요.",
    "h1": "제주 출장마사지·홈타이 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}

PAGES = [PAGE]
