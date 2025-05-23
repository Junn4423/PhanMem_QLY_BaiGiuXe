
from datetime import datetime
from server import api
import models

class QuanLyXe:
    def __init__(self):
        self._phien_gui_xe_dang_gui = {}  # theo mã thẻ
        self.ui = None

    def dat_ui(self, ui):
        self.ui = ui

    def xu_ly_xe_vao(self, ma_the, duong_dan_anh, bien_so, chinh_sach, cong_vao, camera_id):
        # Tự động xác định mã chính sách nếu chưa có
        if not chinh_sach and self.ui:
            if self.ui.che_do_hien_tai == "vao":
                if self.ui.loai_xe_hien_tai == "xe_may":
                    chinh_sach = "CS_XEMAY_4H"
                elif self.ui.loai_xe_hien_tai == "oto":
                    chinh_sach = "CS_OTO_4H"
        gio_vao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session = models.PhienGuiXe(
            uidThe=ma_the,
            bienSo=bien_so or "",
            viTriGui=None,
            chinhSach=chinh_sach,
            congVao=cong_vao,
            gioVao=gio_vao,
            anhVao=duong_dan_anh or "", 
            camera_id=camera_id
        )
        success = api.themPhienGuiXe(session)
        if success:
            self._phien_gui_xe_dang_gui[ma_the] = session
        if self.ui:
            self.ui.cap_nhat_trang_thai_xe_vao(ma_the, bien_so, success)
        return success

    def xu_ly_xe_ra(self, ma_the, duong_dan_anh_ra, cong_ra, camera_id, plate_match=None, bien_so_ra=None):
        print("Xu ly xe ra", ma_the, cong_ra, camera_id, plate_match, bien_so_ra)
        phien_list = api.loadPhienGuiXeTheoMaThe(ma_the)
        if phien_list and len(phien_list) > 0:
            session = phien_list[0]  
        else:
            if self.ui:
                self.ui.cap_nhat_trang_thai_xe_ra(ma_the, '', False, msg="Không tìm thấy phiên gửi xe đang gửi")
            return False
        if not bien_so_ra or str(bien_so_ra).strip() == "":
            if self.ui:
                self.ui.cap_nhat_trang_thai_xe_ra(ma_the, '', False, msg="Không nhận diện được biển số khi xe ra")
            return False

        gio_ra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session.congRa = cong_ra
        session.gioRa = gio_ra
        session.anhRa = duong_dan_anh_ra or ""
        session.camera_id = camera_id
        session.plate_match = plate_match
        session.plate = bien_so_ra

        result = api.capNhatPhienGuiXe(session)
        is_success = result.get("success", False)
        message = result.get("message", "")

        if is_success:
            del self._phien_gui_xe_dang_gui[ma_the]
        if self.ui:
            self.ui.cap_nhat_trang_thai_xe_ra(
                ma_the,
                getattr(session, "bienSo", ""), 
                is_success,
                msg=message
            )
        return is_success

    