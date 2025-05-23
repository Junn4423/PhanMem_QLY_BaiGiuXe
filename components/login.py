import tkinter as tk
from tkinter import simpledialog, messagebox, font

class EnhancedLoginDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.result = False
        self.username = None
        self.password = None
        # Gọi hàm tạo của lớp cha
        super().__init__(parent, title)
        
    # Ghi đè phương thức này để cấu hình cửa sổ sau khi nó đã tạo xong
    def _create_dialog(self):
        super()._create_dialog()
        self.resizable(False, False)
        window_width = 480
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
    def body(self, master):
        # Màu sắc
        bg_color = "#f0f4f8"
        accent_color = "#0f766e"
        text_color = "#0f172a"
        
        # Thiết lập frame chính với padding lớn hơn
        master.configure(bg=bg_color, padx=40, pady=30)
        
        # Thêm header
        header_frame = tk.Frame(master, bg=bg_color)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        header = tk.Label(header_frame, 
                         text="ĐĂNG NHẬP HỆ THỐNG", 
                         font=("Helvetica", 20, "bold"),
                         bg=bg_color, 
                         fg=accent_color)
        header.pack()
        
        subheader = tk.Label(header_frame, 
                            text="Vui lòng đăng nhập để tiếp tục",
                            font=("Helvetica", 11),
                            bg=bg_color, 
                            fg=text_color)
        subheader.pack(pady=(8, 0))
        
        # Logo hoặc icon 
        logo_frame = tk.Frame(master, bg=accent_color, width=80, height=80)
        logo_frame.grid(row=1, column=0, columnspan=2, pady=(0, 25))
        logo_frame.grid_propagate(False)
        
        logo_text = tk.Label(logo_frame, text="P", 
                            font=("Helvetica", 40, "bold"),
                            bg=accent_color, fg="white")
        logo_text.place(relx=0.5, rely=0.5, anchor="center")
        
        # Form đăng nhập với style đẹp và rộng hơn
        username_frame = tk.Frame(master, bg=bg_color, width=400)
        username_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        
        tk.Label(username_frame, text="Tài khoản:", 
                font=("Helvetica", 13, "bold"),
                bg=bg_color, fg=text_color, anchor="w").pack(fill="x", pady=(0, 5))
                
        self.username_entry = tk.Entry(username_frame, 
                                      font=("Helvetica", 13),
                                      relief="solid", bd=1,
                                      bg="white", fg=text_color)
        self.username_entry.pack(fill="x", ipady=10)
        
        password_frame = tk.Frame(master, bg=bg_color, width=400)
        password_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        tk.Label(password_frame, text="Mật khẩu:", 
                font=("Helvetica", 13, "bold"),
                bg=bg_color, fg=text_color, anchor="w").pack(fill="x", pady=(0, 5))
                
        self.password_entry = tk.Entry(password_frame, 
                                      font=("Helvetica", 13),
                                      show="•", relief="solid", bd=1,
                                      bg="white", fg=text_color)
        self.password_entry.pack(fill="x", ipady=10)
        
        # Thêm không gian rỗng để dialog rộng hơn
        spacer = tk.Frame(master, bg=bg_color, width=400, height=10)
        spacer.grid(row=4, column=0, columnspan=2)
        
        # Liên kết phím Enter
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", lambda e: self.ok())
        
        return self.username_entry  # Initial focus
    
    def buttonbox(self):
        # Ghi đè phương thức tạo nút để tạo nút đẹp hơn
        box = tk.Frame(self)
        box.pack(fill="x", expand=True, padx=40, pady=(0, 25))
        
        # Nút login với style đẹp và rộng hơn
        login_btn = tk.Button(box, text="ĐĂNG NHẬP",
                             command=self.ok,
                             font=("Helvetica", 14, "bold"),
                             bg="#0f766e", fg="white",
                             activebackground="#14b8a6",
                             activeforeground="white",
                             cursor="hand2",
                             relief="flat",
                             padx=20, pady=12)
        login_btn.pack(fill="x")
        
        # Nút hủy
        cancel_btn = tk.Button(box, text="Hủy",
                              command=self.cancel,
                              font=("Helvetica", 11),
                              bg="#f0f4f8", fg="#64748b",
                              activebackground="#e2e8f0",
                              activeforeground="#0f172a", 
                              cursor="hand2",
                              relief="flat",
                              padx=10, pady=6)
        cancel_btn.pack(pady=(12, 0))
        
        self.bind("<Escape>", lambda event: self.cancel())
        
    def apply(self):
        self.username = self.username_entry.get().strip()
        self.password = self.password_entry.get().strip()
        if self.username == "admin" and self.password == "1":
            self.result = True
        
def show_login_dialog(root):
    while True:
        dialog = EnhancedLoginDialog(root, title="Đăng Nhập Hệ Thống")
        if dialog.result:
            return True
        elif dialog.username is None and dialog.password is None:
            # Người dùng nhấn cancel hoặc đóng dialog
            return False
        else:
            messagebox.showerror("Lỗi đăng nhập", "Tài khoản hoặc mật khẩu không đúng!")