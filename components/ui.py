import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datetime
import server.api as api  

class GiaoDienQuanLyBaiXe:
    def __init__(self, root, quan_ly_camera, quan_ly_xe, dau_doc_the):
        self.root = root
        
        # Thiết lập full screen
        self.root.state('zoomed')  # Windows
        # self.root.attributes('-zoomed', True)  # Linux nếu cần
        
        self.quan_ly_camera = quan_ly_camera
        self.quan_ly_xe = quan_ly_xe
        self.dau_doc_the = dau_doc_the

        # Biến khu vực
        self.danh_sach_khu = []
        self.khu_hien_tai = None

        # Các biến UI khác
        self.xe_hien_tai = None
        self.dang_quet = False
        self.che_do_hien_tai = "vao"
        self.loai_xe_hien_tai = "xe_may"
        self.anh_camera = None
        self.anh_chup_gan_day = None
        self.anh_xac_nhan_ra = None
        self.anh_bien_so = None

        self.tao_giao_dien()
        self.quan_ly_camera.dat_ui(self)
        self.quan_ly_xe.dat_ui(self)
        self.dau_doc_the.dat_ui(self)
        self.quan_ly_camera.bat_dau_camera()
        self.dau_doc_the.bat_dau_doc_the()
        self.cap_nhat_thoi_gian()
        self.tai_danh_sach_khu()

    def tao_giao_dien(self):
        khung_chinh = tk.Frame(self.root, bg="#f0f9ff")
        khung_chinh.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        khung_tieu_de = tk.Frame(khung_chinh, bg="#0f172a")
        khung_tieu_de.pack(fill=tk.X, pady=(0, 20))
        nhan_tieu_de = tk.Label(
            khung_tieu_de, text="HỆ THỐNG QUẢN LÝ BÃI GIỮ XE",
            font=("Helvetica", 24, "bold"), fg="white", bg="#0f172a", pady=15
        )
        nhan_tieu_de.pack()

        # --- Khung chọn khu ---
        khung_khu = tk.Frame(khung_chinh, bg="#f0f9ff")
        khung_khu.pack(fill=tk.X, padx=0, pady=(0, 10))
        tk.Label(khung_khu, text="Chọn khu:", font=("Helvetica", 11, "bold"), bg="#f0f9ff").pack(side=tk.LEFT)
        self.combo_khu = ttk.Combobox(khung_khu, state="readonly", font=("Helvetica", 11), width=15)
        self.combo_khu.pack(side=tk.LEFT, padx=8)
        self.combo_khu.bind("<<ComboboxSelected>>", self.khi_chon_khu)

        style = ttk.Style()
        style.configure("TNotebook", background="#f0f9ff", borderwidth=0)
        style.configure("TNotebook.Tab", background="#e0f2fe", foreground="#0f172a", padding=[15, 5], font=('Helvetica', 11, 'bold'))
        style.map("TNotebook.Tab", background=[("selected", "#0369a1")], foreground=[("selected", "white")])
        style.configure("TFrame", background="#f0f9ff")

        self.tab_control = ttk.Notebook(khung_chinh)
        self.tab_control.pack(fill=tk.BOTH, expand=True)
        self.tab_quan_ly = ttk.Frame(self.tab_control, style="TFrame")
        self.tab_control.add(self.tab_quan_ly, text="Quản Lý Xe Ra Vào")
        self.tab_danh_sach = ttk.Frame(self.tab_control, style="TFrame")
        self.tab_control.add(self.tab_danh_sach, text="Danh Sách Xe Trong Bãi")
        self.tao_tab_quan_ly()
        self.tao_tab_danh_sach()

        thanh_trang_thai = tk.Frame(khung_chinh, bg="#0f172a", height=30)
        thanh_trang_thai.pack(fill=tk.X, pady=(20, 0))
        thoi_gian_hien_tai = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.nhan_thoi_gian = tk.Label(
            thanh_trang_thai, text=f"Thời gian hiện tại: {thoi_gian_hien_tai}",
            font=("Helvetica", 10), fg="white", bg="#0f172a", pady=5
        )
        self.nhan_thoi_gian.pack(side=tk.RIGHT, padx=10)
        self.nhan_che_do = tk.Label(
            thanh_trang_thai, text="Chế độ: XE MÁY VÀO",
            font=("Helvetica", 10, "bold"), fg="white", bg="#0f172a", pady=5
        )
        self.nhan_che_do.pack(side=tk.LEFT, padx=10)
    
    def tao_tab_quan_ly(self):
        khung_noi_dung = tk.Frame(self.tab_quan_ly, bg="#f0f9ff")
        khung_noi_dung.pack(fill=tk.BOTH, expand=True)

        # Left panel - THIẾT LẬP CHIỀU RỘNG CỐ ĐỊNH
        bang_trai = tk.Frame(khung_noi_dung, bg="#f0f9ff", width=800)
        bang_trai.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        bang_trai.pack_propagate(False)  # QUAN TRỌNG: Ngăn thay đổi kích thước

        # Camera frames - THIẾT LẬP CHIỀU CAO CỐ ĐỊNH
        khung_cameras = tk.Frame(bang_trai, bg="#f0f9ff", height=300)
        khung_cameras.pack(fill=tk.X, pady=(0, 10))
        khung_cameras.pack_propagate(False)  # QUAN TRỌNG

        # Camera vào - THIẾT LẬP KÍCH THƯỚC CỐ ĐỊNH
        khung_camera_vao = tk.LabelFrame(
            khung_cameras, text="Camera Vào (...)", font=("Helvetica", 12, "bold"),
            bg="#f0f9ff", fg="#0369a1", padx=5, pady=5, relief=tk.GROOVE, bd=2,
            width=450, height=330
        )
        khung_camera_vao.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        khung_camera_vao.pack_propagate(False)  # QUAN TRỌNG
        
        self.khung_hien_thi_camera_vao = tk.Label(khung_camera_vao, bg="black", width=450, height=330)
        self.khung_hien_thi_camera_vao.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        anh_camera_vao = Image.new('RGB', (450, 330), color='#333333')
        self.anh_camera_vao = ImageTk.PhotoImage(anh_camera_vao)
        self.khung_hien_thi_camera_vao.config(image=self.anh_camera_vao)
        
        self.nhan_cong_vao = tk.Label(
            khung_camera_vao, text="Cổng vào: ...", font=("Helvetica", 10, "bold"), bg="#f0f9ff", fg="#0369a1"
        )
        self.nhan_cong_vao.pack(pady=(5, 0))

        # Camera ra - THIẾT LẬP KÍCH THƯỚC CỐ ĐỊNH
        khung_camera_ra = tk.LabelFrame(
            khung_cameras, text="Camera Ra (...)", font=("Helvetica", 12, "bold"),
            bg="#f0f9ff", fg="#0369a1", padx=5, pady=5, relief=tk.GROOVE, bd=2,
            width=450, height=330
        )
        khung_camera_ra.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        khung_camera_ra.pack_propagate(False)  # QUAN TRỌNG
        
        self.khung_hien_thi_camera_ra = tk.Label(khung_camera_ra, bg="black", width=450, height=330)
        self.khung_hien_thi_camera_ra.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        anh_camera_ra = Image.new('RGB', (450, 330), color='#333333')
        self.anh_camera_ra = ImageTk.PhotoImage(anh_camera_ra)
        self.khung_hien_thi_camera_ra.config(image=self.anh_camera_ra)
        
        self.nhan_cong_ra = tk.Label(
            khung_camera_ra, text="Cổng ra: ...", font=("Helvetica", 10, "bold"), bg="#f0f9ff", fg="#0369a1"
        )
        self.nhan_cong_ra.pack(pady=(5, 0))
        
        # Captures frame - THIẾT LẬP CHIỀU CAO CỐ ĐỊNH
        khung_anh_chup = tk.Frame(bang_trai, bg="#f0f9ff", height=330)  # Tăng từ 250 lên 330
        khung_anh_chup.pack(fill=tk.X, pady=(0, 10))
        khung_anh_chup.pack_propagate(False)  # QUAN TRỌNG

        # Ảnh vừa chụp - THIẾT LẬP KÍCH THƯỚC CỐ ĐỊNH
        khung_anh_gan_day = tk.LabelFrame(
            khung_anh_chup, 
            text="Ảnh Vừa Chụp", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f9ff", 
            fg="#0369a1",
            padx=5, 
            pady=5, 
            relief=tk.GROOVE,
            bd=2,
            width=450, height=330  # Tăng từ 400x330 lên 450x330
        )
        khung_anh_gan_day.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        khung_anh_gan_day.pack_propagate(False)  # QUAN TRỌNG
        
        self.khung_hien_thi_anh_gan_day = tk.Label(khung_anh_gan_day, bg="black", width=450, height=330)  # Tăng từ 400x330 lên 450x330
        self.khung_hien_thi_anh_gan_day.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        anh_trong = Image.new('RGB', (450, 330), color='#333333')  # Tăng từ 400x330 lên 450x330
        self.anh_chup_gan_day = ImageTk.PhotoImage(anh_trong)
        self.khung_hien_thi_anh_gan_day.config(image=self.anh_chup_gan_day)

        # Exit verify frame - THIẾT LẬP KÍCH THƯỚC CỐ ĐỊNH
        khung_xac_nhan_ra = tk.LabelFrame(
            khung_anh_chup, 
            text="Xác Nhận Xe Ra", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f9ff", 
            fg="#0369a1",
            padx=5, 
            pady=5, 
            relief=tk.GROOVE,
            bd=2,
            width=450, height=330  # Tăng từ 400x330 lên 450x330
        )
        khung_xac_nhan_ra.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        khung_xac_nhan_ra.pack_propagate(False)  # QUAN TRỌNG
        
        self.khung_hien_thi_xac_nhan_ra = tk.Label(khung_xac_nhan_ra, bg="black", width=450, height=330)  # Tăng từ 400x330 lên 450x330
        self.khung_hien_thi_xac_nhan_ra.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        self.anh_xac_nhan_ra = ImageTk.PhotoImage(anh_trong)
        self.khung_hien_thi_xac_nhan_ra.config(image=self.anh_xac_nhan_ra)

        # Plate frame - THIẾT LẬP CHIỀU CAO CỐ ĐỊNH
        khung_bien_so = tk.LabelFrame(
            bang_trai, 
            text="Biển Số Xe", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f9ff", 
            fg="#0369a1",
            padx=5, 
            pady=5, 
            relief=tk.GROOVE,
            bd=2,
            height=120 
        )
        khung_bien_so.pack(fill=tk.X, pady=(0, 10))
        khung_bien_so.pack_propagate(False)  # QUAN TRỌNG

        self.khung_hien_thi_bien_so = tk.Label(
            khung_bien_so, 
            text="", 
            font=("Helvetica", 16, "bold"), 
            bg="white", 
            fg="#0369a1",
            height=5,
            anchor="center"
        )
        self.khung_hien_thi_bien_so.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right panel
        bang_phai = tk.Frame(khung_noi_dung, bg="#f0f9ff", width=400)
        bang_phai.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Info frame
        khung_thong_tin = tk.LabelFrame(
            bang_phai, 
            text="Thông Tin Xe", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f9ff", 
            fg="#0369a1",
            padx=10, 
            pady=10, 
            relief=tk.GROOVE,
            bd=2
        )
        khung_thong_tin.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        khung_truong = tk.Frame(khung_thong_tin, bg="#f0f9ff")
        khung_truong.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Fields
        tk.Label(khung_truong, text="Biển số xe:", font=("Helvetica", 11, "bold"), bg="#f0f9ff", fg="#0f172a").grid(row=0, column=0, sticky="w", pady=5)
        self.nhan_bien_so = tk.Label(khung_truong, text="", font=("Helvetica", 11), bg="white", width=20, anchor="w", padx=5, relief=tk.SUNKEN, bd=1)
        self.nhan_bien_so.grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(khung_truong, text="Giờ vào:", font=("Helvetica", 11, "bold"), bg="#f0f9ff", fg="#0f172a").grid(row=1, column=0, sticky="w", pady=5)
        self.nhan_gio_vao = tk.Label(khung_truong, text="", font=("Helvetica", 11), bg="white", width=20, anchor="w", padx=5, relief=tk.SUNKEN, bd=1)
        self.nhan_gio_vao.grid(row=1, column=1, sticky="w", pady=5)
        
        tk.Label(khung_truong, text="Giờ ra:", font=("Helvetica", 11, "bold"), bg="#f0f9ff", fg="#0f172a").grid(row=2, column=0, sticky="w", pady=5)
        self.nhan_gio_ra = tk.Label(khung_truong, text="", font=("Helvetica", 11), bg="white", width=20, anchor="w", padx=5, relief=tk.SUNKEN, bd=1)
        self.nhan_gio_ra.grid(row=2, column=1, sticky="w", pady=5)
        
        tk.Label(khung_truong, text="Mã thẻ:", font=("Helvetica", 11, "bold"), bg="#f0f9ff", fg="#0f172a").grid(row=3, column=0, sticky="w", pady=5)
        self.nhan_ma_the = tk.Label(khung_truong, text="", font=("Helvetica", 11), bg="white", width=20, anchor="w", padx=5, relief=tk.SUNKEN, bd=1)
        self.nhan_ma_the.grid(row=3, column=1, sticky="w", pady=5)

        tk.Label(khung_truong, text="Thời gian đỗ:", font=("Helvetica", 11, "bold"), bg="#f0f9ff", fg="#0f172a").grid(row=4, column=0, sticky="w", pady=5)
        self.nhan_thoi_gian_do = tk.Label(khung_truong, text="", font=("Helvetica", 11), bg="white", width=20, anchor="w", padx=5, relief=tk.SUNKEN, bd=1)
        self.nhan_thoi_gian_do.grid(row=4, column=1, sticky="w", pady=5)
        
        tk.Label(khung_truong, text="Phí gửi xe:", font=("Helvetica", 11, "bold"), bg="#f0f9ff", fg="#0f172a").grid(row=5, column=0, sticky="w", pady=5)
        self.nhan_phi = tk.Label(khung_truong, text="", font=("Helvetica", 11, "bold"), bg="white", width=20, anchor="w", padx=5, relief=tk.SUNKEN, bd=1, fg="#0369a1")
        self.nhan_phi.grid(row=5, column=1, sticky="w", pady=5)
        
        # Thêm trường Chính sách giá
        tk.Label(khung_truong, text="Chính sách giá:", font=("Helvetica", 11, "bold"), bg="#f0f9ff", fg="#0f172a").grid(row=6, column=0, sticky="w", pady=5)
        self.nhan_chinh_sach = tk.Label(khung_truong, text="", font=("Helvetica", 11), bg="white", width=20, anchor="w", padx=5, relief=tk.SUNKEN, bd=1)
        self.nhan_chinh_sach.grid(row=6, column=1, sticky="w", pady=5)
        
        # Thêm trường Cổng vào
        tk.Label(khung_truong, text="Cổng vào:", font=("Helvetica", 11, "bold"), bg="#f0f9ff", fg="#0f172a").grid(row=7, column=0, sticky="w", pady=5)
        self.nhan_cong_vao_info = tk.Label(khung_truong, text="", font=("Helvetica", 11), bg="white", width=20, anchor="w", padx=5, relief=tk.SUNKEN, bd=1)
        self.nhan_cong_vao_info.grid(row=7, column=1, sticky="w", pady=5)
        
        # Thêm trường Cổng ra
        tk.Label(khung_truong, text="Cổng ra:", font=("Helvetica", 11, "bold"), bg="#f0f9ff", fg="#0f172a").grid(row=8, column=0, sticky="w", pady=5)
        self.nhan_cong_ra_info = tk.Label(khung_truong, text="", font=("Helvetica", 11), bg="white", width=20, anchor="w", padx=5, relief=tk.SUNKEN, bd=1)
        self.nhan_cong_ra_info.grid(row=8, column=1, sticky="w", pady=5)
        
        tk.Label(khung_truong, text="Trạng thái:", font=("Helvetica", 11, "bold"), bg="#f0f9ff", fg="#0f172a").grid(row=9, column=0, sticky="w", pady=5)
        self.nhan_trang_thai = tk.Label(khung_truong, text="", font=("Helvetica", 11), bg="white", width=20, anchor="w", padx=5, relief=tk.SUNKEN, bd=1)
        self.nhan_trang_thai.grid(row=9, column=1, sticky="w", pady=5)
        
        # Reader frame
        khung_dau_doc = tk.LabelFrame(
            bang_phai, 
            text="Đầu Đọc Thẻ", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f9ff", 
            fg="#0369a1",
            padx=10, 
            pady=10, 
            relief=tk.GROOVE,
            bd=2
        )
        khung_dau_doc.pack(fill=tk.X, pady=(0, 10))
        
        self.trang_thai_dau_doc = tk.Label(
            khung_dau_doc, 
            text="Đang chờ quẹt thẻ...", 
            font=("Helvetica", 12, "bold"), 
            fg="#0369a1", 
            bg="#e0f2fe",
            pady=10,
            relief=tk.RIDGE,
            bd=1
        )
        self.trang_thai_dau_doc.pack(fill=tk.X, padx=5, pady=5)
        
        # Mode selection buttons
        khung_che_do = tk.LabelFrame(
            bang_phai, 
            text="Chế Độ Hoạt Động", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f9ff", 
            fg="#0369a1",
            padx=10, 
            pady=10, 
            relief=tk.GROOVE,
            bd=2
        )
        khung_che_do.pack(fill=tk.X, pady=(0, 10))
        
        # Tạo frame cho hàng 1 và hàng 2 của các nút
        hang_che_do_1 = tk.Frame(khung_che_do, bg="#f0f9ff")
        hang_che_do_1.pack(fill=tk.X, pady=(5, 5))
        
        hang_che_do_2 = tk.Frame(khung_che_do, bg="#f0f9ff")
        hang_che_do_2.pack(fill=tk.X, pady=(5, 5))
        
        # Hàng 1: Xe máy vào/ra
        self.nut_xe_may_vao = tk.Button(
            hang_che_do_1, 
            text="Xe máy vào", 
            font=("Helvetica", 12, "bold"), 
            bg="#10b981", 
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            activebackground="#059669",
            activeforeground="white",
            command=self.dat_che_do_xe_may_vao
        )
        self.nut_xe_may_vao.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        self.nut_xe_may_ra = tk.Button(
            hang_che_do_1, 
            text="Xe máy ra", 
            font=("Helvetica", 12, "bold"), 
            bg="#3b82f6", 
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            activebackground="#2563eb",
            activeforeground="white",
            command=self.dat_che_do_xe_may_ra
        )
        self.nut_xe_may_ra.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # Hàng 2: Xe hơi vào/ra
        self.nut_oto_vao = tk.Button(
            hang_che_do_2, 
            text="Xe hơi vào", 
            font=("Helvetica", 12, "bold"),
            bg="#10b981", 
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            activebackground="#059669",
            activeforeground="white",
            command=self.dat_che_do_oto_vao
        )
        self.nut_oto_vao.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        self.nut_oto_ra = tk.Button(
            hang_che_do_2, 
            text="Xe hơi ra", 
            font=("Helvetica", 12, "bold"), 
            bg="#3b82f6", 
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            activebackground="#2563eb",
            activeforeground="white",
            command=self.dat_che_do_oto_ra
        )
        self.nut_oto_ra.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # Control buttons
        khung_nut = tk.LabelFrame(
            bang_phai, 
            text="Điều Khiển", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f9ff", 
            fg="#0369a1",
            padx=10, 
            pady=10, 
            relief=tk.GROOVE,
            bd=2
        )
        khung_nut.pack(fill=tk.X, pady=(0, 0))
        
        self.nut_xoa = tk.Button(
            khung_nut, 
            text="Xóa", 
            font=("Helvetica", 12, "bold"), 
            bg="#ef4444", 
            fg="white",
            padx=15,
            pady=8,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            activebackground="#dc2626",
            activeforeground="white",
            command=self.xoa_thong_tin
        )
        self.nut_xoa.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.nut_kiem_tra = tk.Button(
            khung_nut, 
            text="Kiểm tra biển số", 
            font=("Helvetica", 12, "bold"), 
            bg="#f59e0b", 
            fg="white",
            padx=15,
            pady=8,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            activebackground="#d97706",
            activeforeground="white",
            command=self.kiem_tra_bien_so
        )
        self.nut_kiem_tra.pack(side=tk.LEFT, padx=5, pady=5)

    def tao_tab_danh_sach(self):
        # Tạo frame chính cho tab danh sách
        khung_danh_sach = tk.Frame(self.tab_danh_sach, bg="#f0f9ff")
        khung_danh_sach.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tạo frame thống kê
        khung_thong_ke = tk.Frame(khung_danh_sach, bg="#f0f9ff")
        khung_thong_ke.pack(fill=tk.X, pady=(0, 15))
        
        # Các thẻ thống kê
        self.tao_the_thong_ke(khung_thong_ke, "Tổng số xe:", "0", 0)
        self.tao_the_thong_ke(khung_thong_ke, "Xe trong bãi:", "0", 1)
        self.tao_the_thong_ke(khung_thong_ke, "Tổng doanh thu:", "0 VND", 2)
        self.tao_the_thong_ke(khung_thong_ke, "Xe máy / Xe hơi:", "0 / 0", 3)
        
        # Tạo frame tìm kiếm và lọc
        khung_tim_kiem = tk.LabelFrame(
            khung_danh_sach, 
            text="Tìm Kiếm & Lọc", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f9ff", 
            fg="#0369a1",
            padx=10, 
            pady=10, 
            relief=tk.GROOVE,
            bd=2
        )
        khung_tim_kiem.pack(fill=tk.X, pady=(0, 15))
        
        # Ô tìm kiếm
        khung_tim_kiem_noi = tk.Frame(khung_tim_kiem, bg="#f0f9ff")
        khung_tim_kiem_noi.pack(fill=tk.X, pady=5)
        
        tk.Label(khung_tim_kiem_noi, text="Tìm kiếm:", font=("Helvetica", 11, "bold"), bg="#f0f9ff", fg="#0f172a").pack(side=tk.LEFT, padx=(0, 5))
        self.o_tim_kiem = tk.Entry(khung_tim_kiem_noi, width=30, font=("Helvetica", 11), relief=tk.SUNKEN, bd=2)
        self.o_tim_kiem.pack(side=tk.LEFT, padx=(0, 10))
        self.o_tim_kiem.bind("<KeyRelease>", self.tim_kiem_xe)
        
        # Lọc theo loại xe
        khung_loc_loai = tk.Frame(khung_tim_kiem, bg="#f0f9ff")
        khung_loc_loai.pack(fill=tk.X, pady=5)
        
        tk.Label(khung_loc_loai, text="Loại xe:", font=("Helvetica", 11, "bold"), bg="#f0f9ff", fg="#0f172a").pack(side=tk.LEFT, padx=(0, 5))
        self.loai_xe_var = tk.StringVar(value="tat_ca")
        
        # Tạo style cho Radiobutton
        style = ttk.Style()
        style.configure("TRadiobutton", background="#f0f9ff", font=("Helvetica", 11))
        
        ttk.Radiobutton(khung_loc_loai, text="Tất cả", variable=self.loai_xe_var, value="tat_ca", command=self.loc_danh_sach_xe, style="TRadiobutton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(khung_loc_loai, text="Xe máy", variable=self.loai_xe_var, value="xe_may", command=self.loc_danh_sach_xe, style="TRadiobutton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(khung_loc_loai, text="Xe hơi", variable=self.loai_xe_var, value="oto", command=self.loc_danh_sach_xe, style="TRadiobutton").pack(side=tk.LEFT, padx=(0, 10))
        
        # Lọc theo trạng thái
        khung_loc_trang_thai = tk.Frame(khung_tim_kiem, bg="#f0f9ff")
        khung_loc_trang_thai.pack(fill=tk.X, pady=5)
        
        tk.Label(khung_loc_trang_thai, text="Trạng thái:", font=("Helvetica", 11, "bold"), bg="#f0f9ff", fg="#0f172a").pack(side=tk.LEFT, padx=(0, 5))
        self.trang_thai_var = tk.StringVar(value="tat_ca")
        ttk.Radiobutton(khung_loc_trang_thai, text="Tất cả", variable=self.trang_thai_var, value="tat_ca", command=self.loc_danh_sach_xe, style="TRadiobutton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(khung_loc_trang_thai, text="Trong bãi", variable=self.trang_thai_var, value="trong_bai", command=self.loc_danh_sach_xe, style="TRadiobutton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(khung_loc_trang_thai, text="Đã ra", variable=self.trang_thai_var, value="da_ra", command=self.loc_danh_sach_xe, style="TRadiobutton").pack(side=tk.LEFT, padx=(0, 10))
        
        # Tạo frame danh sách xe
        khung_bang = tk.LabelFrame(
            khung_danh_sach, 
            text="Danh Sách Xe", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f9ff", 
            fg="#0369a1",
            padx=10, 
            pady=10, 
            relief=tk.GROOVE,
            bd=2
        )
        khung_bang.pack(fill=tk.BOTH, expand=True)
        
        # Tạo style cho Treeview
        style = ttk.Style()
        style.configure("Treeview", 
                        background="#ffffff", 
                        foreground="#333333", 
                        rowheight=25, 
                        fieldbackground="#ffffff",
                        font=("Helvetica", 10))
        style.configure("Treeview.Heading", 
                        font=("Helvetica", 11, "bold"), 
                        background="#e0f2fe", 
                        foreground="#0f172a")
        style.map("Treeview", background=[("selected", "#0369a1")], foreground=[("selected", "white")])
        
        # Tạo bảng danh sách xe
        columns = ("bien_so", "loai_xe", "gio_vao", "gio_ra", "ma_the", "thoi_gian_do", "phi", "cong_vao", "cong_ra", "trang_thai")
        self.bang_danh_sach_xe = ttk.Treeview(khung_bang, columns=columns, show="headings", height=15)
        
        # Định nghĩa tiêu đề
        self.bang_danh_sach_xe.heading("bien_so", text="Biển Số")
        self.bang_danh_sach_xe.heading("loai_xe", text="Loại Xe")
        self.bang_danh_sach_xe.heading("gio_vao", text="Giờ Vào")
        self.bang_danh_sach_xe.heading("gio_ra", text="Giờ Ra")
        self.bang_danh_sach_xe.heading("ma_the", text="Mã Thẻ")
        self.bang_danh_sach_xe.heading("thoi_gian_do", text="Thời Gian Đỗ")
        self.bang_danh_sach_xe.heading("phi", text="Phí")
        self.bang_danh_sach_xe.heading("cong_vao", text="Cổng Vào")
        self.bang_danh_sach_xe.heading("cong_ra", text="Cổng Ra")
        self.bang_danh_sach_xe.heading("trang_thai", text="Trạng Thái")
        
        # Định nghĩa cột
        self.bang_danh_sach_xe.column("bien_so", width=100)
        self.bang_danh_sach_xe.column("loai_xe", width=80)
        self.bang_danh_sach_xe.column("gio_vao", width=120)
        self.bang_danh_sach_xe.column("gio_ra", width=120)
        self.bang_danh_sach_xe.column("ma_the", width=80)
        self.bang_danh_sach_xe.column("thoi_gian_do", width=100)
        self.bang_danh_sach_xe.column("phi", width=100)
        self.bang_danh_sach_xe.column("cong_vao", width=80)
        self.bang_danh_sach_xe.column("cong_ra", width=80)
        self.bang_danh_sach_xe.column("trang_thai", width=80)
        
        # Thêm thanh cuộn
        thanh_cuon = ttk.Scrollbar(khung_bang, orient=tk.VERTICAL, command=self.bang_danh_sach_xe.yview)
        self.bang_danh_sach_xe.configure(yscroll=thanh_cuon.set)
        thanh_cuon.pack(side=tk.RIGHT, fill=tk.Y)
        self.bang_danh_sach_xe.pack(fill=tk.BOTH, expand=True)
        
        # Gắn sự kiện chọn
        self.bang_danh_sach_xe.bind("<<TreeviewSelect>>", self.khi_chon_xe)
    
    def tao_the_thong_ke(self, parent, tieu_de, gia_tri, cot):
        khung_the = tk.Frame(parent, bg="white", bd=2, relief=tk.RAISED)
        khung_the.grid(row=0, column=cot, padx=5, pady=5, sticky="nsew")
        
        nhan_tieu_de = tk.Label(
            khung_the, 
            text=tieu_de, 
            font=("Helvetica", 10, "bold"), 
            bg="#e0f2fe", 
            fg="#0f172a",
            width=15,
            pady=5
        )
        nhan_tieu_de.pack(fill=tk.X)
        
        nhan_gia_tri = tk.Label(
            khung_the, 
            text=gia_tri, 
            font=("Helvetica", 14, "bold"), 
            bg="white", 
            fg="#0369a1",
            pady=10
        )
        nhan_gia_tri.pack(fill=tk.X)
        
        # Lưu tham chiếu đến nhãn giá trị
        setattr(self, f"nhan_thong_ke_{cot}", nhan_gia_tri)
        
        # Đảm bảo các cột có kích thước bằng nhau
        parent.grid_columnconfigure(cot, weight=1)
    
    def cap_nhat_thoi_gian(self):
        """Cập nhật thời gian trên giao diện"""
        thoi_gian_hien_tai = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.nhan_thoi_gian.config(text=f"Thời gian hiện tại: {thoi_gian_hien_tai}")
        self.root.after(1000, self.cap_nhat_thoi_gian)
    
    def dat_lai_tat_ca_nut(self):
        """Reset trạng thái của tất cả các nút"""
        self.nut_xe_may_vao.config(bg="#3b82f6", relief=tk.RAISED)
        self.nut_xe_may_ra.config(bg="#3b82f6", relief=tk.RAISED)
        self.nut_oto_vao.config(bg="#3b82f6", relief=tk.RAISED)
        self.nut_oto_ra.config(bg="#3b82f6", relief=tk.RAISED)
    
    def dat_che_do_xe_may_vao(self):
        """Thiết lập chế độ xe máy vào"""
        self.che_do_hien_tai = "vao"
        self.loai_xe_hien_tai = "xe_may"
        self.dat_lai_tat_ca_nut()
        self.nut_xe_may_vao.config(bg="#10b981", relief=tk.SUNKEN)
        self.nhan_che_do.config(text="Chế độ: XE MÁY VÀO")
        self.xoa_thong_tin()
        self.dau_doc_the.dang_quet = False 
        self.quan_ly_camera.chuyen_doi_camera("vao")
    
    def dat_che_do_xe_may_ra(self):
        """Thiết lập chế độ xe máy ra"""
        self.che_do_hien_tai = "ra"
        self.loai_xe_hien_tai = "xe_may"
        self.dat_lai_tat_ca_nut()
        self.nut_xe_may_ra.config(bg="#10b981", relief=tk.SUNKEN)
        self.nhan_che_do.config(text="Chế độ: XE MÁY RA")
        self.xoa_thong_tin()
        self.dau_doc_the.dang_quet = False  
        self.quan_ly_camera.chuyen_doi_camera("ra")
    
    def dat_che_do_oto_vao(self):
        """Thiết lập chế độ xe hơi vào"""
        self.che_do_hien_tai = "vao"
        self.loai_xe_hien_tai = "oto"
        self.dat_lai_tat_ca_nut()
        self.nut_oto_vao.config(bg="#10b981", relief=tk.SUNKEN)
        self.nhan_che_do.config(text="Chế độ: XE HƠI VÀO")
        self.xoa_thong_tin()
        self.dau_doc_the.dang_quet = False 
        self.quan_ly_camera.chuyen_doi_camera("vao")
    
    def dat_che_do_oto_ra(self):
        """Thiết lập chế độ xe hơi ra"""
        self.che_do_hien_tai = "ra"
        self.loai_xe_hien_tai = "oto"
        self.dat_lai_tat_ca_nut()
        self.nut_oto_ra.config(bg="#10b981", relief=tk.SUNKEN)
        self.nhan_che_do.config(text="Chế độ: XE HƠI RA")
        self.xoa_thong_tin()
        self.dau_doc_the.dang_quet = False
        self.quan_ly_camera.chuyen_doi_camera("ra")
    
    def kiem_tra_bien_so(self):
        """Kiểm tra biển số xe"""
        if self.quan_ly_xe.xe_hien_tai:
            # Chụp ảnh mới để kiểm tra
            khung_chup, bien_so_phat_hien = self.quan_ly_camera.chup_anh()
            if khung_chup is not None:
                self.quan_ly_xe.kiem_tra_bien_so(bien_so_phat_hien)
        else:
            self.hien_thi_thong_bao("Thông báo", "Vui lòng chọn một xe từ danh sách để kiểm tra biển số.")
    
    def cap_nhat_khung_camera_vao(self, anh):
        """Cập nhật khung hình camera vào"""
        self.anh_camera_vao = ImageTk.PhotoImage(anh)
        self.khung_hien_thi_camera_vao.config(image=self.anh_camera_vao)

    def cap_nhat_khung_camera_ra(self, anh):
        """Cập nhật khung hình camera ra"""
        self.anh_camera_ra = ImageTk.PhotoImage(anh)
        self.khung_hien_thi_camera_ra.config(image=self.anh_camera_ra)
    
    def cap_nhat_anh_gan_day(self, duong_dan_anh):
        try:
            print(f"Đường dẫn ảnh gần đây: {duong_dan_anh}")  # Debug
            if not duong_dan_anh:
                print("Lỗi: Đường dẫn ảnh gần đây là None")
                return
            if not os.path.exists(duong_dan_anh):
                print(f"Lỗi: File ảnh không tồn tại tại {duong_dan_anh}")
                return
            img = Image.open(duong_dan_anh)
            img = img.resize((450, 330), Image.Resampling.LANCZOS)
            self.anh_chup_gan_day = ImageTk.PhotoImage(img)
            self.khung_hien_thi_anh_gan_day.config(image=self.anh_chup_gan_day)
            print("Đã cập nhật ảnh gần đây thành công")
        except Exception as e:
            print(f"Lỗi khi cập nhật ảnh gần đây: {e}")

    def cap_nhat_anh_xac_nhan_ra(self, duong_dan_anh):
        try:
            print(f"Đường dẫn ảnh xác nhận ra: {duong_dan_anh}")  # Debug
            if not duong_dan_anh:
                print("Lỗi: Đường dẫn ảnh xác nhận ra là None")
                return
            if not os.path.exists(duong_dan_anh):
                print(f"Lỗi: File ảnh không tồn tại tại {duong_dan_anh}")
                return
            img = Image.open(duong_dan_anh)
            img = img.resize((450, 330), Image.Resampling.LANCZOS)
            self.anh_xac_nhan_ra = ImageTk.PhotoImage(img)
            self.khung_hien_thi_xac_nhan_ra.config(image=self.anh_xac_nhan_ra)
            print("Đã cập nhật ảnh xác nhận ra thành công")
        except Exception as e:
            print(f"Lỗi khi cập nhật ảnh xác nhận ra: {e}")

    def cap_nhat_trang_thai_xe_ra(self, ma_the, bien_so, thanh_cong, msg=""):
        from tkinter import messagebox
        if thanh_cong:
            # Trạng thái thành công: cập nhật trạng thái, có thể log hoặc hiển thị popup
            self.cap_nhat_trang_thai_dau_doc(
                f"Xe ra thành công - Thẻ: {ma_the} - Biển số: {bien_so}", "#2ecc71"
            )
        else:
            # Trạng thái thất bại: cập nhật trạng thái, hiển thị lỗi
            self.cap_nhat_trang_thai_dau_doc(
                f"Lỗi xe ra [{ma_the}]: {msg}", "#e74c3c"
            )
            # Hiển thị popup lỗi cho người dùng
            if msg:
                messagebox.showerror("Lỗi xe ra", f"Thẻ: {ma_the}\n{msg}")
            else:
                messagebox.showerror("Lỗi xe ra", f"Thẻ: {ma_the}\nLỗi không xác định")

    def cap_nhat_trang_thai_xe_vao(self, ma_the, bien_so, thanh_cong, msg=""):
        from tkinter import messagebox
        if thanh_cong:
            # Trạng thái thành công
            self.cap_nhat_trang_thai_dau_doc(
                f"Xe vào thành công - Thẻ: {ma_the} - Biển số: {bien_so}", "#2ecc71"
            )
        else:
            # Trạng thái thất bại
            self.cap_nhat_trang_thai_dau_doc(
                f"Lỗi xe vào [{ma_the}]: {msg}", "#e74c3c"
            )
                # Hiển thị popup lỗi cho người dùng
            if msg:
                messagebox.showerror("Lỗi xe vào", f"Thẻ: {ma_the}\n{msg}")
            else:
                messagebox.showerror("Lỗi xe vào", f"Thẻ: {ma_the}\nLỗi không xác định")

    def cap_nhat_trang_thai_dau_doc(self, trang_thai, mau="#3498db"):
        """Cập nhật trạng thái đầu đọc thẻ"""
        self.trang_thai_dau_doc.config(text=trang_thai, fg=mau)
    
    def cap_nhat_anh_bien_so(self, anh):
        """Cập nhật khung hình biển số xe"""
        self.anh_bien_so = ImageTk.PhotoImage(anh)
        self.khung_hien_thi_bien_so.config(image=self.anh_bien_so)
    
    def cap_nhat_anh_xe(self, anh_vao, anh_ra=None):
        """Cập nhật hình ảnh xe vào và xe ra"""
        # Cập nhật hình ảnh vào
        if anh_vao is not None:
            self.cap_nhat_anh_xac_nhan_ra(anh_vao)
        
        # Cập nhật hình ảnh ra
        if anh_ra is not None:
            self.cap_nhat_anh_gan_day(anh_ra)
    
    def cap_nhat_thong_tin_xe(self, du_lieu_xe):
        """Cập nhật thông tin xe"""
        # Cập nhật nhãn thông tin
        self.nhan_bien_so.config(text=du_lieu_xe.get("bien_so", ""))
        self.nhan_gio_vao.config(text=du_lieu_xe.get("gio_vao", ""))
        self.nhan_gio_ra.config(text=du_lieu_xe.get("gio_ra", ""))
        self.nhan_ma_the.config(text=du_lieu_xe.get("ma_the", ""))
        self.nhan_thoi_gian_do.config(text=du_lieu_xe.get("thoi_gian_do", ""))
        self.nhan_phi.config(text=du_lieu_xe.get("phi", ""))
        
        # Cập nhật thông tin cổng vào/ra
        self.nhan_cong_vao_info.config(text=du_lieu_xe.get("cong_vao", "GATE_IN1"))
        self.nhan_cong_ra_info.config(text=du_lieu_xe.get("cong_ra", ""))
        
        # Cập nhật chính sách giá
        chinh_sach = du_lieu_xe.get("chinh_sach", "")
        if chinh_sach == "1":
            chinh_sach_hien_thi = "Xe máy - 4 giờ"
        elif chinh_sach == "2":
            chinh_sach_hien_thi = "Ô tô - 4 giờ"
        else:
            chinh_sach_hien_thi = chinh_sach
        self.nhan_chinh_sach.config(text=chinh_sach_hien_thi)
        
        # Hiển thị thông tin về phương pháp nhận diện biển số và trạng thái
        trang_thai = du_lieu_xe.get("trang_thai", "")
        
        # Thêm loại xe vào trạng thái để vẫn có thông tin
        loai_xe = du_lieu_xe.get("loai_xe", "")
        if loai_xe == "xe_may":
            trang_thai = "Xe máy - " + trang_thai
        elif loai_xe == "oto":
            trang_thai = "Xe hơi - " + trang_thai
        
        if du_lieu_xe.get("nhan_dien_boi_api", False):
            trang_thai += " (Biển số được nhận diện tự động)"
        if du_lieu_xe.get("da_xac_minh", False):
            trang_thai += " ✓ Biển số khớp"
        
        self.nhan_trang_thai.config(text=trang_thai)
    
    def cap_nhat_danh_sach_xe(self, du_lieu_xe, la_moi=False):
        """Cập nhật danh sách xe"""
        # Chuyển đổi loại xe sang chuỗi hiển thị
        loai_xe_hien_thi = "Xe máy" if du_lieu_xe["loai_xe"] == "xe_may" else "Xe hơi"
        
        # Lấy thông tin cổng vào/ra
        cong_vao = du_lieu_xe.get("cong_vao", "GATE_IN1")
        cong_ra = du_lieu_xe.get("cong_ra", "")
        
        if la_moi:
            # Thêm xe mới vào danh sách
            self.bang_danh_sach_xe.insert("", tk.END, values=(
                du_lieu_xe["bien_so"],
                loai_xe_hien_thi,
                du_lieu_xe["gio_vao"],
                du_lieu_xe.get("gio_ra", ""),
                du_lieu_xe["ma_the"],
                du_lieu_xe.get("thoi_gian_do", ""),
                du_lieu_xe.get("phi", ""),
                cong_vao,
                cong_ra,
                du_lieu_xe["trang_thai"]
            ))
        else:
            # Cập nhật thông tin xe hiện có
            for item in self.bang_danh_sach_xe.get_children():
                values = self.bang_danh_sach_xe.item(item, "values")
                if values[0] == du_lieu_xe["bien_so"] and values[4] == du_lieu_xe["ma_the"]:
                    self.bang_danh_sach_xe.item(item, values=(
                        du_lieu_xe["bien_so"],
                        loai_xe_hien_thi,
                        du_lieu_xe["gio_vao"],
                        du_lieu_xe.get("gio_ra", ""),
                        du_lieu_xe["ma_the"],
                        du_lieu_xe.get("thoi_gian_do", ""),
                        du_lieu_xe.get("phi", ""),
                        cong_vao,
                        cong_ra,
                        du_lieu_xe["trang_thai"]
                    ))
                    break
        
        # Cập nhật thống kê
        self.cap_nhat_thong_ke()
    
    def cap_nhat_thong_ke(self):
        """Cập nhật thống kê trên tab danh sách"""
        # Lấy danh sách xe từ quản lý xe
        danh_sach_xe = self.quan_ly_xe.xe
        
        # Tính toán các thống kê
        tong_so_xe = len(danh_sach_xe)
        xe_trong_bai = sum(1 for xe in danh_sach_xe if xe["trang_thai"] == "Trong bãi")
        xe_may_trong_bai = sum(1 for xe in danh_sach_xe if xe["trang_thai"] == "Trong bãi" and xe["loai_xe"] == "xe_may")
        oto_trong_bai = sum(1 for xe in danh_sach_xe if xe["trang_thai"] == "Trong bãi" and xe["loai_xe"] == "oto")
        
        # Tính tổng doanh thu
        tong_doanh_thu = 0
        for xe in danh_sach_xe:
            if xe["trang_thai"] == "Đã ra" and "phi" in xe:
                # Trích xuất số tiền từ chuỗi "X,XXX VND"
                try:
                    phi_text = xe["phi"].replace(",", "").replace("VND", "").strip()
                    phi = int(phi_text)
                    tong_doanh_thu += phi
                except (ValueError, AttributeError):
                    pass
        
        # Cập nhật các nhãn thống kê
        self.nhan_thong_ke_0.config(text=str(tong_so_xe))
        self.nhan_thong_ke_1.config(text=str(xe_trong_bai))
        self.nhan_thong_ke_2.config(text=f"{tong_doanh_thu:,} VND")
        self.nhan_thong_ke_3.config(text=f"{xe_may_trong_bai} / {oto_trong_bai}")
    
    def tim_kiem_xe(self, event=None):
        """Tìm kiếm xe theo biển số hoặc mã thẻ"""
        self.loc_danh_sach_xe()
    
    def loc_danh_sach_xe(self):
        """Lọc danh sách xe theo các tiêu chí"""
        # Lấy các giá trị lọc
        tu_khoa = self.o_tim_kiem.get().lower()
        loai_xe = self.loai_xe_var.get()
        trang_thai = self.trang_thai_var.get()
        
        # Xóa tất cả các mục hiện tại
        for item in self.bang_danh_sach_xe.get_children():
            self.bang_danh_sach_xe.delete(item)
        
        # Lọc và thêm lại các mục phù hợp
        for xe in self.quan_ly_xe.xe:
            # Kiểm tra từ khóa tìm kiếm
            bien_so = xe["bien_so"].lower()
            ma_the = xe["ma_the"].lower()
            if tu_khoa and tu_khoa not in bien_so and tu_khoa not in ma_the:
                continue
            
            # Kiểm tra loại xe
            if loai_xe != "tat_ca" and xe["loai_xe"] != loai_xe:
                continue
            
            # Kiểm tra trạng thái
            if trang_thai == "trong_bai" and xe["trang_thai"] != "Trong bãi":
                continue
            if trang_thai == "da_ra" and xe["trang_thai"] != "Đã ra":
                continue
            
            # Thêm xe vào danh sách
            loai_xe_hien_thi = "Xe máy" if xe["loai_xe"] == "xe_may" else "Xe hơi"
            cong_vao = xe.get("cong_vao", "GATE_IN1")
            cong_ra = xe.get("cong_ra", "")
            
            self.bang_danh_sach_xe.insert("", tk.END, values=(
                xe["bien_so"],
                loai_xe_hien_thi,
                xe["gio_vao"],
                xe.get("gio_ra", ""),
                xe["ma_the"],
                xe.get("thoi_gian_do", ""),
                xe.get("phi", ""),
                cong_vao,
                cong_ra,
                xe["trang_thai"]
            ))
    
    def xoa_thong_tin(self):
        """Xóa thông tin hiện tại"""
        # Xóa thông tin nhãn
        self.nhan_bien_so.config(text="")
        self.nhan_gio_vao.config(text="")
        self.nhan_gio_ra.config(text="")
        self.nhan_ma_the.config(text="")
        self.nhan_thoi_gian_do.config(text="")
        self.nhan_phi.config(text="")
        self.nhan_trang_thai.config(text="")
        self.nhan_cong_vao_info.config(text="")
        self.nhan_cong_ra_info.config(text="")
        self.nhan_chinh_sach.config(text="")
        
        # Xóa văn bản biển số
        self.khung_hien_thi_bien_so.config(text="")
        
        # Xóa hình ảnh
        anh_trong = Image.new('RGB', (450, 330), color='#333333')  # Tăng từ 320x240 lên 450x330
        self.anh_chup_gan_day = ImageTk.PhotoImage(anh_trong)
        self.khung_hien_thi_anh_gan_day.config(image=self.anh_chup_gan_day)
        
        self.anh_xac_nhan_ra = ImageTk.PhotoImage(anh_trong)
        self.khung_hien_thi_xac_nhan_ra.config(image=self.anh_xac_nhan_ra)
        
        # Đặt lại trạng thái đầu đọc thẻ
        self.trang_thai_dau_doc.config(text="Đang chờ quẹt thẻ...", fg="#0369a1")
    def khi_chon_xe(self, event):
        """Xử lý chọn xe từ danh sách"""
        selected_items = self.bang_danh_sach_xe.selection()
        if selected_items:
            item = selected_items[0]
            values = self.bang_danh_sach_xe.item(item, "values")
            # Thông báo cho quản lý xe
            self.quan_ly_xe.chon_xe(values[0], values[4])
            
            # Chuyển về tab quản lý
            self.tab_control.select(0)
    
    def hien_thi_thong_bao(self, tieu_de, thong_bao):
        """Hiển thị thông báo"""
        messagebox.showinfo(tieu_de, thong_bao)
    
    def hien_thi_loi(self, tieu_de, thong_bao):
        """Hiển thị lỗi"""
        messagebox.showerror(tieu_de, thong_bao)
    
    def khi_dong_cua_so(self):
        """Xử lý khi đóng cửa sổ"""
        # Dừng camera
        self.quan_ly_camera.dung_camera()
        # Dừng đọc thẻ
        self.dau_doc_the.dung_doc_the()
        # Đóng cửa sổ
        self.root.destroy()
        
    def tai_danh_sach_khu(self):
        try:
            ds = api.lay_danh_sach_khu()
            self.danh_sach_khu = ds if ds else []
            self.combo_khu['values'] = [khu['tenKhuVuc'] for khu in self.danh_sach_khu]
            if self.danh_sach_khu:
                self.combo_khu.current(0)
                self.khu_hien_tai = self.danh_sach_khu[0]
                self.cap_nhat_camera_cong_theo_khu(self.khu_hien_tai)
        except Exception as e:
            print("Lỗi lấy danh sách khu:", e)

    def khi_chon_khu(self, event=None):
        idx = self.combo_khu.current()
        if idx < 0 or idx >= len(self.danh_sach_khu):
            return
        self.khu_hien_tai = self.danh_sach_khu[idx]
        self.cap_nhat_camera_cong_theo_khu(self.khu_hien_tai)

    def cap_nhat_camera_cong_theo_khu(self, khu):
        # Cập nhật label cổng/camera vào/ra trên giao diện
        if khu['congVao'] and len(khu['congVao']) > 0:
            cong_vao = khu['congVao'][0]
            self.nhan_cong_vao.config(text=f"Cổng vào: {cong_vao['tenCong']} ({cong_vao['maCong']})")
        else:
            self.nhan_cong_vao.config(text="Cổng vào: ...")
        if khu['congRa'] and len(khu['congRa']) > 0:
            cong_ra = khu['congRa'][0]
            self.nhan_cong_ra.config(text=f"Cổng ra: {cong_ra['tenCong']} ({cong_ra['maCong']})")
        else:
            self.nhan_cong_ra.config(text="Cổng ra: ...")
        if khu['cameraVao'] and len(khu['cameraVao']) > 0:
            cam_vao = khu['cameraVao'][0]
            self.khung_hien_thi_camera_vao.master.config(
                text=f"Camera Vào ({cam_vao['maCamera']} - {cam_vao['viTriLapDat']})"
            )
        else:
            self.khung_hien_thi_camera_vao.master.config(text="Camera Vào (...)")
        if khu['cameraRa'] and len(khu['cameraRa']) > 0:
            cam_ra = khu['cameraRa'][0]
            self.khung_hien_thi_camera_ra.master.config(
                text=f"Camera Ra ({cam_ra['maCamera']} - {cam_ra['viTriLapDat']})"
            )
        else:
            self.khung_hien_thi_camera_ra.master.config(text="Camera Ra (...)")
    
    def hien_thi_anh_xe_vao_trong_xac_nhan_ra(self, anh_vao_url, bien_so_vao, ma_the):
        """Hiển thị chỉ ảnh xe vào trong khung Xác nhận xe ra"""
        try:
            # Load ảnh từ URL database
            anh_vao_pil = self.load_anh_tu_url(anh_vao_url)
            
            if anh_vao_pil:
                # Resize ảnh để phù hợp với khung hiện có
                anh_resize = anh_vao_pil.resize((360, 260), Image.Resampling.LANCZOS)
                self.photo_xe_vao = ImageTk.PhotoImage(anh_resize)
                
                # Hiển thị trực tiếp trong label hiện có
                self.khung_hien_thi_xac_nhan_ra.config(image=self.photo_xe_vao)
                self.khung_hien_thi_xac_nhan_ra.image = self.photo_xe_vao
                
                # Cập nhật title của khung
                parent_frame = self.khung_hien_thi_xac_nhan_ra.master
                if hasattr(parent_frame, 'config'):
                    parent_frame.config(text=f"Xe VÀO - Mã thẻ: {ma_the} - Biển số: {bien_so_vao}")
                
                print(f"Đã hiển thị ảnh xe vào cho thẻ {ma_the}")
                
            else:
                print(f"Không thể load ảnh từ URL: {anh_vao_url}")
                self.hien_thi_placeholder_anh_xe_vao_don_gian(bien_so_vao, ma_the)
                
        except Exception as e:
            print(f"Lỗi hiển thị ảnh xe vào: {e}")
            self.hien_thi_placeholder_anh_xe_vao_don_gian(bien_so_vao, ma_the)

    def hien_thi_placeholder_anh_xe_vao_don_gian(self, bien_so_vao, ma_the):
        """Hiển thị placeholder đơn giản khi không load được ảnh xe vào"""
        try:
            # Tạo ảnh text thay thế
            anh_placeholder = Image.new('RGB', (360, 280), color='#ffebee')
            
            # Thêm text lên ảnh (nếu có thư viện PIL.ImageDraw)
            try:
                from PIL import ImageDraw, ImageFont
                draw = ImageDraw.Draw(anh_placeholder)
                
                # Text thông tin
                text_lines = [
                    "Không thể tải ảnh xe vào",
                    f"Mã thẻ: {ma_the}",
                    f"Biển số: {bien_so_vao}"
                ]
                
                # Vẽ text
                y_offset = 80
                for line in text_lines:
                    bbox = draw.textbbox((0, 0), line)
                    text_width = bbox[2] - bbox[0]
                    x = (320 - text_width) // 2
                    draw.text((x, y_offset), line, fill='#c62828')
                    y_offset += 25
                    
            except ImportError:
                # Nếu không có ImageDraw, chỉ dùng màu nền
                pass
            
            # Hiển thị ảnh placeholder
            self.photo_xe_vao = ImageTk.PhotoImage(anh_placeholder)
            self.khung_hien_thi_xac_nhan_ra.config(image=self.photo_xe_vao)
            self.khung_hien_thi_xac_nhan_ra.image = self.photo_xe_vao
            
            # Cập nhật title
            parent_frame = self.khung_hien_thi_xac_nhan_ra.master
            if hasattr(parent_frame, 'config'):
                parent_frame.config(text=f"Xe VÀO - Mã thẻ: {ma_the} - Biển số: {bien_so_vao}")
                
        except Exception as e:
            print(f"Lỗi hiển thị placeholder: {e}")

    def khoi_phuc_khung_xac_nhan_ra_ban_dau(self):
        """Khôi phục khung xác nhận xe ra về trạng thái ban đầu"""
        try:
            # Tạo ảnh trống
            anh_trong = Image.new('RGB', (360, 280), color='#333333')
            self.anh_xac_nhan_ra = ImageTk.PhotoImage(anh_trong)
            self.khung_hien_thi_xac_nhan_ra.config(image=self.anh_xac_nhan_ra)
            
            # Khôi phục title gốc
            parent_frame = self.khung_hien_thi_xac_nhan_ra.master
            if hasattr(parent_frame, 'config'):
                parent_frame.config(text="Xác Nhận Xe Ra")
                
        except Exception as e:
            print(f"Lỗi khôi phục khung: {e}")
            """Ẩn thông tin xe vào khi không cần thiết"""
            if hasattr(self, 'frame_anh_container'):
                # Reset về trạng thái ban đầu
                try:
                    self.frame_anh_container.pack_forget()
                    
                    # Khôi phục label gốc
                    anh_trong = Image.new('RGB', (380, 260), color='#333333')
                    self.anh_xac_nhan_ra = ImageTk.PhotoImage(anh_trong)
                    self.khung_hien_thi_xac_nhan_ra.config(image=self.anh_xac_nhan_ra)
                    
                except Exception as e:
                    print(f"Lỗi ẩn thông tin xe vào: {e}")
        
    def load_anh_tu_url(self, url_path):
        """Load ảnh từ URL database"""
        try:
            import os
            
            if not url_path:
                return None
            
            print(f"🔍 DEBUG: Đường dẫn ảnh nhận được: '{url_path}'")
            
            # Convert URL "server/images\file.jpg" thành đường dẫn thực tế
            if url_path.startswith("server/"):
                # Chuẩn hóa đường dẫn - thay thế cả \ và /
                local_path = url_path.replace("\\", "/").replace("//", "/")
                
                # Tạo full path
                current_dir = os.getcwd()
                full_path = os.path.join(current_dir, local_path)
                full_path = os.path.normpath(full_path)
                
                print(f"🔍 DEBUG: Đường dẫn đầy đủ: '{full_path}'")
                
                # Kiểm tra file tồn tại
                if os.path.exists(full_path):
                    print(f"✅ File tồn tại, đang load ảnh...")
                    image = Image.open(full_path)
                    print(f"✅ Load ảnh thành công, kích thước: {image.size}")
                    return image
                else:
                    print(f"❌ File không tồn tại: {full_path}")
                    # Thử tìm trong thư mục gốc
                    filename = os.path.basename(url_path)
                    alt_path = os.path.join(current_dir, "server", "images", filename)
                    print(f"🔍 Thử đường dẫn thay thế: {alt_path}")
                    
                    if os.path.exists(alt_path):
                        print(f"✅ Tìm thấy file tại đường dẫn thay thế")
                        image = Image.open(alt_path)
                        return image
                    else:
                        print(f"❌ Không tìm thấy file ở đường dẫn thay thế")
                        return None
            else:
                # Đường dẫn tuyệt đối
                print(f"🔍 Đường dẫn tuyệt đối: {url_path}")
                if os.path.exists(url_path):
                    image = Image.open(url_path)
                    return image
                else:
                    print(f"❌ Đường dẫn tuyệt đối không tồn tại")
                    return None
                    
        except Exception as e:
            print(f"❌ Lỗi load ảnh từ URL {url_path}: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        return None