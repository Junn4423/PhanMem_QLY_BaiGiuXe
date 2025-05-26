import requests
from typing import List
import models
import server.url as url

def layALLLoaiPhuongTien() -> List[models.LoaiPhuongTien]:
    api = url.url_api
    payload = {
        "table": "pm_nc0001",
        "func": "data"
    }
    res = requests.post(api, json=payload)
    res.raise_for_status()
    raw_data = res.json()
    return [models.LoaiPhuongTien(**item) for item in raw_data]
def lay_danh_sach_khu():
    import requests
    import server.url as url
    api = url.url_api
    payload = {
        "table": "pm_nc0004",
        "func": "khu_vuc_camera_cong"
    }
    res = requests.post(api, json=payload)
    return res.json()
def themLoaiPhuongTien(loai_phuong_tien: models.LoaiPhuongTien) -> bool:
    api = url.url_api
    payload = {
        "table": "pm_nc0001",
        "func": "add",
        "maLoaiPT": loai_phuong_tien.maLoaiPT,
        "tenLoaiPT": loai_phuong_tien.tenLoaiPT,
        "moTa": loai_phuong_tien.moTa
    }
    res = requests.post(api, json=payload)
    res.raise_for_status()
    return res.json().get('success', False)

def capNhatLoaiPhuongTien(loai_phuong_tien: models.LoaiPhuongTien) -> bool:
    api = url.url_api
    payload = {
        "table": "pm_nc0001",
        "func": "edit",
        "maLoaiPT": loai_phuong_tien.maLoaiPT,
        "tenLoaiPT": loai_phuong_tien.tenLoaiPT,
        "moTa": loai_phuong_tien.moTa
    }
    res = requests.post(api, json=payload)
    res.raise_for_status()
    return res.json().get('success', False)

def xoaLoaiPhuongTien(ma_loai_phuong_tien: str) -> bool:
    api = url.url_api
    payload = {
        "table": "pm_nc0001",
        "func": "delete",
        "maLoaiPT": ma_loai_phuong_tien
    }
    res = requests.post(api, json=payload)
    res.raise_for_status()
    return res.json().get('success', False)

def layALLPhienGuiXe() -> List[models.PhienGuiXe]:
    api = url.url_api
    payload = {
        "table": "pm_nc0009",
        "func": "data"
    }
    res = requests.post(api, json=payload)
    res.raise_for_status()
    raw_data = res.json()
    # Nếu API trả về {'success': true, 'data': [...]}, thì lấy res.json()['data']
    return [models.PhienGuiXe(**item) for item in raw_data.get('data', raw_data)]

def themPhienGuiXe(session: models.PhienGuiXe) -> bool:
    api = url.url_api
    payload = {
        "table": "pm_nc0009",
        "func": "add",
        "uidThe": session.uidThe,
        "bienSo": session.bienSo,
        "viTriGui": getattr(session, "viTriGui", None),
        "chinhSach": session.chinhSach,
        "congVao": session.congVao,
        "gioVao": session.gioVao,
        "anhVao": session.anhVao,
        "camera_id": getattr(session, "camera_id", None), 
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    print("Payload gửi lên:", payload)
    res = requests.post(api, json=payload)
    try:
        res.raise_for_status()
        if not res.text.strip():
            print("API trả về rỗng!")
            return False
        return res.json().get('success', False)
    except Exception as e:
        print("Lỗi gọi API:", e)
        print("Status code:", res.status_code)
        print("Response text:", res.text)
        return False

def capNhatPhienGuiXe(session: models.PhienGuiXe) -> dict:
    import requests
    api = url.url_api
    payload = {
        "table": "pm_nc0009",
        "func": "edit",
        "maPhien": session.maPhien,
        "congRa": session.congRa,
        "gioRa": session.gioRa,
        "anhRa": session.anhRa,
        "camera_id": getattr(session, "camera_id", None),
        "plate_match": getattr(session, "plate_match", None),
        "plate": getattr(session, "plate", None),
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    print("Payload gửi lên:", payload)
    res = requests.post(api, json=payload)
    res.raise_for_status()
    return res.json()

def loadPhienGuiXeTheoMaThe(ma_the: str) -> models.PhienGuiXe:
    api = url.url_api
    payload = {
        "table": "pm_nc0009",
        "func": "layPhienGuiXeTuUID",
        "uidThe": ma_the
    }
    res = requests.post(api, json=payload)
    res.raise_for_status()
    raw_data = res.json()
    return [models.PhienGuiXe(**item) for item in raw_data] if raw_data else None

def loadPhienGuiXeTheoMaThe_XeRa(ma_the: str) -> models.PhienGuiXe:
    api = url.url_api
    payload = {
        "table": "pm_nc0009",
        "func": "layPhienGuiXeTuUID_Da_Ra",
        "uidThe": ma_the
    }
    res = requests.post(api, json=payload)
    res.raise_for_status()
    raw_data = res.json()
    return [models.PhienGuiXe(**item) for item in raw_data] if raw_data else None