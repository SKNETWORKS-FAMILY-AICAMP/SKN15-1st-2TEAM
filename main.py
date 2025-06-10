# import streamlit as st
# import pymysql
# import pandas as pd

# st.set_page_config(page_title="TEAM PROJECT", layout="wide")

# st.markdown("""

# <h1 style='text-align: center; color: black;'>🚗 SKN_15기_2조 <br>    중고차 정보 통합 비교 사이트
# </h1> <hr style='border:1px solid lightgray'> """, unsafe_allow_html=True)
# st.markdown("### 🛠️ 차량 조건을 선택하세요")

# # 입력 폼
# col1, col2, col3 = st.columns(3)

# with col1:
#     model_name = st.text_input("🔍 모델명", placeholder="예: 소나타")

# with col2:
#     year = st.selectbox("📅 연식 이하", list(range(2000, 2026)))

# with col3:
#     origin = st.radio("🚩 수입 구분", ["국산", "수입","상관없음"], horizontal=True)
#     if origin == "상관없음":
#         origin = 0

# car_colors = [
# "흰색", "검정색", "회색", "은색", "빨간색", "파란색", "초록색", "노란색", "주황색",
# "갈색", "보라색", "분홍색", "청록색", "네이비", "골드", "샴페인", "버건디", "카키", "민트"
# ]

# col4, col5, col6 = st.columns(3)

# with col4:
#     color = st.selectbox("🎨 차량 색상", car_colors)

# with col5:
#     fuel_efficiency = st.selectbox("⛽ 연비 (km/L) 이하", list(range(5, 60, 5)))

# with col6:
#     fuel_type = st.radio("🛢️ 연료 종류", ["가솔린", "가스", "휘발유","상관없음"], horizontal=True)
#     if fuel_type == "상관없음":
#         fuel_type = 0

# col7, col8 = st.columns(2)

# with col7:
#     price = st.slider("💰 가격 (만원 단위)", 0, 10000, step=500)

# with col8:
#     mileage = st.slider("📍 주행거리 (만 km)", 0, 50, step=1)


# if st.button("➡️ 조건 확인"): # 값 저장
#     # 현재 세션 상태값 출력 (디버깅용)
#     # st.write("세션 상태 값:", st.session_state)
#     st.session_state["model_name"] = model_name
#     st.session_state["year"] = year
#     st.session_state["origin"] = origin
#     st.session_state["color"] = color
#     st.session_state["fuel_efficiency"] = fuel_efficiency
#     st.session_state["fuel_type"] = fuel_type
#     st.session_state["price"] = price
#     st.session_state["mileage"] = mileage

#     # MySQL에서 조건에 맞는 차량 데이터를 가져오는 함수
#     def sql_input():
#         # MySQL 연결 설정
#         conn = pymysql.connect(
#             host='192.168.0.22',         # DB 서버 주소
#             user='team_2',               # 사용자명
#             passwd='123',                # 비밀번호
#             database='sk15_2team',       # 데이터베이스 이름
#             port=3306                    # 포트 번호
#         )
#         cur = conn.cursor()

#         # 모델명, 연식, 색상, 연료, 연비, 가격(만원 → 원), 주행거리(만 km → km)
#         # NULL 값 일때, 제외 함

#         sql = "SELECT * FROM total WHERE 1=1\n"
#         if model_name:
#             sql += f"AND car_model LIKE '%{model_name}%'\n"
#         if color:
#             sql += f"AND car_color = '{color}'\n"
#         if year:
#             sql += f"AND car_year <= '{year}'\n"
#         if fuel_type:
#             sql += f"AND car_fuel_type = '{fuel_type}'\n"
#         if origin:
#             sql += f"AND no_use2 = '{origin}'\n"
#         if fuel_efficiency:
#             sql += f"AND car_fuel_effi <= '{fuel_efficiency}'\n"
#         if price:
#             sql += f"AND car_price <= {int(price) * 10000}\n"  # 만원 → 원
#         if mileage:
#             sql += f"AND car_distance <= {int(mileage) * 10000}\n"  # 만 km → km


#         print(sql)

#         # 쿼리 실행
#         cur.execute(sql)
#         result = cur.fetchall()

#         # 연결 종료
#         cur.close()
#         conn.close()

#         return result

#     #  결과 출력
#     results = sql_input()
#     df = pd.DataFrame(results)
#     st.write("📊 결과 목록:", df)
import streamlit as st
import pymysql
import pandas as pd

if "place1_sv" not in st.session_state:
    st.session_state.place1_sv = False
if "place2_sv" not in st.session_state:
    st.session_state.place2_sv = False
if "place3_sv" not in st.session_state:
    st.session_state.place3_sv = False



# 페이지 리스트 정의
pages = list(range(1,20))

