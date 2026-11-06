import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont

# ================== CẤU HÌNH MÀU SẮC & FONT ==================
BG_MAIN = "#FFF3E0"       # Nền chính (Cam rất nhạt)
BG_FRAME = "#FFE0B2"      # Nền khung (Cam nhạt)
TEXT_COLOR = "#4E342E"    # Chữ (Nâu đậm)
BTN_COLOR = "#E65100"     # Nút bấm (Cam đậm)
BTN_HOVER = "#BF360C"     # Nút bấm khi di chuột (Cam sậm)
TEXT_BTN = "#FFFFFF"      # Chữ trên nút (Trắng)

# ================== XỬ LÝ ĐIỂM ==================
def he10_sang_he4(diem):
    if 9.0 <= diem <= 10:
        return 4.0
    elif 8.5 <= diem < 9.0:
        return 3.7
    elif 8.0 <= diem < 8.5:
        return 3.5
    elif 7.0 <= diem < 8.0:
        return 3.0
    elif 6.5 <= diem < 7.0:
        return 2.5
    elif 5.5 <= diem < 6.5:
        return 2.0
    elif 5.0 <= diem < 5.5:
        return 1.5
    elif 4.0 <= diem < 5.0:
        return 1.0
    else:
        return 0.0  # Dưới 4.0 là F (0 điểm)

# ================== DỮ LIỆU ==================
ds_mon = []   # Lưu danh sách môn mới: (điểm, tín chỉ)
editing_index = None  # Biến lưu vị trí môn đang được chọn để sửa

# ================== CẬP NHẬT THÔNG TIN TÍN CHỈ REALTIME ==================
def cap_nhat_hien_thi_tin_chi(event=None):
    try:
        tc_hientai = int(entry_tc_hientai.get() or 0)
    except ValueError:
        tc_hientai = 0
    
    tc_moi = sum(tc for _, tc in ds_mon)
    tong_tc = tc_hientai + tc_moi
    lbl_tong_tinchi_live.config(text=f"📌 Tổng tín chỉ: {tong_tc} (Cũ: {tc_hientai} | Mới: {tc_moi})")

# ================== SỰ KIỆN ==================
def focus_tinchi(event):
    entry_tinchi.focus()

def enter_tinchi(event):
    them_mon()

def chon_mon_de_sua(event):
    global editing_index
    selection = listbox.curselection()
    if not selection:
        return
    
    editing_index = selection[0]
    diem, tinchi = ds_mon[editing_index]
    
    # Đưa dữ liệu lên ô nhập
    entry_diem.delete(0, tk.END)
    entry_diem.insert(0, str(diem))
    
    entry_tinchi.delete(0, tk.END)
    entry_tinchi.insert(0, str(tinchi))
    
    btn_them.config(text="Cập Nhật Môn")
    entry_diem.focus()

def them_mon():
    global editing_index
    try:
        diem = float(entry_diem.get())
        tinchi = int(entry_tinchi.get())
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho điểm và tín chỉ!")
        return

    if not (0 <= diem <= 10) or tinchi <= 0:
        messagebox.showerror("Lỗi", "Điểm (0-10) hoặc tín chỉ (>0) không hợp lệ!")
        return

    if editing_index is not None:
        ds_mon[editing_index] = (diem, tinchi)
        listbox.delete(editing_index)
        listbox.insert(editing_index, f"  Điểm 10: {diem:<4} | Tín chỉ: {tinchi}")
        editing_index = None
        btn_them.config(text="Thêm Môn")
    else:
        ds_mon.append((diem, tinchi))
        listbox.insert(tk.END, f"  Điểm 10: {diem:<4} | Tín chỉ: {tinchi}")

    entry_diem.delete(0, tk.END)
    entry_tinchi.delete(0, tk.END)
    entry_diem.focus()
    
    cap_nhat_hien_thi_tin_chi()

def xoa_mon():
    global editing_index
    try:
        index = listbox.curselection()[0]
    except IndexError:
        messagebox.showwarning("Nhắc nhở", "Vui lòng chọn môn cần xóa trong danh sách!")
        return

    listbox.delete(index)
    ds_mon.pop(index)
    
    editing_index = None
    btn_them.config(text="Thêm Môn")
    entry_diem.delete(0, tk.END)
    entry_tinchi.delete(0, tk.END)
    entry_diem.focus()
    
    cap_nhat_hien_thi_tin_chi()

