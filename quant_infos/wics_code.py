"""
wics_code

기업 분류 코드 표준 구분법
"""
WICS = {10:'에너지', 
        15:'소재', 
        20:'산업재', 
        25:'경기관련소비재', 
        30:'필수소비재', 
        35:'건강관리',
        40:'금융', 
        45:'IT', 
        50:'커뮤니케이션서비스', 
        55:'유틸리티', # 대분류
        1010:'에너지',
        1510:'소재',
        2010:'자본재',
        2020:'상업서비스와공급품',
        2030:'운송',
        2510:'자동차와부품',
        2520:'내구소비재와의류',
        2530:'호텔,레스토랑,레저 등',
        2550:'소매(유통)',
        2560:'교육서비스',
        3010:'식품과기본식료품소매',
        3020:'식품,음료,담배',
        3030:'가정용품과개인용품',
        3510:'건강관리장비와서비스',
        3520:'제약과생물공학',
        4010:'은행',
        4020:'증권',
        4030:'다각화된금융',
        4040:'보험',
        4050:'부동산',
        4510:'소프트웨어와서비스',
        4520:'기술하드웨어와장비',
        4530:'반도체와반도체장비',
        4535:'전자와 전기제품',
        4540:'디스플레이',
        5010:'전기통신서비스',
        5020:'미디어와엔터테인먼트',
        5510:'유틸리티', # 중분류
        # 101010:'에너지장비및서비스',
        # 101020:'석유와가스',
        # 151010:'화학',
        # 151030:'포장재',
        # 151040:'비철금속',
        # 151050:'철강',
        # 151060:'종이와목재',
        # 201010:'우주항공과국방',
        # 201020:'건축제품',
        # 201025:'건축자재',
        # 201030:'건설',
        # 201035:'가구',
        # 201040:'전기장비',
        # 201050:'복합기업',
        # 201060:'기계',
        # 201065:'조선',
        # 201070:'무역회사와판매업체',
        # 202010:'상업서비스와공급품',
        # 203010:'항공화물운송과물류',
        # 203020:'항공사',
        # 203030:'해운사',
        # 203040:'도로와철도운송',
        # 203050:'운송인프라',
        # 251010:'자동차부품',
        # 251020:'자동차',
        # 252040:'가정용기기와용품',
        # 252050:'레저용장비와제품',
        # 252060:'섬유,의류,신발,호화품',
        # 252065:'화장품',
        # 252070:'문구류',
        # 253010:'호텔,레스토랑,레저',
        # 253020:'다각화된소비자서비스',
        # 255010:'판매업체',
        # 255020:'인터넷과카탈로그소매',
        # 255030:'백화점과일반상점',
        # 255040:'전문소매',
        # 256010:'교육서비스',
        # 301010:'식품과기본식료품소매',
        # 302010:'음료',
        # 302020:'식품',
        # 302030:'담배',
        # 303010:'가정용품',
        # 351010:'건강관리장비와용품',
        # 351020:'건강관리업체및서비스',
        # 351030:'건강관리기술',
        # 352010:'생물공학',
        # 352020:'제약',
        # 352030:'생명과학도구및서비스',
        # 401010:'은행',
        # 402010:'증권',
        # 403020:'창업투자',
        # 403030:'카드',
        # 403040:'기타금융',
        # 404010:'손해보험',
        # 404020:'생명보험',
        # 405020:'부동산',
        # 451020:'IT서비스',
        # 451030:'소프트웨어',
        # 452010:'통신장비',
        # 452015:'핸드셋',
        # 452020:'컴퓨터와주변기기',
        # 452030:'전자장비와기기',
        # 452040:'사무용전자제품',
        # 453010:'반도체와반도체장비',
        # 453510:'전자제품',
        # 453520:'전기제품',
        # 454010:'디스플레이 패널',
        # 454020:'디스플레이 장비 및 부품',
        # 501010:'다각화된통신서비스',
        # 501020:'무선통신서비스',
        # 502010:'광고',
        # 502020:'방송과엔터테인먼트',
        # 502030:'출판',
        # 502040:'게임엔터테인먼트',
        # 502050:'양방향미디어와서비스',
        # 551010:'전기유틸리티',
        # 551020:'가스유틸리티',
        # 551030:'복합유틸리티',
        # 551050:'독립전력생산및에너지거래', # 소분류
        }
 
def wics_url(date, wics_code):
    url =f'http://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt={date}&sec_cd=G{wics_code}'
    return url