# 세션 상태에 페이지 변수 초기화
if "page" not in st.session_state:
    st.session_state.page = pages[0]



# if 'db_conn' not in st.session_state:
#     st.session_state['db_conn'] = pymysql.connect(
#         host='222.112.208.67',         # DB 서버 주소
#         user='team_2',               # 사용자명
#         passwd='123',                # 비밀번호
#         database='sk15_2team',       # 데이터베이스 이름
#         port=3306  d
#     )
# 이후 코드에서는 st.session_state['db_conn']을 사용

st.set_page_config(page_title="TEAM PROJECT", layout="wide")

st.markdown("""
<h2 style='text-align: center; color: black;'> 🚗중고차 정보 통합 비교 사이트
</h2> <hr style='border:1px solid lightgray'> """, unsafe_allow_html=True)

coll1, coll2 = st.columns([9, 1])
with coll1:
    st.markdown("### 🛠️ 차량 조건을 선택하세요")

with coll2:
    button_search =  st.button("➡️ 조건 확인")
    


# 입력 폼
col1, col2, col3 = st.columns(3)
yearli = ['선택 안함'] + list(range(2000, 2026))
with col1:
    model_name = st.text_input("🔍 모델명", placeholder="예: 소나타")

with col2:
    year = st.selectbox("📅 연식 이하", yearli)
    if year == "선택 안함":
        year = None

with col3:
    origin = st.radio("🚩 수입 구분", ["상관없음", "국산", "수입"], horizontal=True)

car_colors = ["선택 안함", 
"흰색", "검정색", "회색", "은색", "빨간색", "파란색", "초록색", "노란색", "주황색",
"갈색", "보라색", "분홍색", "청록색", "네이비", "골드", "샴페인", "버건디", "카키", "민트"
]

col4, col5, col6 = st.columns(3)
effi_li = ['선택 안함'] + list(range(5, 60, 5))

with col4:
    color = st.selectbox("🎨 차량 색상", car_colors)

with col5:
    fuel_efficiency = st.selectbox("⛽ 연비 (km/L) 이하", effi_li)
    if fuel_efficiency =="선택 안함":
        fuel_efficiency = None

with col6:
    fuel_type = st.radio("🛢️ 연료 종류", ["상관없음", "가솔린", "가스", "휘발유"], horizontal=True)

col7, col8 = st.columns(2)

with col7:
    price = st.slider("💰 가격 (만원 단위)", 0, 10000, step=500)

with col8:
    mileage = st.slider("📍 주행거리 (만 km)", 0, 50, step=1)


def sql_get(quary):
    if 'conn' not in st.session_state:
        st.session_state['conn'] = pymysql.connect(
            host='222.112.208.67',
            user='team_2',
            passwd='123',
            database='sk15_2team',
            port=3306
        )
    cur = st.session_state['conn'].cursor()
    cur.execute(quary)

    return cur.fetchall()

place1 = st.empty()
place2 = [st.empty() for _ in range(10)]
place3 = st.empty()




if button_search: # 값 저장
    # 현재 세션 상태값 출력 (디버깅용)
    # st.write("세션 상태 값:", st.session_state)

    if 'model_name' not in st.session_state:
        st.session_state["model_name"] = model_name
    if 'year' not in st.session_state:
        st.session_state["year"] = year
    if 'origin' not in st.session_state:
        st.session_state["origin"] = origin
    if 'color' not in st.session_state:
        st.session_state["color"] = color
    if 'fuel_efficiency' not in st.session_state:
        st.session_state["fuel_efficiency"] = fuel_efficiency
    if 'fuel_type' not in st.session_state:
        st.session_state["fuel_type"] = fuel_type
    if 'price' not in st.session_state:
        st.session_state["price"] = price
    if 'mileage' not in st.session_state:
        st.session_state["mileage"] = mileage

    sql = "SELECT car_model, car_distance, car_price, car_link, car_option, seller_name, site_type FROM total WHERE 1=1\n"
    if model_name:
        sql += f"AND car_model LIKE '%{model_name}%'\n"
    if color and color != "선택 안함":
        sql += f"AND car_color = '{color}'\n"
    if year:
        sql += f"AND car_year <= {year}\n"
    if fuel_type:
        if fuel_type != "상관없음":
            sql += f"AND car_fuel_type = '{fuel_type}'\n"
    if origin:
        if origin != "상관없음":
            sql += f"AND no_use2 = '{origin}'\n"
    if fuel_efficiency:
        sql += f"AND car_fuel_effi <= {fuel_efficiency}\n"
    if price:
        sql += f"AND car_price <= {int(price) * 10000}\n"  # 만원 → 원
    if mileage:
        sql += f"AND car_distance <= {int(mileage) * 10000}\n"  # 만 km → km
    # sql = sql + "and site_type = '엔카' order by car_link desc"

    
    rt = (sql_get(sql))
    col = ['모델명', '주행거리', '가격', '링크', '옵션', '판매자', '사이트']

    df = pd.DataFrame(data = rt, columns=col)
    df['가격'] = pd.to_numeric(df['가격'], errors='coerce')
    df['가격'] = df['가격'].astype('Int64')
    max_value = str(df['가격'].max(numeric_only=True))[:-5]+'만원'
    min_value = str(df['가격'].min(numeric_only=True))[:-5]+'만원'
    mean = str(int(df['가격'].mean(numeric_only=True)))[:-5]+'만원'

    st.session_state.place1_sv = True
    st.session_state.place2_sv = True
    st.session_state.place3_sv = True



