import tkinter as tk
import os
import sys
from components.login import show_login_dialog

goi_can_thiet = ['opencv-python', 'pillow', 'numpy', 'keyboard', 'requests', 'mysql-connector-python']

def kiem_tra_va_cai_dat_goi():
    import importlib.util
    import subprocess
    for goi in goi_can_thiet:
        try:
            if goi == 'opencv-python':
                ten_goi = 'cv2'
            elif goi == 'pillow':
                ten_goi = 'PIL'
            elif goi == 'mysql-connector-python':
                ten_goi = 'mysql.connector'
            else:
                ten_goi = goi
            spec = importlib.util.find_spec(ten_goi)
            if spec is None:
                print(f"Đang cài đặt {goi}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", goi])
                print(f"Đã cài đặt {goi}.")
        except Exception as e:
            print(f"Lỗi khi cài đặt {goi}: {e}")
            print(f"Vui lòng cài đặt thủ công bằng lệnh: pip install {goi}")
            if goi in ['opencv-python', 'keyboard', 'requests', 'mysql-connector-python']:
                print("Ứng dụng không thể chạy mà không có gói này.")
                sys.exit(1)

kiem_tra_va_cai_dat_goi()

os.makedirs("server/images", exist_ok=True)
os.makedirs("server/data", exist_ok=True)
os.makedirs("server/logs", exist_ok=True)
os.makedirs("server/config", exist_ok=True)

if not os.path.exists("server/config/db_config.json"):
    with open("server/config/db_config.json", "w", encoding="utf-8") as f:
        f.write("""{
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "PM",
    "port": 3306
}
""")

from components.ui import GiaoDienQuanLyBaiXe
from components.camera import QuanLyCamera
from components.vehicle import QuanLyXe
from components.card_reader import DauDocThe

def main():
    if __name__ == "__main__":
        root = tk.Tk()
        root.withdraw()  # Ẩn cửa sổ chính cho đến khi đăng nhập thành công

        # Gọi login dialog
        if not show_login_dialog(root):
            root.destroy()
            sys.exit(0)
        root.deiconify()  # Hiện cửa sổ chính sau khi đăng nhập

        root.title("Hệ Thống Quản Lý Bãi Đỗ Xe")
        root.geometry("1280x800")
        root.configure(bg="#f0f9ff")
    try:
        if os.path.exists("assets/icon.ico"):
            root.iconbitmap("assets/icon.ico")
    except:
        pass

    quan_ly_camera = QuanLyCamera()
    quan_ly_xe = QuanLyXe()
    dau_doc_the = DauDocThe()

    app = GiaoDienQuanLyBaiXe(root, quan_ly_camera, quan_ly_xe, dau_doc_the)

    print("Ứng dụng đã được khởi động. Quét thẻ ở bất cứ đâu để chụp ảnh. Nhấn 'q' để thoát.")

    root.protocol("WM_DELETE_WINDOW", app.khi_dong_cua_so)
    root.mainloop()

if __name__ == "__main__":
    main()