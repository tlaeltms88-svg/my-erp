import tkinter as tk
from tkinter import messagebox, simpledialog
import csv

filename = "erp_data.csv"

def on_select(event):
    try:
        index = listbox.curselection()[0]
        selected_text = listbox.get(index)
        
        parts = selected_text.split(" | ")
        name = parts[0].replace("상품명: ", "").strip()
        quantity = parts[1].replace("수량: ", "").replace("개", "").strip()
        price = parts[2].replace("가격: ", "").replace("원", "").replace("정보없음", "").strip()
        
        clear_entries()
        entry_name.insert(0, name)
        entry_quantity.insert(0, quantity)
        entry_price.insert(0, price)
    except:
        pass

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)

def add_item():
    name = entry_name.get().strip()
    quantity = entry_quantity.get().strip()
    price = entry_price.get().strip()

    if name == "" or quantity == "":
        messagebox.showwarning("경고", "상품명과 수량을 입력해주세요!")
        return

    with open(filename, mode="a", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, quantity, price])

    messagebox.showinfo("성공", f"'{name}' 등록 완료!")
    clear_entries()
    view_items()

def view_items():
    listbox.delete(0, tk.END)
    try:
        with open(filename, mode="r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    # 화면에 보여줄 때 원본 엑셀의 띄어쓰기 찌꺼기들을 다 무시하고 보여줌
                    clean_name = row[0].strip()
                    clean_qty = row[1].strip()
                    if len(row) >= 3:
                        clean_price = row[2].strip()
                        listbox.insert(tk.END, f"상품명: {clean_name} | 수량: {clean_qty}개 | 가격: {clean_price}원")
                    else:
                        listbox.insert(tk.END, f"상품명: {clean_name} | 수량: {clean_qty}개 | 가격: 정보없음")
    except FileNotFoundError:
        pass

def search_item():
    search_name = simpledialog.askstring("상품 검색", "검색할 단어의 일부를 입력하세요:")
    if not search_name: 
        return

    listbox.delete(0, tk.END)
    found = False
    try:
        with open(filename, mode="r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    clean_name = row[0].strip()
                    if search_name in clean_name:
                        found = True
                        clean_qty = row[1].strip()
                        if len(row) >= 3:
                            clean_price = row[2].strip()
                            listbox.insert(tk.END, f"상품명: {clean_name} | 수량: {clean_qty}개 | 가격: {clean_price}원")
                        else:
                            listbox.insert(tk.END, f"상품명: {clean_name} | 수량: {clean_qty}개 | 가격: 정보없음")
            
        if not found:
            messagebox.showwarning("결과 없음", f"'{search_name}'이(가) 포함된 상품이 없습니다.")
            view_items()
    except FileNotFoundError:
        messagebox.showerror("에러", "아직 저장된 데이터가 없습니다.")

def update_item():
    name = entry_name.get().strip()
    new_qty = entry_quantity.get().strip()
    new_price = entry_price.get().strip()
    
    if name == "":
        messagebox.showwarning("경고", "아래 목록에서 수정할 상품을 먼저 마우스로 클릭해주세요!")
        return
        
    updated = False
    rows = []
    try:
        with open(filename, mode="r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    # 💡 핵심 해결: 엑셀 파일 안의 글자(row[0])도 양옆 띄어쓰기를 없앤 뒤 비교!
                    if row[0].strip() == name:
                        row[0] = name # 수정하면서 엑셀 데이터의 띄어쓰기도 영구적으로 깨끗하게 고침
                        row[1] = new_qty
                        if len(row) >= 3:
                            row[2] = new_price
                        else:
                            row.append(new_price)
                        updated = True
                    rows.append(row)
                    
        if updated:
            with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            messagebox.showinfo("수정 완료", f"'{name}' 상품이 수정되었습니다.")
            view_items()
            clear_entries()
        else:
            messagebox.showwarning("오류", f"'{name}' 상품을 찾을 수 없습니다.")
    except FileNotFoundError:
        pass

def delete_item():
    name = entry_name.get().strip()
    if name == "":
        messagebox.showwarning("경고", "아래 목록에서 삭제할 상품을 먼저 마우스로 클릭해주세요!")
        return
        
    if messagebox.askyesno("삭제 확인", f"정말 '{name}' 상품을 삭제하시겠습니까?"):
        deleted = False
        rows = []
        try:
            with open(filename, mode="r", encoding="utf-8-sig") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        # 💡 핵심 해결: 삭제할 때도 양옆 띄어쓰기 무시하고 찾기
                        if row[0].strip() == name:
                            deleted = True
                            continue 
                        rows.append(row)
                        
            if deleted:
                with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
                messagebox.showinfo("삭제 완료", f"'{name}' 상품이 삭제되었습니다.")
                view_items() 
                clear_entries()
            else:
                messagebox.showwarning("오류", f"'{name}' 상품을 찾을 수 없습니다.")
        except FileNotFoundError:
            pass

# --- 화면(UI) 그리기 ---
window = tk.Tk()
window.title("미니 ERP 시스템")
window.geometry("450x620")

tk.Label(window, text="상품명 (클릭하면 자동 입력됩니다):").pack(pady=2)
entry_name = tk.Entry(window)
entry_name.pack()

tk.Label(window, text="수량:").pack(pady=2)
entry_quantity = tk.Entry(window)
entry_quantity.pack()

tk.Label(window, text="가격(원):").pack(pady=2)
entry_price = tk.Entry(window)
entry_price.pack()

tk.Button(window, text="신규 상품 등록하기", command=add_item, bg="lightblue", width=20).pack(pady=10)

frame_buttons = tk.Frame(window)
frame_buttons.pack(pady=5)
tk.Button(frame_buttons, text="🔍 검색", command=search_item, width=8).pack(side="left", padx=2)
tk.Button(frame_buttons, text="🔄 전체보기", command=view_items, width=8).pack(side="left", padx=2)
tk.Button(frame_buttons, text="✏️ 수정", command=update_item, width=8, bg="#fff2cc").pack(side="left", padx=2)
tk.Button(frame_buttons, text="🗑️ 삭제", command=delete_item, width=8, bg="#ffcccc").pack(side="left", padx=2)

tk.Label(window, text="--- 등록된 상품 목록 ---").pack(pady=10)
listbox = tk.Listbox(window, width=55, height=12)
listbox.pack()

listbox.bind('<<ListboxSelect>>', on_select)

view_items()
window.mainloop()