if st.session_state.place1_sv:
    with place1:
        st.markdown(
            f"""
            <hr style='border:1px solid #bbb; margin-bottom:40px;'>
            <h2 style='text-align: center;'>{min_value} ~ {max_value}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;평균 : {mean}</h2>
            <hr style='border:1px solid #bbb; margin-bottom:40px;'>
            """,
            unsafe_allow_html=True
        )

url_1 ="https://file2.bobaedream.co.kr/pds/CyberCar/1/774851/img_774851_1.jpg"
url_2 = "https://file2.bobaedream.co.kr/pds/CyberCar/9/775879/img_775879_1.jpg"
url_3 = "https://file4.bobaedream.co.kr/direct/2025/04/18/GA16501744967678_1.jpg"
url_4 = "https://file4.bobaedream.co.kr/direct/2025/03/10/Eh12401741588345_1.jpg"
url_5 = "https://file4.bobaedream.co.kr/direct/2025/05/23/Eh18591747960858_1.jpg"


page = st.session_state.page
size = 600
import random

if st.session_state.place3_sv:
    with place3:
        st.selectbox("페이지를 선택하세요", pages, index=pages.index(st.session_state.page))

#['모델명', '주행거리', '가격', '링크', '옵션', '판매자', '사이트']
if st.session_state.place2_sv:
    i = 0
    for p in place2:
        with p:
            row = df.iloc[i + (page-1)* 10 ]
            co1, co2 = st.columns(2)
            with co1:
                num = random.randint(1, 5)
                import streamlit as st
                if num == 1:
                    st.markdown(
                        f"<div style='text-align: center;'><img src='{url_1}' width='{size}'></div>",
                        unsafe_allow_html=True
                    )
                if num == 2:
                    st.markdown(
                        f"<div style='text-align: center;'><img src='{url_2}' width='{size}'></div>",
                        unsafe_allow_html=True
                    )
                if num == 3:
                    st.markdown(
                        f"<div style='text-align: center;'><img src='{url_3}' width='{size}'></div>",
                        unsafe_allow_html=True
                    )
                if num == 4:
                    st.markdown(
                        f"<div style='text-align: center;'><img src='{url_4}' width='{size}'></div>",
                        unsafe_allow_html=True
                    )
                if num == 5:
                    st.markdown(
                        f"<div style='text-align: center;'><img src='{url_5}' width='{size}'></div>",
                        unsafe_allow_html=True
                    )
                # if num == 1:
                #     st.image(url_1 , width=size)
                # if num == 2:
                #     st.image(url_2 , width=size)
                # if num == 3:
                #     st.image(url_3 , width=size)
                # if num == 4:
                #     st.image(url_4 , width=size)
                # if num == 5:
                #     st.image(url_5 , width=size)
            with co2:
                st.markdown(f"""
                            <div style="border:1px solid #eee; border-radius:10px; padding:18px 20px; margin-bottom:10px; background-color:#f9f9fc;">
                            <h4 style="margin-bottom:10px; color:#2c3e50;">{row['모델명']}</h4>
                            <ul style="list-style:none; padding:0; margin:0 0 10px 0;">
                            <li><b>주행거리:</b> {row['주행거리']}</li>
                            <li><b>가격:</b> {row['가격']}</li>
                            <li><b>옵션:</b> {row['옵션']}</li>
                            <li><b>판매자:</b> {row.get('판매자', '-')}</li>
                            <li><b>사이트:</b> {row.get('사이트', '-')}</li>
                            </ul>
                            <a href="{row['링크']}" target="_blank" style="color:#1565c0; text-decoration:underline; font-weight:bold;">
                            차량 상세 페이지 바로가기
                            </a>
                            </div>
                            """,
                            unsafe_allow_html=True)
                #['모델명', '주행거리', '가격', '링크', '옵션', '판매자', '사이트']
                # st.write(row['모델명'])
                # st.write(row['주행거리'])
                # st.write(row['가격'])
                # st.write(row['링크'])
                # st.write(row['옵션'])
            i +=1
            