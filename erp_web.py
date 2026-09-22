import streamlit as st
import pandas as pd

# --- 영수증(장바구니)을 기억하는 공간 만들기 ---
if "cart" not in st.session_state:
    st.session_state.cart = []

password = st.text_input("비밀번호를 입력하세요", type="password")

if password == "132412":
    st.title("📚 우리 매장 ERP")
    
    tab1, tab2, tab3 = st.tabs(["🛒 1. 소매 장부", "🤝 2. 외상 장부", "🏢 3. 매입 장부"])
    
    # --- [첫 번째 탭: 소매 장부 (포스기 계산대)] ---
    with tab1:
        st.header("🛒 소매 장부 (계산대)")
        
        # 화면을 왼쪽(검색)과 오른쪽(영수증)으로 반반 나눕니다.
        col1, col2 = st.columns([1, 1])
        
        # [왼쪽 화면: 검색 및 추가]
        with col1:
            st.subheader("1. 품목 검색")
            search_item = st.text_input("🔍 품목 이름의 일부를 입력하세요", key="item")
            
            if search_item:
                try:
                    df = pd.read_csv("erp_data.csv")
                    # 검색어가 포함된 상품 찾기
                    result = df[df['상품명'].str.contains(search_item, na=False)]
                    
                    if not result.empty:
                        # 찾은 상품 목록을 보여주고 하나를 고르게 합니다.
                        item_names = result['상품명'].tolist()
                        selected_item = st.selectbox("👉 장바구니에 담을 정확한 상품을 선택하세요", item_names)
                        
                        # 선택한 상품의 가격 가져오기 (엑셀에 쉼표가 있을 수 있어 숫자로 변환)
                        price_str = result[result['상품명'] == selected_item]['가격'].values[0]
                        unit_price = int(str(price_str).replace(',', ''))
                        
                        # 수량 입력받기
                        qty = st.number_input("📦 수량", min_value=1, value=1)
                        
                        # 담기 버튼
                        if st.button("➕ 영수증에 담기"):
                            st.session_state.cart.append({
                                "상품명": selected_item,
                                "수량": qty,
                                "단가": unit_price,
                                "금액": unit_price * qty
                            })
                            st.rerun() # 화면을 갱신해서 영수증에 바로 띄움
                    else:
                        st.warning("해당하는 품목이 없습니다.")
                except Exception as e:
                    st.error("데이터를 읽는 중 오류가 발생했습니다. 엑셀 파일을 확인해주세요.")

        # [오른쪽 화면: 영수증 및 총액 계산]
        with col2:
            st.subheader("2. 현재 영수증")
            
            # 장바구니에 물건이 하나라도 있다면 표로 보여주기
            if len(st.session_state.cart) > 0:
                cart_df = pd.DataFrame(st.session_state.cart)
                st.dataframe(cart_df, use_container_width=True)
                
                # '금액' 열을 다 더해서 총 결제금액 계산
                total_amount = cart_df['금액'].sum()
                st.markdown(f"### 💰 총 결제 금액: **{total_amount:,} 원**")
                
                # 영수증 초기화 버튼
                if st.button("🗑️ 영수증 비우기"):
                    st.session_state.cart = []
                    st.rerun()
            else:
                st.info("아직 담긴 품목이 없습니다. 왼쪽에서 검색 후 추가해주세요.")

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
