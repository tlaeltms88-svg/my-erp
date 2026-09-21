import streamlit as st
import pandas as pd
import os
import csv

# 웹사이트 전체 화면 설정 (반드시 제일 위에 있어야 함)
st.set_page_config(page_title="미니 ERP 시스템", layout="wide")

# ------------------------------------
# 🔒 비밀번호 설정 (여기에 원하는 비밀번호를 적으세요!)
# ------------------------------------
MY_PASSWORD = "132412"

# --- 1. 로그인 화면 (자물쇠) ---
# 로그인을 성공했는지 기억하는 저장소
if "login_success" not in st.session_state:
    st.session_state["login_success"] = False

# 로그인을 아직 안 했다면? -> 로그인 화면만 보여줌
if not st.session_state["login_success"]:
    st.title("🔒 서건 상사 미니 ERP (비공개)")
    st.info("외부 접속이 차단된 안전한 페이지입니다. 비밀번호를 입력하세요.")
    
    pwd = st.text_input("비밀번호", type="password") # type="password"로 하면 입력할 때 까만 점(●●●●)으로 가려집니다!
    
    if st.button("로그인"):
        if pwd == MY_PASSWORD:
            st.session_state["login_success"] = True
            st.rerun() # 비밀번호가 맞으면 화면을 새로고침해서 ERP를 켬
        else:
            st.error("비밀번호가 틀렸습니다! 다시 확인해주세요.")
            
    st.stop() # 🛑 로그인을 안 하면 여기서 프로그램을 멈추고 아래 ERP 코드는 절대 실행 안 함!


# --- 2. 진짜 ERP 화면 (로그인 성공 시에만 보임) ---
# 파일 이름 지정
filename = "erp_data.csv"

st.title("📊 웹기반 미니 ERP 시스템 (모바일 지원)")

def load_data():
    if os.path.exists(filename):
        df = pd.read_csv(filename, names=["상품명", "수량", "가격"], dtype=str)
        df['상품명'] = df['상품명'].str.strip()
        return df
    else:
        return pd.DataFrame(columns=["상품명", "수량", "가격"])

df = load_data()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 상품 관리")
    
    with st.expander("➕ 신규 상품 등록", expanded=True):
        with st.form("add_form", clear_on_submit=True):
            new_name = st.text_input("상품명")
            new_qty = st.text_input("수량")
            new_price = st.text_input("가격(원)")
            submit_btn = st.form_submit_button("상품 등록하기")
            
            if submit_btn:
                if new_name and new_qty:
                    with open(filename, mode="a", encoding="utf-8-sig", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([new_name.strip(), new_qty.strip(), new_price.strip()])
                    st.success(f"'{new_name}' 등록 완료!")
                    st.rerun() 
                else:
                    st.warning("상품명과 수량을 모두 입력해주세요.")
    
    with st.expander("🗑️ 상품 삭제"):
        if not df.empty:
            item_list = df["상품명"].tolist()
            delete_name = st.selectbox("삭제할 상품을 선택하세요", item_list)
            if st.button("삭제 실행", type="primary"):
                new_df = df[df["상품명"] != delete_name]
                new_df.to_csv(filename, index=False, header=False, encoding='utf-8-sig')
                st.success(f"'{delete_name}' 삭제 완료!")
                st.rerun()
        else:
            st.info("삭제할 데이터가 없습니다.")

with col2:
    st.subheader("📦 현재 재고 목록")
    
    search_keyword = st.text_input("🔍 상품 검색 (이름의 일부만 입력해도 됩니다)")
    
    if search_keyword:
        display_df = df[df["상품명"].str.contains(search_keyword, na=False)]
    else:
        display_df = df
        
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# 오른쪽 위 로그아웃 버튼
st.sidebar.button("로그아웃", on_click=lambda: st.session_state.update(login_success=False))