def tinh_ket_qua():
    try:
        tc_hientai = int(entry_tc_hientai.get() or 0)
        diem10_hientai = float(entry_diem10_hientai.get() or 0)
        diem4_hientai = float(entry_diem4_hientai.get() or 0)
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số cho thông tin tích lũy!")
        return

    tc_moi = sum(tc for _, tc in ds_mon)
    tong_tinchi = tc_hientai + tc_moi

    if tong_tinchi == 0:
        messagebox.showwarning("Kết quả", "Chưa có dữ liệu tín chỉ để tính toán!")
        return

    tong_diem10 = diem10_hientai * tc_hientai
    tong_diem4 = diem4_hientai * tc_hientai
    so_mon_rot = 0

    for diem, tinchi in ds_mon:
        he4 = he10_sang_he4(diem)
        if he4 == 0.0:
            so_mon_rot += 1
            
        tong_diem10 += diem * tinchi
        tong_diem4 += he4 * tinchi

    tb10 = tong_diem10 / tong_tinchi
    tb4 = tong_diem4 / tong_tinchi

    lbl_ketqua.config(
        text=f"📊 KẾT QUẢ TỔNG KẾT\n"
             f"• Tổng tín chỉ: {tong_tinchi} (Cũ: {tc_hientai} | Mới: {tc_moi})\n"
             f"• Số môn rớt (mới): {so_mon_rot}\n"
             f"• Điểm TB Hệ 10 mới: {tb10:.2f}\n"
             f"• Điểm TB Hệ 4 mới  : {tb4:.2f}",
        fg="#D84315"
    )

def on_enter(e):
    e.widget['background'] = BTN_HOVER
def on_leave(e):
    e.widget['background'] = BTN_COLOR

# ================== GIAO DIỆN (UI) ==================
root = tk.Tk()
root.title("GPA Calculator")
root.geometry("620x450") # Chiều rộng 620px, Chiều cao 450px gọn gàng
root.configure(bg=BG_MAIN)
root.resizable(False, False)

font_title = tkFont.Font(family="Helvetica", size=11, weight="bold")
font_label = tkFont.Font(family="Helvetica", size=9, weight="bold")
font_entry = tkFont.Font(family="Helvetica", size=10)

# Tiêu đề chính
tk.Label(root, text="🎓 TÍNH ĐIỂM TRUNG BÌNH TÍCH LŨY", font=tkFont.Font(family="Helvetica", size=13, weight="bold"), bg=BG_MAIN, fg=BTN_COLOR).pack(pady=8)

# Bố cục chính: Cột trái (Danh sách) - Cột phải (Nhập liệu & Kết quả)
frame_body = tk.Frame(root, bg=BG_MAIN)
frame_body.pack(fill="both", expand=True, padx=15, pady=5)

# ================== CỘT TRÁI ==================
frame_left = tk.Frame(frame_body, bg=BG_MAIN)
frame_left.pack(side="left", fill="both", expand=True, padx=(0, 10))

lbl_list_title = tk.Label(frame_left, text="📋 Danh sách môn mới", bg=BG_MAIN, fg=TEXT_COLOR, font=font_title)
lbl_list_title.pack(anchor="w")

# Khung danh sách chứa Scrollbar
frame_listbox = tk.Frame(frame_left, bg=BG_MAIN)
frame_listbox.pack(fill="both", expand=True, pady=5)

scrollbar = tk.Scrollbar(frame_listbox)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(frame_listbox, font=("Consolas", 10), relief="solid", bd=1, highlightthickness=0, yscrollcommand=scrollbar.set)
listbox.pack(side="left", fill="both", expand=True)
scrollbar.config(command=listbox.yview)
listbox.bind("<<ListboxSelect>>", chon_mon_de_sua)

lbl_tong_tinchi_live = tk.Label(frame_left, text="📌 Tổng tín chỉ: 0 (Cũ: 0 | Mới: 0)", font=font_label, bg=BG_MAIN, fg="#BF360C")
lbl_tong_tinchi_live.pack(anchor="w", pady=3)

frame_left_btns = tk.Frame(frame_left, bg=BG_MAIN)
frame_left_btns.pack(fill="x", pady=5)

btn_xoa = tk.Button(frame_left_btns, text="Xóa Môn Chọn", bg="#6D4C41", fg=TEXT_BTN, font=font_label, relief="flat", cursor="hand2", command=xoa_mon)
btn_xoa.pack(side="left", fill="x", expand=True, padx=(0, 2))

