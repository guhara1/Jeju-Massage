# 사이트 공통 설정
BASE_URL = "https://jeju-massage.netlify.app"

BRAND = "제주 예쁨 마사지"
PHONE = "0508-202-4723"
PHONE_DISPLAY = "0508-202-4723"

# 네이버 서치어드바이저 사이트 소유확인 코드 — 메인 페이지 <head>에만 출력한다.
# 여러 계정으로 확인할 수 있도록 코드를 누적 보관한다(여러 개여도 충돌하지 않는다).
NAVER_VERIFICATION_CODES = [
    "7fb4e141e28657966f57b39d9643b4fa10172ea9",
    "585229888908c4675978d0f3f5a7bf2130d55ef4",
]

# IndexNow API 키 — 빌드 시 루트에 {키}.txt 소유 확인 파일이 생성된다.
# scripts/indexnow_submit.py 가 이 키로 빙·네이버에 색인 요청을 보낸다.
INDEXNOW_KEY = "035cd3202fb1448e926f1a30302e1e66"

# 구조화 데이터(JSON-LD)용 후기·평점 데이터.
# /reviews/ 페이지에 실제로 노출되는 후기를 그대로 사용해 self-serving 우려를 줄인다.
# AggregateRating 의 reviewCount 는 아래 REVIEWS 개수와 일치시킨다.
REVIEWS = [
    ("K", 5, "제주시 노형동", "전화하고 한 시간 반쯤 뒤에 오셨고, 어깨 위주로 풀어달라는 요청을 시작 전에 한 번 더 확인해 주셔서 좋았어요."),
    ("H", 5, "제주시 이도동", "오피스텔로 퇴근 후 불렀는데 도착 전에 연락을 주셔서 기다림이 없었습니다. 90분이 끝나고 나니 적당했네요."),
    ("J", 5, "서귀포시", "부모님 댁에 선물로 예약했습니다. 대신 예약하는 절차가 번거롭지 않았고, 어머니가 다음에 또 부르자고 하셨어요."),
    ("P", 4, "서귀포시 성산", "멀어서 안 될 줄 알았는데 시간을 넉넉히 잡으니 가능했습니다. 도착 시각을 중간에 한 번 더 알려준 점이 믿음직했어요."),
    ("Y", 5, "제주시 아라동", "야근 끝나고 밤 11시 넘어 불렀는데 평소와 똑같이 차분하게 진행해 주셨고, 끝나고 바로 잘 수 있어서 다음 날이 달랐어요."),
    ("L", 5, "제주시 애월", "풀빌라에서 커플로 동시에 받았습니다. 두 분이 같이 오셔서 세팅도 빨랐고, 진입로가 좁은데도 정확히 찾아오셨습니다."),
    ("S", 5, "서귀포시 중문", "호텔 객실에서 받았는데 로비에서 전화 주셔서 문제없이 진행됐고, 침대 위에 시트를 깔아주셔서 침구 걱정도 없었습니다."),
    ("C", 4, "제주시 함덕", "독채 펜션에서 밤 10시쯤 받았습니다. 조용히 진행해 주셔서 아이가 깨지 않았고, 다음 날 올레길 걷는 데 다리가 훨씬 편했습니다."),
    ("A", 5, "서귀포시 표선", "리조트에 가족이 묵으며 부모님 두 분이 차례로 받으셨는데, 두 분 압을 각각 다르게 맞춰주신 게 좋았습니다."),
    ("M", 5, "제주공항 인근", "저녁 비행기로 도착해 공항 근처 호텔에 짐 풀자마자 받았더니 비행 피로가 풀려 다음 날 일정이 살았습니다."),
    ("B", 4, "서귀포시 중문", "라운딩 마치고 숙소로 불렀는데, 골프 쳤다고 하니 허리와 전완까지 챙겨주는 게 그냥 미는 관리와 달랐어요."),
    ("D", 5, "제주공항 인근", "마지막 날 오전 비행기라 전날 밤 공항 근처 숙소에서 받았더니, 여행 내내 운전한 피로가 풀려 돌아가는 길이 가벼웠습니다."),
]

# 위 후기 평점의 평균·개수 — AggregateRating 에 사용한다.
RATING_VALUE = round(sum(r[1] for r in REVIEWS) / len(REVIEWS), 1)  # 4.8
REVIEW_COUNT = len(REVIEWS)

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
