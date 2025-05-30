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
            
            # Cập nhật thông tin xe vào UI
            if self.ui:
                du_lieu_xe_vao = {
                    "bien_so": bien_so or "",
                    "gio_vao": gio_vao,
                    "gio_ra": "",  # Chưa có
                    "ma_the": ma_the,
                    "thoi_gian_do": "",  # Chưa có
                    "phi": "",  # Chưa có
                    "chinh_sach": chinh_sach or "",
                    "cong_vao": cong_vao,
                    "cong_ra": "",  # Chưa có
                    "trang_thai": "Trong bãi",
                    "loai_xe": self.ui.loai_xe_hien_tai if self.ui else "xe_may"
                }
                # Cập nhật thông tin xe lên UI
                self.ui.cap_nhat_thong_tin_xe(du_lieu_xe_vao)
        else:
            error_msg = success.get('message', 'Unknown error')
            print(f"Lỗi: {error_msg}")

        if self.ui:
            self.ui.cap_nhat_trang_thai_xe_vao(ma_the, bien_so, success)
        return success

    def xu_ly_xe_ra(self, ma_the, duong_dan_anh_ra, cong_ra, camera_id, plate_match=None, bien_so_ra=None):
        print("Xu ly xe ra", ma_the, cong_ra, camera_id, plate_match, bien_so_ra)
        
        try:
            # Bước 1: Load phiên gửi xe theo mã thẻ
            print(f"🔍 DEBUG: Gọi API loadPhienGuiXeTheoMaThe cho mã thẻ: {ma_the}")
            response = api.loadPhienGuiXeTheoMaThe(ma_the)
            
            print(f"🔍 DEBUG: API Response type: {type(response)}")
            print(f"🔍 DEBUG: API Response: {response}")
            
            # Xử lý response từ API
            session = None
            if isinstance(response, list) and len(response) > 0:
                # API trả về list, lấy phần tử đầu tiên (phiên gửi xe gần nhất)
                session = response[0]
                print(f"🔍 DEBUG: Lấy session từ list: {session}")
            elif isinstance(response, dict):
                # Nếu response là dict với format {"success": True, "data": {...}}
                if response.get("success") and response.get("data"):
                    data = response["data"]
                    if isinstance(data, list) and len(data) > 0:
                        session = data[0]
                    else:
                        session = data
                else:
                    msg = response.get("message", "Không tìm thấy phiên gửi xe")
                    print(f"❌ API trả về lỗi: {msg}")
                    if self.ui:
                        self.ui.cap_nhat_trang_thai_xe_ra(ma_the, "", False, msg)
                    return {"success": False, "message": msg}
            elif hasattr(response, '__dict__'):
                # Nếu response là object, dùng trực tiếp
                session = response
            else:
                msg = "Không tìm thấy phiên gửi xe hoặc format response không đúng"
                print(f"❌ {msg}")
                if self.ui:
                    self.ui.cap_nhat_trang_thai_xe_ra(ma_the, "", False, msg)
                return {"success": False, "message": msg}
            
            if not session:
                msg = "Dữ liệu phiên gửi xe trống"
                print(f"❌ {msg}")
                if self.ui:
                    self.ui.cap_nhat_trang_thai_xe_ra(ma_the, "", False, msg)
                return {"success": False, "message": msg}
            
            print(f"🔍 DEBUG: Session object: {session}")
            
            # Lấy thông tin từ session object (sử dụng getattr thay vì .get())
            bien_so_vao = getattr(session, 'bienSo', '') or ''
            anh_vao_url = getattr(session, 'anhVao', '') or ''
            ma_phien = getattr(session, 'maPhien', '') or ''
            
            print(f"🔍 DEBUG: Biển số vào = '{bien_so_vao}', Biển số ra = '{bien_so_ra}'")
            print(f"🔍 DEBUG: URL ảnh vào = '{anh_vao_url}'")
            print(f"🔍 DEBUG: Mã phiên = '{ma_phien}'")
            
            # Hiển thị ảnh xe vào ngay lập tức
            if self.ui and anh_vao_url:
                self.ui.hien_thi_anh_xe_vao_trong_xac_nhan_ra(anh_vao_url, bien_so_vao, ma_the)
            
            # Kiểm tra biển số có khớp không
            bien_so_khop = self.kiem_tra_bien_so_khop(bien_so_vao, bien_so_ra)
            print(f"🔍 DEBUG: Kết quả kiểm tra khớp = {bien_so_khop}")
            
            if not bien_so_khop and self.ui:
                print("🚨 Hiển thị dialog lỗi biển số")
                ket_qua = self.xu_ly_loi_bien_so(ma_the, bien_so_vao, bien_so_ra, duong_dan_anh_ra)
                print(f"🔍 DEBUG: Kết quả dialog = {ket_qua}")
                
                if isinstance(ket_qua, str) and ket_qua.startswith("xac_nhan:"):
                    bien_so_ra = ket_qua.split(":", 1)[1]
                    print(f"🔍 DEBUG: Biển số mới từ dialog = {bien_so_ra}")
                    bien_so_khop = True  # Người dùng đã xác nhận
                elif ket_qua == "huy":
                    return {"success": False, "message": "Người dùng hủy bỏ"}
                else:
                    return {"success": False, "message": "Xử lý lỗi biển số thất bại"}
            
            # Bước 2: Cập nhật phiên gửi xe (xe ra) - SỬ DỤNG API ĐÚNG
            thoi_gian_hien_tai = datetime.now()
            
            # Tạo object PhienGuiXe để cập nhật
            session_update = models.PhienGuiXe(
                maPhien=ma_phien,
                uidThe=ma_the,
                bienSo=bien_so_vao,  # Giữ nguyên biển số vào
                viTriGui=getattr(session, 'viTriGui', None),
                chinhSach=getattr(session, 'chinhSach', ''),
                congVao=getattr(session, 'congVao', ''),
                gioVao=getattr(session, 'gioVao', ''),
                anhVao=getattr(session, 'anhVao', ''),
                trangThai='DA_RA',  # Cập nhật trạng thái
                congRa=cong_ra,
                gioRa=thoi_gian_hien_tai.strftime("%Y-%m-%d %H:%M:%S"),
                anhRa=duong_dan_anh_ra,
                camera_id=camera_id,
                plate_match=1 if bien_so_khop else 0,
                plate=bien_so_ra
            )
            
            print(f"🔍 DEBUG: Cập nhật phiên gửi xe: {session_update}")
            
            # **DÙNG API CẬP NHẬT PHIÊN GỬI XE**
            result = api.capNhatPhienGuiXe(session_update)
            
            if result:
                print("✅ Cập nhật xe ra thành công, bắt đầu load dữ liệu hoàn chỉnh...")
                
                # Bước 3: Load lại dữ liệu hoàn chỉnh từ server
                self.load_va_hien_thi_du_lieu_xe_ra(ma_the)
                
                return {"success": True, "message": "Xe ra thành công"}
            else:
                msg = "Lỗi cập nhật phiên gửi xe"
                if self.ui:
                    self.ui.cap_nhat_trang_thai_xe_ra(ma_the, bien_so_vao, False, msg)
                return {"success": False, "message": msg}
                
        except Exception as e:
            print(f"❌ Lỗi xử lý xe ra: {e}")
            import traceback
            traceback.print_exc()
            if self.ui:
                self.ui.cap_nhat_trang_thai_xe_ra(ma_the, "", False, str(e))
            return {"success": False, "message": str(e)}

    def load_va_hien_thi_du_lieu_xe_ra(self, ma_the):
        """Load dữ liệu hoàn chỉnh từ API và hiển thị lên UI"""
        try:
            print(f"🔍 DEBUG: Bắt đầu load dữ liệu hoàn chỉnh cho mã thẻ {ma_the}")
            
            # Gọi API loadPhienGuiXeTheoMaThe lần nữa để lấy dữ liệu mới nhất
            response = api.loadPhienGuiXeTheoMaThe_XeRa(ma_the)
            
            session = None
            if isinstance(response, list) and len(response) > 0:
                session = response[0]
            elif isinstance(response, dict):
                if response.get("success") and response.get("data"):
                    data = response["data"]
                    if isinstance(data, list) and len(data) > 0:
                        session = data[0]
                    else:
                        session = data
                else:
                    msg = response.get("message", "Lỗi load dữ liệu từ server")
                    print(f"❌ Load dữ liệu thất bại: {msg}")
                    if self.ui:
                        self.ui.cap_nhat_trang_thai_xe_ra(ma_the, "", False, msg)
                    return
            elif hasattr(response, '__dict__'):
                session = response
            else:
                msg = "Không có response từ server hoặc format không đúng"
                print(f"❌ Load dữ liệu thất bại: {msg}")
                if self.ui:
                    self.ui.cap_nhat_trang_thai_xe_ra(ma_the, "", False, msg)
                return
            
            print(f"🔍 DEBUG: Session object nhận được: {session}")
            
            # Chuyển đổi dữ liệu để hiển thị lên UI
            du_lieu_xe = self.chuyen_doi_session_object_sang_ui(session)
            
            if self.ui:
                print(f"🔍 DEBUG: Cập nhật UI với dữ liệu: {du_lieu_xe}")
                
                # Cập nhật thông tin xe lên UI
                self.ui.cap_nhat_thong_tin_xe(du_lieu_xe)
                
                # Cập nhật danh sách xe
                self.cap_nhat_xe_trong_danh_sach(du_lieu_xe)
                self.ui.cap_nhat_danh_sach_xe(du_lieu_xe, la_moi=False)
                
                # Cập nhật trạng thái thành công
                self.ui.cap_nhat_trang_thai_xe_ra(ma_the, du_lieu_xe["bien_so"], True)
                
                print(f"✅ Đã load và hiển thị dữ liệu hoàn chỉnh cho mã thẻ {ma_the}")
            
        except Exception as e:
            print(f"❌ Lỗi load và hiển thị dữ liệu: {e}")
            import traceback
            traceback.print_exc()
            if self.ui:
                self.ui.cap_nhat_trang_thai_xe_ra(ma_the, "", False, f"Lỗi load dữ liệu: {str(e)}")

    def chuyen_doi_session_object_sang_ui(self, session):
        """Chuyển đổi session object từ API response sang format UI"""
        try:
            # Lấy dữ liệu từ session object sử dụng getattr
            gio_vao_str = getattr(session, 'gioVao', '') or ''
            gio_ra_str = getattr(session, 'gioRa', '') or ''
            bien_so = getattr(session, 'bienSo', '') or ''
            ma_the = getattr(session, 'uidThe', '') or ''
            chinh_sach = getattr(session, 'chinhSach', '') or ''
            cong_vao = getattr(session, 'congVao', '') or ''
            cong_ra = getattr(session, 'congRa', '') or ''
            phi_value = getattr(session, 'phi', '') or ''
            
            print(f"🔍 DEBUG: Trích xuất dữ liệu từ session:")
            print(f"  - Biển số: {bien_so}")
            print(f"  - Giờ vào: {gio_vao_str}")
            print(f"  - Giờ ra: {gio_ra_str}")
            print(f"  - Phí: {phi_value}")
            
            # Tính thời gian đỗ
            thoi_gian_do_formatted = ""
            if gio_vao_str and gio_ra_str:
                try:
                    gio_vao = datetime.strptime(gio_vao_str, "%Y-%m-%d %H:%M:%S")
                    gio_ra = datetime.strptime(gio_ra_str, "%Y-%m-%d %H:%M:%S")
                    thoi_gian_do = gio_ra - gio_vao
                    
                    gio_do = int(thoi_gian_do.total_seconds() // 3600)
                    phut_do = int((thoi_gian_do.total_seconds() % 3600) // 60)
                    thoi_gian_do_formatted = f"{gio_do}h {phut_do}m"
                except Exception as e:
                    print(f"⚠️ Lỗi tính thời gian đỗ: {e}")
                    thoi_gian_do_formatted = "N/A"
            
            # Format phí
            phi_formatted = ""
            if phi_value:
                try:
                    phi = int(phi_value)
                    phi_formatted = f"{phi:,} VND"
                except:
                    phi_formatted = str(phi_value)
            
            # Xác định loại xe
            loai_xe = "xe_may"  # mặc định
            if "oto" in chinh_sach.lower() or "xe_hoi" in chinh_sach.lower() or "CS_OTO" in chinh_sach:
                loai_xe = "oto"
            
            # Tạo dữ liệu UI
            du_lieu_xe = {
                "bien_so": bien_so,
                "gio_vao": gio_vao_str,
                "gio_ra": gio_ra_str,
                "ma_the": ma_the,
                "thoi_gian_do": thoi_gian_do_formatted,
                "phi": phi_formatted,
                "cong_vao": cong_vao,
                "cong_ra": cong_ra,
                "chinh_sach": chinh_sach,
                "trang_thai": "Đã ra" if gio_ra_str else "Trong bãi",
                "loai_xe": loai_xe,
                "nhan_dien_boi_api": getattr(session, 'plate_match', 0) == 1,
                "da_xac_minh": True,
            }
            
            print(f"🔍 DEBUG: Dữ liệu UI được tạo: {du_lieu_xe}")
            return du_lieu_xe
            
        except Exception as e:
            print(f"❌ Lỗi chuyển đổi session object: {e}")
            import traceback
            traceback.print_exc()
            
            # Fallback data
            return {
                "bien_so": getattr(session, 'bienSo', '') if hasattr(session, 'bienSo') else "",
                "gio_vao": getattr(session, 'gioVao', '') if hasattr(session, 'gioVao') else "",
                "gio_ra": getattr(session, 'gioRa', '') if hasattr(session, 'gioRa') else "",
                "ma_the": getattr(session, 'uidThe', '') if hasattr(session, 'uidThe') else "",
                "thoi_gian_do": "",
                "phi": "",
                "cong_vao": getattr(session, 'congVao', '') if hasattr(session, 'congVao') else "",
                "cong_ra": getattr(session, 'congRa', '') if hasattr(session, 'congRa') else "",
                "chinh_sach": getattr(session, 'chinhSach', '') if hasattr(session, 'chinhSach') else "",
                "trang_thai": "Lỗi dữ liệu",
                "loai_xe": "xe_may",
                "nhan_dien_boi_api": False,
                "da_xac_minh": False
            }

    def kiem_tra_bien_so_khop(self, bien_so_vao, bien_so_ra):
        """Kiểm tra xem biển số có khớp không"""
        if not bien_so_vao or not bien_so_ra:
            return False
        
        # Chuẩn hóa biển số (loại bỏ khoảng trắng, chuyển hoa)
        bien_so_vao_clean = str(bien_so_vao).strip().upper().replace(" ", "").replace("-", "")
        bien_so_ra_clean = str(bien_so_ra).strip().upper().replace(" ", "").replace("-", "")
        
        print(f"So sánh biển số: '{bien_so_vao_clean}' vs '{bien_so_ra_clean}'")
        
        # Kiểm tra khớp chính xác TRƯỚC
        if bien_so_vao_clean == bien_so_ra_clean:
            print("Biển số khớp chính xác")
            return True
        
        # **THÊM KIỂM TRA CHẶT CHẼ HƠN**
        # Nếu độ dài khác nhau quá 2 ký tự -> không khớp
        if abs(len(bien_so_vao_clean) - len(bien_so_ra_clean)) > 2:
            print("Biển số khác nhau quá nhiều về độ dài")
            return False
        
        # Kiểm tra khớp với tolerance nhưng CHẶT HƠN
        from difflib import SequenceMatcher
        similarity = SequenceMatcher(None, bien_so_vao_clean, bien_so_ra_clean).ratio()
        
        print(f"Độ tương đồng: {similarity:.2%}")
        
        # **GIẢM THRESHOLD XUỐNG 95%** để chặt chẽ hơn
        is_similar = similarity >= 0.95
        
        if is_similar:
            print("Biển số được coi là khớp (similarity >= 95%)")
        else:
            print("Biển số KHÔNG khớp (similarity < 95%)")
        
        return is_similar

    def xu_ly_loi_bien_so(self, ma_the, bien_so_vao, bien_so_ra, anh_xe_ra):
        """Xử lý khi biển số không khớp"""
        try:
            from dialogs.BienSoLoiDialog import BienSoLoiDialog
            
            # Lấy URL ảnh vào từ session hiện tại
            response = api.loadPhienGuiXeTheoMaThe(ma_the)
            anh_vao_url = None
            
            if response:
                session = None
                if isinstance(response, list) and len(response) > 0:
                    session = response[0]
                elif isinstance(response, dict) and response.get("success") and response.get("data"):
                    data = response["data"]
                    session = data[0] if isinstance(data, list) and len(data) > 0 else data
                elif hasattr(response, '__dict__'):
                    session = response
                
                if session:
                    anh_vao_url = getattr(session, 'anhVao', '') or ''
                    print(f"🔍 DEBUG Dialog: URL ảnh vào: {anh_vao_url}")
            
            # Chuyển đổi ảnh ra nếu cần
            anh_pil = None
            if anh_xe_ra:
                try:
                    if isinstance(anh_xe_ra, str):
                        from PIL import Image
                        anh_pil = Image.open(anh_xe_ra)
                    elif hasattr(anh_xe_ra, 'save'):
                        anh_pil = anh_xe_ra
                except Exception as e:
                    print(f"Lỗi xử lý ảnh ra: {e}")
            
            # Hiển thị dialog với cả ảnh vào và ảnh ra
            dialog = BienSoLoiDialog(
                self.ui.root, 
                ma_the, 
                bien_so_vao, 
                bien_so_ra, 
                anh_pil,
                anh_vao_url  
            )
            
            ket_qua, bien_so_thuc = dialog.hien_thi()
            print(f"🔍 DEBUG Dialog: Kết quả = {ket_qua}, Biển số = {bien_so_thuc}")
            
            if ket_qua == "xac_nhan" and bien_so_thuc:
                return f"xac_nhan:{bien_so_thuc}"
            else:
                return ket_qua or "huy"
                
        except Exception as e:
            print(f"❌ Lỗi hiển thị dialog: {e}")
            import traceback
            traceback.print_exc()
            return "huy"

    def cap_nhat_xe_trong_danh_sach(self, du_lieu_xe):
        """Cập nhật hoặc thêm xe vào danh sách quản lý"""
        # Tạo danh sách nếu chưa có
        if not hasattr(self, 'xe') or not isinstance(self.xe, list):
            self.xe = []
        
        ma_the = du_lieu_xe["ma_the"]
        bien_so = du_lieu_xe["bien_so"]
        
        # Tìm xe trong danh sách
        xe_ton_tai = None
        for xe in self.xe:
            if xe["ma_the"] == ma_the:
                xe_ton_tai = xe
                break
        
        if xe_ton_tai:
            # Cập nhật xe hiện có
            xe_ton_tai.update(du_lieu_xe)
            print(f"✅ Đã cập nhật xe {bien_so} trong danh sách")
        else:
            # Thêm xe mới
            self.xe.append(du_lieu_xe)
            print(f"✅ Đã thêm xe {bien_so} vào danh sách")