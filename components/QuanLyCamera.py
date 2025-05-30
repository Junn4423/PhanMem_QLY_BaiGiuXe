
import cv2
import numpy as np
import threading
import time
import os
import re
import requests
from PIL import Image

class QuanLyCamera:
    def __init__(self):
        self.camera_vao = None
        self.camera_ra = None
        self.luong_camera_vao = None
        self.luong_camera_ra = None
        self.camera_dang_chay = False
        self.khung_hinh_cuoi_vao = None
        self.khung_hinh_cuoi_ra = None
        self.anh_da_chup = None
        self.ui = None
        self.camera_hien_tai = "vao"
        os.makedirs("server/images", exist_ok=True)
        try:
            from server import url
            self.url_rtsp_vao = url.rtsp_url_in
            self.url_rtsp_ra = url.rtsp_url_out
            self.api_bien_so = url.api_BienSo
        except ImportError:
            self.url_rtsp_vao = 0
            self.url_rtsp_ra = 1
            self.api_bien_so = None

    def dat_ui(self, ui):
        self.ui = ui

    def bat_dau_camera(self):
        self.luong_camera_vao = threading.Thread(target=self.vong_lap_camera_vao, daemon=True)
        self.luong_camera_ra = threading.Thread(target=self.vong_lap_camera_ra, daemon=True)
        self.camera_dang_chay = True
        self.luong_camera_vao.start()
        self.luong_camera_ra.start()

    def dung_camera(self):
        self.camera_dang_chay = False
        if self.luong_camera_vao and self.luong_camera_vao.is_alive():
            self.luong_camera_vao.join(1.0)
        if self.luong_camera_ra and self.luong_camera_ra.is_alive():
            self.luong_camera_ra.join(1.0)
        if self.camera_vao is not None and self.camera_vao.isOpened():
            self.camera_vao.release()
        if self.camera_ra is not None and self.camera_ra.isOpened():
            self.camera_ra.release()

    def chuyen_doi_camera(self, che_do):
        self.camera_hien_tai = che_do

    def vong_lap_camera_vao(self):
        try:
            self.camera_vao = cv2.VideoCapture(self.url_rtsp_vao)
            if not self.camera_vao.isOpened():
                print(f"Lỗi: Không thể mở camera vào.")
                return
            while self.camera_dang_chay:
                ret, frame = self.camera_vao.read()
                if ret:
                    self.khung_hinh_cuoi_vao = frame
                    img = self._frame_to_img(frame)
                    if self.ui:
                        self.ui.root.after(0, self.ui.cap_nhat_khung_camera_vao, img)
                time.sleep(0.03)
        except Exception as e:
            print(f"Lỗi camera vào: {e}")
        finally:
            if self.camera_vao is not None and self.camera_vao.isOpened():
                self.camera_vao.release()

    def vong_lap_camera_ra(self):
        try:
            self.camera_ra = cv2.VideoCapture(self.url_rtsp_ra)
            if not self.camera_ra.isOpened():
                print(f"Lỗi: Không thể mở camera ra.")
                return
            while self.camera_dang_chay:
                ret, frame = self.camera_ra.read()
                if ret:
                    self.khung_hinh_cuoi_ra = frame
                    img = self._frame_to_img(frame)
                    if self.ui:
                        self.ui.root.after(0, self.ui.cap_nhat_khung_camera_ra, img)
                time.sleep(0.03)
        except Exception as e:
            print(f"Lỗi camera ra: {e}")
        finally:
            if self.camera_ra is not None and self.camera_ra.isOpened():
                self.camera_ra.release()

    def chup_anh(self, ma_the=None, che_do="vao"):
        khung_hinh_cuoi = self.khung_hinh_cuoi_vao if che_do == "vao" else self.khung_hinh_cuoi_ra
        duong_dan = None
        bien_so = None
        if khung_hinh_cuoi is not None:
            print(f"Đã lấy được khung hình từ camera ({che_do})")  # Debug
            self.anh_da_chup = khung_hinh_cuoi.copy()
            if ma_the:
                ten_file = f"{ma_the}_{int(time.time())}.jpg"
                duong_dan = os.path.join("server/images", ten_file)
                cv2.imwrite(duong_dan, self.anh_da_chup)
                print(f"Đã lưu ảnh tại: {duong_dan}")  # Debug
                if not os.path.exists(duong_dan):
                    print(f"Lỗi: Không thể lưu ảnh tại {duong_dan}")
                    duong_dan = None  # Đặt lại duong_dan nếu lưu thất bại
                else:
                    # Gọi API nhận diện biển số nếu có
                    if self.api_bien_so:
                        try:
                            with open(duong_dan, "rb") as file_anh:
                                files = {"file": file_anh}
                                response = requests.post(self.api_bien_so, files=files, timeout=10)
                                if response.status_code == 200:
                                    ket_qua = response.json()
                                    if ket_qua.get("ket_qua"):
                                        chuoi_ocr = ket_qua["ket_qua"][0].get("ocr", "")
                                        match = re.search(r"text='(.*?)'", chuoi_ocr)
                                        if match:
                                            bien_so = match.group(1)
                                            print(f"Nhận diện biển số thành công: {bien_so}")
                        except Exception as e:
                            print("Lỗi khi gửi ảnh lên API biển số:", e)
            else:
                print("Lỗi: Không có mã thẻ để lưu ảnh")
            
            # Cập nhật ảnh vừa chụp lên giao diện (truyền đường dẫn thay vì img)
            if self.ui and duong_dan:
                self.ui.cap_nhat_anh_gan_day(duong_dan)
            else:
                print("Không thể cập nhật ảnh vừa chụp: Không có đường dẫn hoặc UI không tồn tại")
            
            return duong_dan, bien_so
        else:
            print(f"Lỗi: Không có khung hình từ camera ({che_do})")
            return None, None

    def _frame_to_img(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        target_width = 320
        target_height = 240
        height, width = rgb_frame.shape[:2]
        scale = max(target_width / width, target_height / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        rgb_frame = cv2.resize(rgb_frame, (new_width, new_height))
        start_x = max(0, (new_width - target_width) // 2)
        start_y = max(0, (new_height - target_height) // 2)
        rgb_frame = rgb_frame[start_y:start_y+target_height, start_x:start_x+target_width]
        if rgb_frame.shape[0] != target_height or rgb_frame.shape[1] != target_width:
            rgb_frame = cv2.resize(rgb_frame, (target_width, target_height))
        img = Image.fromarray(rgb_frame)
        return img