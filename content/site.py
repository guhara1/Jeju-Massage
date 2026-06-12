# 사이트 공통 설정
BASE_URL = "https://jeju-massage.pages.dev"

BRAND = "제주 예쁨 마사지"
PHONE = "0508-202-4723"
PHONE_DISPLAY = "0508-202-4723"

# IndexNow API 키 — 빌드 시 루트에 {키}.txt 소유 확인 파일이 생성된다.
# scripts/indexnow_submit.py 가 이 키로 빙·네이버에 색인 요청을 보낸다.
INDEXNOW_KEY = "035cd3202fb1448e926f1a30302e1e66"

# 상단 메뉴 — 하위 메뉴에는 키워드를 반복하지 않고 지역명·거점명만 짧게 표시한다.
# 지역+교통거점+테마 조합 메뉴는 만들지 않는다.
NAV = [
    ("홈", "/", []),
    ("제주 출장마사지", "/massage/", [
        ("출장마사지 안내", "/massage/#service"),
        ("홈타이 안내", "/massage/#hometai"),
        ("전지역 방문 안내", "/massage/#coverage"),
        ("교통거점 인근 안내", "/massage/#places"),
        ("예약 가능 시간", "/massage/#hours"),
        ("코스 선택 안내", "/massage/#course"),
        ("이용 전 확인사항", "/massage/#check"),
        ("위생·안전 안내", "/massage/#safety"),
        ("자주 묻는 질문", "/massage/#faq"),
    ]),
    ("지역별 안내", "/jeju/", [
        ("제주 전체", "/jeju/"),
        ("제주시", "/jeju/jeju-si/"),
        ("서귀포시", "/jeju/seogwipo-si/"),
    ]),
    ("교통거점별 안내", "/jeju/places/", [
        ("교통거점 전체", "/jeju/places/"),
        ("제주공항", "/jeju/places/jeju-airport/"),
        ("제주항", "/jeju/places/jeju-port/"),
        ("제주시외버스터미널", "/jeju/places/jeju-bus-terminal/"),
        ("서귀포버스터미널", "/jeju/places/seogwipo-bus-terminal/"),
        ("성산항", "/jeju/places/seongsan-port/"),
        ("모슬포항", "/jeju/places/moseulpo-port/"),
        ("한림항", "/jeju/places/hanlim-port/"),
        ("중문관광단지", "/jeju/places/jungmun-tourist-complex/"),
        ("제주시청 인근", "/jeju/places/jeju-city-hall/"),
        ("서귀포시청 인근", "/jeju/places/seogwipo-city-hall/"),
        ("제주대학교 인근", "/jeju/places/jeju-university/"),
        ("노형오거리 인근", "/jeju/places/nohyeong-five-way/"),
        ("누웨마루거리 인근", "/jeju/places/nuwemaru-street/"),
        ("애월해안도로 인근", "/jeju/places/aewol-coastal-road/"),
        ("함덕해수욕장 인근", "/jeju/places/hamdeok-beach/"),
        ("협재해수욕장 인근", "/jeju/places/hyeopjae-beach/"),
        ("성산일출봉 인근", "/jeju/places/seongsan-ilchulbong/"),
        ("표선해수욕장 인근", "/jeju/places/pyoseon-beach/"),
    ]),
    ("테마별 안내", "/themes/", [
        ("전체 테마", "/themes/"),
        ("스웨디시", "/themes/swedish/"),
        ("로미로미", "/themes/lomilomi/"),
        ("타이마사지", "/themes/thai/"),
        ("중국마사지", "/themes/chinese/"),
        ("아로마테라피", "/themes/aroma/"),
        ("홈케어", "/themes/homecare/"),
        ("호텔식마사지", "/themes/hotel-style/"),
        ("발마사지", "/themes/foot/"),
        ("스포츠·경락", "/themes/sports/"),
        ("스킨케어", "/themes/skincare/"),
        ("왁싱", "/themes/waxing/"),
        ("커플 관리", "/themes/couple/"),
        ("24시간", "/themes/24hours/"),
        ("수면 가능", "/themes/overnight/"),
    ]),
    ("코스안내", "/courses/", [
        ("전체 코스", "/courses/"),
        ("피로 회복 관리", "/courses/#recovery"),
        ("아로마 관리", "/courses/#aroma"),
        ("스포츠 관리", "/courses/#sports"),
        ("홈타이 코스", "/courses/#hometai"),
        ("커플·가족 방문 관리", "/courses/#couple"),
        ("호텔·숙소 방문 관리", "/courses/#hotel"),
        ("기업·단체 방문 관리", "/courses/#group"),
        ("가격 안내", "/courses/#price"),
        ("코스 선택 가이드", "/courses/#guide"),
    ]),
    ("예약안내", "/reservation/", [
        ("예약 방법", "/reservation/#how"),
        ("예약 가능 시간", "/reservation/#hours"),
        ("방문 가능 장소", "/reservation/#place"),
        ("호텔·숙소 방문 안내", "/reservation/#hotel"),
        ("결제 안내", "/reservation/#payment"),
        ("변경·취소 안내", "/reservation/#change"),
        ("예약 전 체크사항", "/reservation/#check"),
    ]),
    ("이용가이드", "/guide/", [
        ("처음 이용하시는 분", "/guide/#first"),
        ("방문 전 준비사항", "/guide/#prepare"),
        ("호텔 이용 시 확인사항", "/guide/#hotel"),
        ("펜션·리조트 이용 시", "/guide/#pension"),
        ("위생 및 안전 기준", "/guide/#hygiene"),
        ("관리 후 주의사항", "/guide/#after"),
        ("금지행위 안내", "/guide/#prohibited"),
        ("이용 FAQ", "/guide/#faq"),
    ]),
    ("후기", "/reviews/", [
        ("전체 후기", "/reviews/"),
        ("지역별 후기", "/reviews/#area"),
        ("숙소 방문 후기", "/reviews/#stay"),
        ("교통거점 인근 후기", "/reviews/#place"),
        ("후기 작성 안내", "/reviews/#write"),
    ]),
    ("고객센터", "/support/", [
        ("공지사항", "/support/#notice"),
        ("자주 묻는 질문", "/support/#faq"),
        ("1:1 문의", "/support/#contact"),
        ("제휴·기업 문의", "/support/#biz"),
        ("개인정보처리방침", "/support/privacy/"),
        ("이용약관", "/support/terms/"),
    ]),
]
