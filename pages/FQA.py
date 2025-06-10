import streamlit as st
import pandas as pd
import pymysql

# 캐시 데이터 불러오기
@st.cache_data
def fetch_data():
    conn = pymysql.connect(
        host='192.168.0.22',
        user='team_2',
        passwd='123',
        database='sk15_2team',
        port=3306
    )
    query = "SELECT question, answer, division FROM fqa;"
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    conn.close()
    columns = ['question', 'answer', 'division']
    df = pd.DataFrame(data, columns=columns)
    return df

# 🔍 필터 함수
def filter_df(df, search_term=None, keyword=None):
    if search_term:
        df = df[df['question'].str.contains(search_term, case=False, na=False)]
    if keyword:
        df = df[df['question'].str.contains(keyword, case=False, na=False)]
    return df

def main():
    st.markdown("<h1 style='text-align: center;'>❓ 자주 하는 질문 FAQ</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>궁금하신 키워드를 입력하세요!</p>", unsafe_allow_html=True)

    df = fetch_data()

    # 🔍 검색어 입력창
    search_query = st.text_input("🔍 검색어를 입력하세요")

    # 🏷️ 주요 키워드 버튼
    keyword = None
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("전체보기"):
            keyword = ""
    with col2:
        if st.button("🛒 구매"):
            keyword = "구매"
    with col3:
        if st.button("📦 판매"):
            keyword = "판매"
    with col4:
        if st.button("🔧 수리"):
            keyword = "수리"
    with col5:
        if st.button("⚠️ 주의"):
            keyword = "주의"

    # 🔍 검색어 + 키워드 필터 동시 적용
    df = filter_df(df, search_term=search_query, keyword=keyword)

    # 📂 division 기반 탭
    tab1, tab2, tab3 = st.tabs(["⚠️ 주의사항 (caution)", "📋 체크리스트 (checklist)", "📁 기타 (ect)"])
    tab_div_map = {
        tab1: "caution",
        tab2: "checklist",
        tab3: "ect"
    }

    for tab, div_name in tab_div_map.items():
        with tab:
            division_df = df[df['division'] == div_name]

            if division_df.empty:
                st.info("해당 조건에 맞는 질문이 없습니다.")
            else:
                for _, row in division_df.iterrows():
                    with st.expander("❓ " + row['question']):
                        st.write("💡 " + row['answer'])

if __name__ == "__main__":
    main()
