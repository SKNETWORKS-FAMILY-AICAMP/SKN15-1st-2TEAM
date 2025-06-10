import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px

# ---------------------- [1] 캐시된 데이터 불러오기 함수 정의 ----------------------
@st.cache_data(ttl=600)
def fetch_data(query):
    conn = pymysql.connect(
        host='192.168.0.22',
        user='team_2',
        password='123',
        db='sk15_2team',
        charset='utf8mb4'
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ---------------------- [2] 정확한 브랜드 목록 불러오기 ----------------------
brand_query = """
SELECT m.manufacturer AS brand, COUNT(*) AS count
FROM MANUFACTURER m
JOIN total t ON t.car_model LIKE CONCAT(m.manufacturer, '%')
GROUP BY m.manufacturer
ORDER BY count DESC
LIMIT 6;
"""
brand_df = fetch_data(brand_query)

# 🔘 브랜드 선택 위젯
selected_brand = st.selectbox("브랜드를 선택하세요", brand_df['brand'])

# ---------------------- [3] 선택된 브랜드의 모델 목록 가져오기 ----------------------
model_query = f"""
SELECT car_model, COUNT(*) AS count
FROM total
WHERE car_model LIKE '{selected_brand}%'
GROUP BY car_model
ORDER BY count DESC
LIMIT 6;
"""
model_df = fetch_data(model_query)

# 🔘 모델 선택 위젯
selected_model = st.selectbox("모델을 선택하세요", model_df['car_model'])

# 🔘 차량 유형 선택
car_type = st.radio("차량 유형", ("전체", "국산", "수입"))

# ---------------------- [4] 색상 분포 데이터 ----------------------
color_query = f"""
SELECT car_color, COUNT(*) AS count
FROM total
WHERE car_model = '{selected_model}'
{f"AND car_type = '{car_type}'" if car_type != "전체" else ""}
GROUP BY car_color
ORDER BY count DESC;
"""
color_df = fetch_data(color_query)

# ---------------------- [5] 가격 분포 데이터 ----------------------
price_query = f"""
SELECT car_price
FROM total
WHERE car_model = '{selected_model}'
{f"AND car_type = '{car_type}'" if car_type != "전체" else ""};
"""
price_df = fetch_data(price_query)

# ---------------------- [6] 탭 구성 ----------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 브랜드별 차량 비율",
    f"📊 {selected_brand} 모델별 차량 비율",
    f"🎨 {selected_brand} {selected_model} 색상 분포",
    f"💰 {selected_brand} {selected_model} 가격 분포"
])

# ---------------------- [탭 1] 브랜드 비율 ----------------------
with tab1:
    st.subheader("브랜드별 차량 비율")
    fig1 = px.pie(brand_df, values='count', names='brand', title='브랜드별 중고차 수')
    st.plotly_chart(fig1)

# ---------------------- [탭 2] 모델 비율 ----------------------
with tab2:
    st.subheader(f"{selected_brand} 모델별 차량 비율")
    fig2 = px.pie(model_df, values='count', names='car_model', title=f'{selected_brand} 모델 비율')
    st.plotly_chart(fig2)

# ---------------------- [탭 3] 색상 분포 ----------------------
with tab3:
    st.subheader(f"{selected_brand} {selected_model} 색상 분포")
    if not color_df.empty:
        fig3 = px.pie(color_df, values='count', names='car_color', title='색상 분포')
        st.plotly_chart(fig3)
    else:
        st.warning("해당 모델의 색상 정보가 없습니다.")

# ---------------------- [탭 4] 가격 분포 ----------------------
with tab4:
    st.subheader(f"{selected_brand} {selected_model} 가격 분포")
    if not price_df.empty:
        # 📌 가격을 '만원 단위'로 변환
        price_df['car_price'] = price_df['car_price'] // 10000  # 원 → 만원

        # 📌 nbins 조정으로 폭 좁히기 (기존보다 더 세분화)
        fig4 = px.histogram(
            price_df,
            x='car_price',
            nbins=40,  # 더 많은 구간으로 세분화
            title='가격 히스토그램 (만원 단위)'
        )
        fig4.update_layout(
            xaxis_title='가격 (만원)',  # x축 라벨
            yaxis_title='차량 수',
            bargap=0.05  # 막대 사이 간격 조정
        )
        st.plotly_chart(fig4)
    else:
        st.warning("해당 모델의 가격 정보가 없습니다.")