btn_tinh = tk.Button(frame_left_btns, text="TÍNH KẾT QUẢ", bg=BTN_COLOR, fg=TEXT_BTN, font=font_label, relief="flat", cursor="hand2", command=tinh_ket_qua)
btn_tinh.pack(side="right", fill="x", expand=True, padx=(2, 0))
btn_tinh.bind("<Enter>", on_enter)
btn_tinh.bind("<Leave>", on_leave)

# ================== CỘT PHẢI ==================
frame_right = tk.Frame(frame_body, bg=BG_MAIN)
frame_right.pack(side="right", fill="both", padx=(5, 0))

# Khung 1: Tích lũy hiện tại
frame_hientai = tk.LabelFrame(frame_right, text=" Thông tin tích lũy hiện tại ", bg=BG_FRAME, fg=TEXT_COLOR, font=font_title, padx=10, pady=5)
frame_hientai.pack(fill="x", pady=(0, 5))

tk.Label(frame_hientai, text="Tín chỉ tích lũy:", bg=BG_FRAME, fg=TEXT_COLOR, font=font_label).grid(row=0, column=0, sticky="w", pady=2)
entry_tc_hientai = tk.Entry(frame_hientai, font=font_entry, width=12, justify="center")
entry_tc_hientai.grid(row=0, column=1, pady=2, padx=5)
entry_tc_hientai.bind("<KeyRelease>", cap_nhat_hien_thi_tin_chi)
entry_tc_hientai.bind("<Return>", lambda e: entry_diem10_hientai.focus())

tk.Label(frame_hientai, text="Điểm hệ 10 hiện tại:", bg=BG_FRAME, fg=TEXT_COLOR, font=font_label).grid(row=1, column=0, sticky="w", pady=2)
entry_diem10_hientai = tk.Entry(frame_hientai, font=font_entry, width=12, justify="center")
entry_diem10_hientai.grid(row=1, column=1, pady=2, padx=5)
entry_diem10_hientai.bind("<Return>", lambda e: entry_diem4_hientai.focus())

tk.Label(frame_hientai, text="Điểm hệ 4 hiện tại:", bg=BG_FRAME, fg=TEXT_COLOR, font=font_label).grid(row=2, column=0, sticky="w", pady=2)
entry_diem4_hientai = tk.Entry(frame_hientai, font=font_entry, width=12, justify="center")
entry_diem4_hientai.grid(row=2, column=1, pady=2, padx=5)
entry_diem4_hientai.bind("<Return>", lambda e: entry_diem.focus())

# Khung 2: Nhập môn học mới
frame_moi = tk.LabelFrame(frame_right, text=" Nhập môn học mới ", bg=BG_FRAME, fg=TEXT_COLOR, font=font_title, padx=10, pady=5)
frame_moi.pack(fill="x", pady=5)

tk.Label(frame_moi, text="Điểm hệ 10:", bg=BG_FRAME, fg=TEXT_COLOR, font=font_label).grid(row=0, column=0, sticky="w", pady=2)
entry_diem = tk.Entry(frame_moi, font=font_entry, width=12, justify="center")
entry_diem.grid(row=0, column=1, pady=2, padx=5)
entry_diem.bind("<Return>", focus_tinchi)

tk.Label(frame_moi, text="Số tín chỉ:", bg=BG_FRAME, fg=TEXT_COLOR, font=font_label).grid(row=1, column=0, sticky="w", pady=2)
entry_tinchi = tk.Entry(frame_moi, font=font_entry, width=12, justify="center")
entry_tinchi.grid(row=1, column=1, pady=2, padx=5)
entry_tinchi.bind("<Return>", enter_tinchi)

btn_them = tk.Button(frame_moi, text="Thêm Môn", bg=BTN_COLOR, fg=TEXT_BTN, font=font_label, relief="flat", cursor="hand2", command=them_mon)
btn_them.grid(row=2, column=0, columnspan=2, pady=5, sticky="we")
btn_them.bind("<Enter>", on_enter)
btn_them.bind("<Leave>", on_leave)

# Khung 3: Kết quả hiển thị
frame_ketqua = tk.Frame(frame_right, bg=BG_MAIN)
frame_ketqua.pack(fill="both", expand=True, pady=5)

lbl_ketqua = tk.Label(frame_ketqua, text="📊 KẾT QUẢ TỔNG KẾT\n(Chờ nhập dữ liệu...)", font=tkFont.Font(family="Helvetica", size=9, weight="bold"), bg=BG_MAIN, fg="#D84315", justify="left")
lbl_ketqua.pack(anchor="w")

entry_tc_hientai.focus()
root.mainloop()