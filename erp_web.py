import streamlit as st
import pandas as pd

# --- 영수증(장바구니)을 기억하는 공간 ---
if "cart" not in st.session_state:
    st.session_state.cart = []

password = st.text_input("비밀번호를 입력하세요", type="password")

if password == "132412":
    st.title("📚 우리 매장 ERP")
    
    tab1, tab2, tab3 = st.tabs(["🛒 1. 소매 장부", "🤝 2. 외상 장부", "🏢 3. 매입 장부"])
    
    # --- [첫 번째 탭: 소매 장부 (포스기 계산대)] ---
    with tab1:
        st.header("🛒 소매 장부 (계산대)")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("1. 품목 검색")
            search_item = st.text_input("🔍 품목 이름의 일부를 입력하세요", key="item")
            
            if search_item:
                try:
                    # 💡 수정: utf-8-sig를 사용해 눈에 안보이는 유령 기호(BOM) 완벽 제거
                    try:
                        df = pd.read_csv("erp_data.csv", encoding="utf-8-sig")
                    except UnicodeDecodeError:
                        df = pd.read_csv("erp_data.csv", encoding="cp949")
                    
                    # 띄어쓰기 싹 제거
                    df.columns = df.columns.str.strip()
                    
                    # '상품명' 기둥이 있는지 확인
                    if '상품명' not in df.columns:
                        # 없다면 실제 기둥 이름이 뭔지 화면에 보여주기
                        st.error(f"오류: '상품명' 열을 찾을 수 없습니다. 현재 엑셀 파일의 열 이름은 다음과 같습니다: {list(df.columns)}")
                    else:
                        result = df[df['상품명'].astype(str).str.contains(search_item, na=False)]
                        
                        if not result.empty:
                            item_names = result['상품명'].tolist()
                            selected_item = st.selectbox("👉 장바구니에 담을 정확한 상품을 선택하세요", item_names)
                            
                            price_str = result[result['상품명'] == selected_item]['가격'].values[0]
                            # 가격에 쉼표나 문자가 있어도 숫자로 강제 변환
                            unit_price = int(str(price_str).replace(',', '').replace('원', '').strip())
                            
                            qty = st.number_input("📦 수량", min_value=1, value=1)
                            
                            if st.button("➕ 영수증에 담기"):
                                st.session_state.cart.append({
                                    "상품명": selected_item,
                                    "수량": qty,
                                    "단가": unit_price,
                                    "금액": unit_price * qty
                                })
                                st.rerun() 
                        else:
                            st.warning("해당하는 품목이 없습니다.")
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

        with col2:
            st.subheader("2. 현재 영수증")
            if len(st.session_state.cart) > 0:
                cart_df = pd.DataFrame(st.session_state.cart)
                st.dataframe(cart_df, use_container_width=True)
                
                total_amount = cart_df['금액'].sum()
                st.markdown(f"### 💰 총 결제 금액: **{total_amount:,} 원**")
                
                if st.button("🗑️ 영수증 비우기"):
                    st.session_state.cart = []
                    st.rerun()
            else:
                st.info("아직 담긴 품목이 없습니다. 왼쪽에서 검색 후 추가해주세요.")

    with tab2:
        st.header("🤝 외상 거래처 장부")
        search_customer = st.text_input("🔍 거래처 상호명 검색", key="customer")
        if search_customer:
            st.write(f"'{search_customer}' 장부를 엽니다! (외상 내역 연결 예정)")

    with tab3:
        st.header("🏢 매입(구매처) 장부")
        search_vendor = st.text_input("🔍 구매처 이름 검색", key="vendor")
        if search_vendor:
            st.write(f"'{search_vendor}' 장부를 엽니다! (매입 내역 연결 예정)")

elif password != "":
    st.error("비밀번호가 틀렸습니다.")
