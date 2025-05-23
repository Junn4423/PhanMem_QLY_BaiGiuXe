from pydantic import BaseModel
from typing import Optional

# 1. Loại Phương Tiện (pm_nc0001)
class LoaiPhuongTien(BaseModel):
    maLoaiPT: str
    tenLoaiPT: str
    moTa: Optional[str] = None

# 2. Phương Tiện (pm_nc0002)
class PhuongTien(BaseModel):
    bienSo: str
    maLoaiPT: str

# 3. Thẻ RFID (pm_nc0003)
class TheRFID(BaseModel):
    uidThe: str
    loaiThe: str
    trangThai: str
    ngayPhatHanh: str

# 4. Khu Vực Đỗ Xe (pm_nc0004)
class KhuVuc(BaseModel):
    maKhuVuc: str
    tenKhuVuc: str
    moTa: Optional[str] = None

# 5. Chỗ Đỗ Xe (pm_nc0005)
class ChoDo(BaseModel):
    maChoDo: str
    maKhuVuc: str
    trangThai: str
    tenKhuVuc: Optional[str] = None 


#9. Phiên gửi xe (pm_nc0009)
class PhienGuiXe(BaseModel):
    maPhien: Optional[str] = None   # Cho phép None
    uidThe: str
    bienSo: str
    viTriGui: Optional[str] = None
    chinhSach: str
    congVao: str
    gioVao: str
    anhVao: str
    trangThai: Optional[str] = None
    congRa: Optional[str] = None
    gioRa: Optional[str] = None
    phutGui: Optional[int] = None
    anhRa: Optional[str] = None
    phi: Optional[float] = None
    # Các trường backend/log bổ sung:
    camera_id: Optional[str] = None
    plate_match: Optional[int] = None
    plate: Optional[str] = None

# 10. Nhật ký gửi xe (pm_nc0010)
class NhatKyGuiXe(BaseModel):
    id: Optional[int] = None
    session_id: str
    camera_id: Optional[str] = None
    time: str
    image_path: Optional[str] = None
    plate_match: Optional[int] = None
    direction: str # 'entry' or 'exit'