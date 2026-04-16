'''
Python의 Streamlit을 사용하여 부산 여행 안내 서비스를 만드는 코드를 작성해주세요.

다음 요구사항을 반드시 모두 반영해주세요.

1. 상단에 굵은 큰 글씨로 "Busan Travel Plan"을 출력하세요.
2. 그 아래 1번보다 작은 글씨로 "부산 2박 3일 코스"를 출력하세요.
3. 부산의 대표 관광지 5곳을 데이터로 사용하세요.
   - 해운대 해수욕장
   - 감천문화마을
   - 태종대
   - 광안리 해수욕장
   - 해동 용궁사
4. 각 관광지에 대해 다음 정보를 포함하세요.
   - 관광지명
   - 추천 이유
   - 위도(lat)
   - 경도(lon)
5. 표(table)를 사용하여 다음 2개의 컬럼만 출력하세요.
   - 관광지
   - 추천 이유
6. 지도는 streamlit에서 pydeck을 사용하여 구현하세요.
7. 지도는 밝은 스타일(light theme)로 설정하세요.
8. 각 관광지 위치에는 빨간색 마커를 표시하세요.
9. 각 마커 위 또는 근처에 관광지 이름(TextLayer)을 함께 표시하세요.
10. 마우스를 마커 위에 올리면 관광지명과 추천 이유가 tooltip으로 보이도록 하세요.
11. 지도의 중심은 부산 전체가 잘 보이도록 설정하세요.
12. 최종 결과는 바로 실행 가능한 하나의 Python 스크립트 형태로 작성하세요.
13. 코드에는 적절한 주석을 포함하여 초보자도 이해하기 쉽게 작성하세요.
'''

import streamlit as st
import pandas as pd
import pydeck as pdk

# 1. 페이지 설정 및 제목 출력
st.set_page_config(page_title="Busan Travel Plan", layout="wide")

st.markdown("# **Busan Travel Plan**")  # 1번 요구사항: 굵은 큰 글씨
st.markdown("### 부산 2박 3일 코스")     # 2번 요구사항: 작은 글씨

# 3, 4. 관광지 데이터 정의 (명칭, 추천 이유, 위도, 경도)
busan_data = [
    {"관광지": "해운대 해수욕장", "추천 이유": "부산을 대표하는 해변으로 산책과 야경이 일품입니다.", "lat": 35.1587, "lon": 129.1603},
    {"관광지": "감천문화마을", "추천 이유": "한국의 산토리니로 불리는 알록달록한 계단식 마을입니다.", "lat": 35.0975, "lon": 129.0106},
    {"관광지": "태종대", "추천 이유": "깎아지른 해안 절벽과 탁 트인 바다 전망을 즐길 수 있습니다.", "lat": 35.0528, "lon": 129.0881},
    {"관광지": "광안리 해수욕장", "추천 이유": "화려한 광안대교의 야경과 트렌디한 카페가 많습니다.", "lat": 35.1532, "lon": 129.1189},
    {"관광지": "해동 용궁사", "추천 이유": "바다와 가장 가까운 곳에 위치한 아름다운 사찰입니다.", "lat": 35.1885, "lon": 129.2234}
]

df = pd.DataFrame(busan_data)

# 5. 표(Table) 출력: 관광지와 추천 이유 컬럼만 표시
st.write("### 주요 관광지 정보")
st.table(df[["관광지", "추천 이유"]])

# 6-11. Pydeck을 이용한 지도 구현
st.write("### 부산 관광 지도")

# 빨간색 마커 표시를 위한 ScatterplotLayer (8번 요구사항)
icon_layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position="[lon, lat]",
    get_color="[255, 0, 0, 160]",  # 빨간색 (RGBA)
    get_radius=200,
    pickable=True,  # 툴팁을 위해 클릭/마우스 오버 가능하게 설정
)

# 관광지 이름을 표시하기 위한 TextLayer (9번 요구사항)
text_layer = pdk.Layer(
    "TextLayer",
    df,
    get_position="[lon, lat]",
    get_text="관광지",
    get_size=16,
    get_color=[0, 0, 0],
    get_alignment_baseline="'bottom'",
)

# 지도의 초기 중심점 설정 (11번 요구사항: 부산 전체가 잘 보이도록 설정)
view_state = pdk.ViewState(
    latitude=35.13, 
    longitude=129.10, 
    zoom=10.5, 
    pitch=0
)

# 툴팁 설정 (10번 요구사항: 마우스 오버 시 관광지명과 추천 이유 표시)
tooltip = {
    "html": "<b>관광지:</b> {관광지} <br/> <b>추천 이유:</b> {추천 이유}",
    "style": {"backgroundColor": "steelblue", "color": "white"}
}

# 최종 지도 출력 (7번 요구사항: 라이트 테마 설정)
r = pdk.Deck(
    layers=[icon_layer, text_layer],
    initial_view_state=view_state,
    map_style="light",  # 밝은 스타일
    tooltip=tooltip
)

st.pydeck_chart(r)