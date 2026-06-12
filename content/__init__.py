# 전체 페이지 목록 집계
from . import (main, massage, region_hubs, areas_jeju_eup, areas_jeju_dong1,
               areas_jeju_dong2, areas_seogwipo1, areas_seogwipo2,
               places1, places2, themes1, themes2, info, about)

PAGES = (
    main.PAGES
    + massage.PAGES
    + region_hubs.PAGES
    + areas_jeju_eup.PAGES
    + areas_jeju_dong1.PAGES
    + areas_jeju_dong2.PAGES
    + areas_seogwipo1.PAGES
    + areas_seogwipo2.PAGES
    + places1.PAGES
    + places2.PAGES
    + themes1.PAGES
    + themes2.PAGES
    + info.PAGES
    + about.PAGES
)
