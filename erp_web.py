import streamlit as st
import pandas as pd

password = st.text_input("비밀번호를 입력하세요", type="password")

if password == "1234":
    st.title("📚 우리 매장 ERP")
    
    # 엑셀 시트처럼 PC에서 누르기 편한 '상단 탭' 만들기
    tab1, tab2, tab3 = st.tabs(["🛒 1. 소매 장부", "🤝 2. 외상 장부", "🏢 3. 매입 장부"])
    
    # --- [첫 번째 탭: 소매 장부] ---
    with tab1:
        st.header("🛒 일반 소매 장부")
        # 키보드로 타이핑할 때 창끼리 헷갈리지 않게 key 값을 다르게 줍니다.
        search_item = st.text_input("🔍 품목 이름 검색", key="item")
        if search_item:
            st.write(f"'{search_item}' 품목을 찾았습니다! (계산기 연결 예정)")

    # --- [두 번째 탭: 외상 장부] ---
    with tab2:
        st.header("🤝 외상 거래처 장부")
        search_customer = st.text_input("🔍 거래처 상호명 검색", key="customer")
        if search_customer:
            st.write(f"'{search_customer}' 장부를 엽니다! (외상 내역 연결 예정)")

    # --- [세 번째 탭: 매입 장부] ---
    with tab3:
        st.header("🏢 매입(구매처) 장부")
        search_vendor = st.text_input("🔍 구매처 이름 검색", key="vendor")
        if search_vendor:
            st.write(f"'{search_vendor}' 장부를 엽니다! (매입 내역 연결 예정)")

elif password != "":
    st.error("비밀번호가 틀렸습니다.")
