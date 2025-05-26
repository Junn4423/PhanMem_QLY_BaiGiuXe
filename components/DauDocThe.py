import threading
import keyboard

class DauDocThe:
    def __init__(self):
        self.luong_doc_the = None
        self.dang_chay = False
        self.dang_quet = False
        self.ui = None
        self.quan_ly_xe = None
        self.quan_ly_camera = None
        self.bo_dem_the = ""

    def dat_ui(self, ui):
        self.ui = ui
        self.quan_ly_xe = ui.quan_ly_xe
        self.quan_ly_camera = ui.quan_ly_camera

    def bat_dau_doc_the(self):
        self.luong_doc_the = threading.Thread(target=self.vong_lap_doc_the, daemon=True)
        self.dang_chay = True
        self.luong_doc_the.start()

    def dung_doc_the(self):
        self.dang_chay = False
        if self.luong_doc_the and self.luong_doc_the.is_alive():
            self.luong_doc_the.join(1.0)

    def reset_trang_thai_quet(self):
        """Reset trạng thái quét thẻ để cho phép quét tiếp"""
        self.dang_quet = False
        self.bo_dem_the = ""

    def vong_lap_doc_the(self):
        try:
            while self.dang_chay:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == 'enter':
                        if self.bo_dem_the and not self.dang_quet:
                            self.dang_quet = True
                            ma_the = self.bo_dem_the
                            if self.ui:
                                self.ui.root.after(0, lambda: self.ui.cap_nhat_trang_thai_dau_doc(f"Đã quét thẻ: {ma_the}", "#e74c3c"))
                                self.ui.root.after(100, lambda id=ma_the: self.xu_ly_quet_the(id))
                            self.bo_dem_the = ""
                        else:
                            self.bo_dem_the = ""
                    elif len(event.name) == 1:
                        self.bo_dem_the += event.name
        except Exception as e:
            print(f"Lỗi đầu đọc thẻ: {e}")

    def xu_ly_quet_the(self, ma_the):
        try:
            if self.ui:
                self.ui.cap_nhat_trang_thai_dau_doc(f"Đã quét thẻ: {ma_the}", "#2ecc71")
            if self.ui and self.quan_ly_camera and self.quan_ly_xe:
                che_do_hien_tai = self.ui.che_do_hien_tai
                khu = getattr(self.ui, 'khu_hien_tai', None)
                if not khu:
                    print("Không có khu hiện tại!")
                    return
                if che_do_hien_tai == "vao": 
                    cong_vao_str = khu['congVao'][0]['maCong'] if khu.get('congVao') and len(khu['congVao']) > 0 else "N/A"
                    camera_id = khu['cameraVao'][0]['maCamera'] if khu.get('cameraVao') and len(khu['cameraVao']) > 0 else "N/A"
                    khung_hinh_chup, bien_so = self.quan_ly_camera.chup_anh(ma_the, che_do="vao")
                    self.quan_ly_xe.xu_ly_xe_vao(ma_the, khung_hinh_chup, bien_so, None, cong_vao_str, camera_id)
                else:
                    cong_ra_str = khu['congRa'][0]['maCong'] if khu.get('congRa') and len(khu['congRa']) > 0 else "N/A"
                    camera_id = khu['cameraRa'][0]['maCamera'] if khu.get('cameraRa') and len(khu['cameraRa']) > 0 else "N/A"
                    anh_ra_path, bien_so_ra = self.quan_ly_camera.chup_anh(ma_the, che_do="ra")
                    plate_match = 1
                    res = self.quan_ly_xe.xu_ly_xe_ra(
                        ma_the,
                        anh_ra_path,
                        cong_ra_str,
                        camera_id,
                        plate_match,
                        bien_so_ra
                    )
                    if res and isinstance(res, dict) and not res.get("success", True):
                        message = res.get("message", "Có lỗi xảy ra")
                        self.ui.hien_thi_loi("Lỗi xe ra", message)
        finally:
            self.reset_trang_thai_quet()