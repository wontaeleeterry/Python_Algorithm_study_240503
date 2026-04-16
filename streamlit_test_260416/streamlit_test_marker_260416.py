import streamlit as st
import pandas as pd
import pydeck as pdk

# -----------------------------
# Page Title
# -----------------------------
st.markdown("<h1 style='font-weight:bold;'>Busan Travel Plan</h1>", unsafe_allow_html=True)
st.markdown("<h3>부산 2박 3일 코스</h3>", unsafe_allow_html=True)

# -----------------------------
# Tourist Spots Data
# -----------------------------
places = [
    {
        "관광지": "해운대 해수욕장",
        "추천 이유": "부산의 대표 해변으로 낮과 밤 모두 아름다운 풍경을 즐길 수 있습니다.",
        "lat": 35.1587,
        "lon": 129.1604
    },
    {
        "관광지": "감천문화마을",
        "추천 이유": "알록달록한 집들과 예술 골목이 어우러진 부산 대표 포토 스팟입니다.",
        "lat": 35.0970,
        "lon": 129.0106
    },
    {
        "관광지": "태종대",
        "추천 이유": "절벽과 푸른 바다가 만들어내는 웅장한 자연 풍경이 매력적입니다.",
        "lat": 35.0527,
        "lon": 129.0872
    },
    {
        "관광지": "광안리 해수욕장",
        "추천 이유": "광안대교 야경과 감성적인 카페 거리로 유명합니다.",
        "lat": 35.1532,
        "lon": 129.1187
    },
    {
        "관광지": "해동 용궁사",
        "추천 이유": "바다 절벽 위에 자리한 아름다운 사찰로 일출 명소입니다.",
        "lat": 35.1886,
        "lon": 129.2234
    }
]

df = pd.DataFrame(places)

# -----------------------------
# Table
# -----------------------------
st.subheader("추천 관광지")
st.table(df[["관광지", "추천 이유"]])

# -----------------------------
# Map with Red Markers + Bright Style
# -----------------------------
st.subheader("여행 지도")

marker_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[lon, lat]',
    get_fill_color='[255, 0, 0, 180]',  # 빨간색
    get_radius=500,
    pickable=True
)

text_layer = pdk.Layer(
    "TextLayer",
    data=df,
    get_position='[lon, lat]',
    get_text='관광지',
    get_size=16,
    get_color='[0, 0, 0]',   # 검정 글씨
    get_pixel_offset=[0, 20]
)

view_state = pdk.ViewState(
    latitude=35.14,
    longitude=129.12,
    zoom=10
)

deck = pdk.Deck(
    map_style="light",   # 밝은 지도 스타일
    initial_view_state=view_state,
    layers=[marker_layer, text_layer],
    tooltip={"text": "{관광지}\n{추천 이유}"}
)

st.pydeck_chart(deck)