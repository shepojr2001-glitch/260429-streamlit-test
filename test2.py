import streamlit as st

st.sidebar.header("사이드바")
option = st.sidebar.selectbox(
 "메뉴 선택",
 ["홈", "분석", "설정"]
)
st.write("선택:", option)
# 타이틀명
st.title("Text Elements")

# 서브 타이틀명
st.subheader("subheader")

# 마크다운
st.markdown("markdown")

col1, col2, col3 =st.columns(3)
with col1:
    st.subheader("방문자")
    st.write("300")
with col2:
    st.subheader("매출")
    st.write("30")
with col3:
    st.subheader("구매전환율")
    st.write("90")    

data=[
    {"월": "1월", "방문자":"", "매출": 100, "만족도":10},
    {"월": "2월", "방문자":"", "매출": 200, "만족도":10},
    {"월": "3월", "방문자":"", "매출": 150, "만족도":10},
    {"월": "4월", "방문자":"", "매출": 300, "만족도":10},
]

# 데이터 엘리먼츠
# 서브 타이틀명
st.subheader("Data Elements")

st.table(data)

st.json(data)

st.subheader("Chart Elements")

col4,col5,col6 = st.columns(3)

with col4:    
    st.line_chart(data,x="월",y="매출")
with col5:
    st.bar_chart(data,x="월",y="만족도")
with col6:
    st.area_chart(data,x="월",y="만족도")
    
#업로드
st.title("Media Elements")

col7, col8, col9 = st.columns(3)

with col7:
    upload_file1 = st.file_uploader(   "파일 업로드",
        type=["png","jpg","jpeg"],
        accept_multiple_files=False
    )
with col8:
    upload_file2 = st.file_uploader(   "파일 업로드",
        type=["MP3"],
        accept_multiple_files=False
    )
with col9:
    upload_file3 = st.file_uploader(   "파일 업로드",
        type=["MP4","MPEG4"],
        accept_multiple_files=False
    )        