import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

class BienSoLoiDialog:
    def __init__(self, parent, ma_the, bien_so_cu, bien_so_moi, anh_xe_ra=None, anh_vao_url=None):
        self.parent = parent
        self.ma_the = ma_the
        self.bien_so_cu = bien_so_cu
        self.bien_so_moi = bien_so_moi
        self.anh_xe_ra = anh_xe_ra
        self.anh_vao_url = anh_vao_url  # URL từ database
        self.ket_qua = None
        self.bien_so_thuc = None
        
        self.tao_dialog()
    
    def load_anh_tu_url(self, url_path):
        """Convert URL database thành ảnh PIL"""
        try:
            if not url_path:
                return None
            
            # Convert URL "server/images/file.jpg" thành đường dẫn thực tế
            if url_path.startswith("server/"):
                # Giả sử project root là thư mục hiện tại
                local_path = url_path.replace("server/", "server/")
                local_path = local_path.replace("\\", "/")  # Chuẩn hóa separator
                
                # Tạo full path
                current_dir = os.getcwd()
                full_path = os.path.join(current_dir, local_path)
                
                # Kiểm tra file tồn tại
                if os.path.exists(full_path):
                    image = Image.open(full_path)
                    return image
                else:
                    print(f"File không tồn tại: {full_path}")
                    return None
            else:
                # Nếu là đường dẫn tuyệt đối
                if os.path.exists(url_path):
                    image = Image.open(url_path)
                    return image
                    
        except Exception as e:
            print(f"Lỗi load ảnh từ URL {url_path}: {e}")
            return None
        
        return None
    
    def tao_dialog(self):
        # Tạo cửa sổ dialog với kích thước lớn hơn để chứa 2 ảnh
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Lỗi Biển Số Không Trùng Khớp")
        self.dialog.geometry("800x700")  # Tăng kích thước
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        self.dialog.protocol("WM_DELETE_WINDOW", self.dong_dialog)
        
        # Center dialog
        self.dialog.transient(self.parent)
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (700 // 2)
        self.dialog.geometry(f"800x700+{x}+{y}")
        
        # Frame chính với scrollbar
        canvas = tk.Canvas(self.dialog, bg="#f0f9ff")
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f9ff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        main_frame = scrollable_frame
        
        # Tiêu đề
        title_label = tk.Label(
            main_frame, 
            text="⚠️ CẢNH BÁO: BIỂN SỐ KHÔNG TRÙNG KHỚP", 
            font=("Helvetica", 16, "bold"), 
            fg="#dc2626", 
            bg="#f0f9ff"
        )
        title_label.pack(pady=(0, 20))
        
        # Thông tin thẻ
        info_frame = tk.LabelFrame(
            main_frame, 
            text="Thông Tin Thẻ", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f9ff", 
            fg="#0369a1"
        )
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(info_frame, text=f"Mã thẻ: {self.ma_the}", 
                font=("Helvetica", 11, "bold"), bg="#f0f9ff").pack(pady=5)
        
        # **THÊM MỚI: Frame hiển thị 2 ảnh so sánh**
        self.hien_thi_anh_so_sanh(main_frame)
        
        # So sánh biển số
        compare_frame = tk.LabelFrame(
            main_frame, 
            text="So Sánh Biển Số", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f9ff", 
            fg="#0369a1"
        )
        compare_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Layout 2 cột cho biển số
        cols_frame = tk.Frame(compare_frame, bg="#f0f9ff")
        cols_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Cột trái - Biển số vào
        left_col = tk.Frame(cols_frame, bg="#f0f9ff")
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(left_col, text="Biển số khi VÀO:", 
                font=("Helvetica", 11, "bold"), bg="#f0f9ff").pack()
        bien_so_vao_label = tk.Label(
            left_col, 
            text=self.bien_so_cu, 
            font=("Helvetica", 14, "bold"), 
            bg="#10b981", 
            fg="white", 
            padx=10, 
            pady=5
        )
        bien_so_vao_label.pack(pady=(5, 0))
        
        # Cột phải - Biển số ra
        right_col = tk.Frame(cols_frame, bg="#f0f9ff")
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(right_col, text="Biển số nhận diện khi RA:", 
                font=("Helvetica", 11, "bold"), bg="#f0f9ff").pack()
        bien_so_ra_label = tk.Label(
            right_col, 
            text=self.bien_so_moi, 
            font=("Helvetica", 14, "bold"), 
            bg="#dc2626", 
            fg="white", 
            padx=10, 
            pady=5
        )
        bien_so_ra_label.pack(pady=(5, 0))
        
        # Frame nhập biển số thủ công
        manual_frame = tk.LabelFrame(
            main_frame, 
            text="Nhập Biển Số Thủ Công", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f9ff", 
            fg="#0369a1"
        )
        manual_frame.pack(fill=tk.X, pady=(0, 15))
        
        input_frame = tk.Frame(manual_frame, bg="#f0f9ff")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(input_frame, text="Biển số thực tế:", 
                font=("Helvetica", 11, "bold"), bg="#f0f9ff").pack(side=tk.LEFT)
        
        self.bien_so_entry = tk.Entry(
            input_frame, 
            font=("Helvetica", 12), 
            width=15,
            relief=tk.SUNKEN,
            bd=2
        )
        self.bien_so_entry.pack(side=tk.LEFT, padx=(10, 0))
        self.bien_so_entry.insert(0, self.bien_so_cu)
        self.bien_so_entry.focus()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg="#f0f9ff")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Các nút như cũ...
        self.tao_cac_nut(button_frame)
        
        # Bind Enter key
        self.bien_so_entry.bind("<Return>", lambda e: self.xac_nhan_bien_so())
    
    def hien_thi_anh_so_sanh(self, parent):
        """Hiển thị 2 ảnh so sánh: vào và ra"""
        images_frame = tk.LabelFrame(
            parent, 
            text="So Sánh Ảnh Xe", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f9ff", 
            fg="#0369a1"
        )
        images_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Container cho 2 ảnh
        container = tk.Frame(images_frame, bg="#f0f9ff")
        container.pack(fill=tk.X, padx=10, pady=10)
        
        # Ảnh vào (trái)
        left_frame = tk.Frame(container, bg="#f0f9ff", relief=tk.SUNKEN, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(left_frame, text="Ảnh khi VÀO", 
                font=("Helvetica", 11, "bold"), bg="#10b981", fg="white").pack(fill=tk.X)
        
        # Load và hiển thị ảnh vào
        anh_vao = self.load_anh_tu_url(self.anh_vao_url)
        if anh_vao:
            try:
                resized_vao = anh_vao.resize((250, 180), Image.Resampling.LANCZOS)
                photo_vao = ImageTk.PhotoImage(resized_vao)
                
                label_vao = tk.Label(left_frame, image=photo_vao, bg="#f0f9ff")
                label_vao.image = photo_vao  # Keep reference
                label_vao.pack(pady=5)
            except Exception as e:
                print(f"Lỗi hiển thị ảnh vào: {e}")
                tk.Label(left_frame, text="Không thể tải ảnh vào", 
                        bg="#f0f9ff", fg="#dc2626").pack(pady=20)
        else:
            tk.Label(left_frame, text="Không có ảnh vào", 
                    bg="#f0f9ff", fg="#6b7280").pack(pady=20)
        
        # Ảnh ra (phải)
        right_frame = tk.Frame(container, bg="#f0f9ff", relief=tk.SUNKEN, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(right_frame, text="Ảnh khi RA", 
                font=("Helvetica", 11, "bold"), bg="#dc2626", fg="white").pack(fill=tk.X)
        
        # Hiển thị ảnh ra
        if self.anh_xe_ra:
            try:
                if hasattr(self.anh_xe_ra, 'resize'):
                    resized_ra = self.anh_xe_ra.resize((250, 180), Image.Resampling.LANCZOS)
                else:
                    resized_ra = self.anh_xe_ra
                
                photo_ra = ImageTk.PhotoImage(resized_ra)
                
                label_ra = tk.Label(right_frame, image=photo_ra, bg="#f0f9ff")
                label_ra.image = photo_ra  # Keep reference
                label_ra.pack(pady=5)
            except Exception as e:
                print(f"Lỗi hiển thị ảnh ra: {e}")
                tk.Label(right_frame, text="Không thể tải ảnh ra", 
                        bg="#f0f9ff", fg="#dc2626").pack(pady=20)
        else:
            tk.Label(right_frame, text="Không có ảnh ra", 
                    bg="#f0f9ff", fg="#6b7280").pack(pady=20)
    
    def tao_cac_nut(self, button_frame):
        """Tạo các nút điều khiển"""
        # Nút Quét lại
        self.btn_quet_lai = tk.Button(
            button_frame,
            text="🔄 Quét Lại",
            font=("Helvetica", 12, "bold"),
            bg="#f59e0b",
            fg="white",
            padx=20,
            pady=8,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=self.quet_lai
        )
        self.btn_quet_lai.pack(side=tk.LEFT, padx=(0, 10))
        
        # Nút Xác nhận biển số thủ công
        self.btn_xac_nhan = tk.Button(
            button_frame,
            text="✅ Xác Nhận",
            font=("Helvetica", 12, "bold"),
            bg="#10b981",
            fg="white",
            padx=20,
            pady=8,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=self.xac_nhan_bien_so
        )
        self.btn_xac_nhan.pack(side=tk.LEFT, padx=(0, 10))
        
        # Nút Hủy
        self.btn_huy = tk.Button(
            button_frame,
            text="❌ Hủy",
            font=("Helvetica", 12, "bold"),
            bg="#ef4444",
            fg="white",
            padx=20,
            pady=8,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=self.dong_dialog
        )
        self.btn_huy.pack(side=tk.RIGHT)
    
    # Các phương thức khác giữ nguyên...
    def quet_lai(self):
        self.ket_qua = "quet_lai"
        self.dialog.destroy()
    
    def xac_nhan_bien_so(self):
        bien_so_nhap = self.bien_so_entry.get().strip().upper()
        
        if not bien_so_nhap:
            messagebox.showerror("Lỗi", "Vui lòng nhập biển số!")
            return
        
        if len(bien_so_nhap) < 6:
            if not messagebox.askyesno("Xác nhận", 
                                     f"Biển số '{bien_so_nhap}' có vẻ ngắn. Bạn có chắc chắn không?"):
                return
        
        self.ket_qua = "xac_nhan"
        self.bien_so_thuc = bien_so_nhap
        self.dialog.destroy()
    
    def dong_dialog(self):
        self.ket_qua = "huy"
        self.dialog.destroy()
    
    def hien_thi(self):
        self.dialog.wait_window()
        return self.ket_qua, self.bien_so_thuc