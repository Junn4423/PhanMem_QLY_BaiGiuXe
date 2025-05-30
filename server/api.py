import requests
from typing import List, Dict, Any
import models
import server.url as url

def handle_api_response(response: requests.Response) -> Dict[str, Any]:
    try:
        response.raise_for_status()
        data = response.json()
        
        # Nếu API trả về success: false, raise exception với message
        if isinstance(data, dict) and data.get('success') == False:
            error_message = data.get('message', 'Unknown error from API')
            raise Exception(error_message)
        
        return data
    except requests.exceptions.HTTPError as e:
        # Thử lấy error message từ response body
        try:
            error_data = response.json()
            error_message = error_data.get('message', f'HTTP Error: {response.status_code}')
        except:
            error_message = f'HTTP Error: {response.status_code}'
        raise Exception(error_message)
    except Exception as e:
        # Re-raise exception với message gốc
        raise e

def layALLLoaiPhuongTien() -> List[models.LoaiPhuongTien]:
    api = url.url_api
    payload = {
        "table": "pm_nc0001",
        "func": "data"
    }
    res = requests.post(api, json=payload)
    raw_data = handle_api_response(res)
    return [models.LoaiPhuongTien(**item) for item in raw_data]

def lay_danh_sach_khu():
    api = url.url_api
    payload = {
        "table": "pm_nc0004",
        "func": "khu_vuc_camera_cong"
    }
    res = requests.post(api, json=payload)
    return handle_api_response(res)

def themLoaiPhuongTien(loai_phuong_tien: models.LoaiPhuongTien) -> Dict[str, Any]:
    """
    Trả về dict chứa success và message thay vì chỉ bool
    """
    api = url.url_api
    payload = {
        "table": "pm_nc0001",
        "func": "add",
        "maLoaiPT": loai_phuong_tien.maLoaiPT,
        "tenLoaiPT": loai_phuong_tien.tenLoaiPT,
        "moTa": loai_phuong_tien.moTa
    }
    res = requests.post(api, json=payload)
    return handle_api_response(res)

def capNhatLoaiPhuongTien(loai_phuong_tien: models.LoaiPhuongTien) -> Dict[str, Any]:
    api = url.url_api
    payload = {
        "table": "pm_nc0001",
        "func": "edit",
        "maLoaiPT": loai_phuong_tien.maLoaiPT,
        "tenLoaiPT": loai_phuong_tien.tenLoaiPT,
        "moTa": loai_phuong_tien.moTa
    }
    res = requests.post(api, json=payload)
    return handle_api_response(res)

def xoaLoaiPhuongTien(ma_loai_phuong_tien: str) -> Dict[str, Any]:
    api = url.url_api
    payload = {
        "table": "pm_nc0001",
        "func": "delete",
        "maLoaiPT": ma_loai_phuong_tien
    }
    res = requests.post(api, json=payload)
    return handle_api_response(res)

def layALLPhienGuiXe() -> List[models.PhienGuiXe]:
    api = url.url_api
    payload = {
        "table": "pm_nc0009",
        "func": "data"
    }
    res = requests.post(api, json=payload)
    raw_data = handle_api_response(res)
    # Nếu API trả về {'success': true, 'data': [...]}, thì lấy res.json()['data']
    return [models.PhienGuiXe(**item) for item in raw_data.get('data', raw_data)]

def themPhienGuiXe(session: models.PhienGuiXe) -> Dict[str, Any]:
    """
    Trả về dict chứa success và message từ API
    """
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
    
    try:
        res = requests.post(api, json=payload)
        return handle_api_response(res)
    except Exception as e:
        print("Lỗi gọi API:", str(e))
        print("Status code:", res.status_code if 'res' in locals() else 'N/A')
        print("Response text:", res.text if 'res' in locals() else 'N/A')
        # Trả về dict với thông tin lỗi
        return {
            "success": False,
            "message": str(e)
        }

def capNhatPhienGuiXe(session: models.PhienGuiXe) -> Dict[str, Any]:
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
    
    try:
        res = requests.post(api, json=payload)
        return handle_api_response(res)
    except Exception as e:
        print("Lỗi gọi API:", str(e))
        return {
            "success": False,
            "message": str(e)
        }

def loadPhienGuiXeTheoMaThe(ma_the: str) -> List[models.PhienGuiXe]:
    api = url.url_api
    payload = {
        "table": "pm_nc0009",
        "func": "layPhienGuiXeTuUID",
        "uidThe": ma_the
    }
    try:
        res = requests.post(api, json=payload)
        raw_data = handle_api_response(res)
        return [models.PhienGuiXe(**item) for item in raw_data] if raw_data else []
    except Exception as e:
        print(f"Lỗi load phiên gửi xe theo mã thẻ {ma_the}: {str(e)}")
        return []

def loadPhienGuiXeTheoMaThe_XeRa(ma_the: str) -> List[models.PhienGuiXe]:
    api = url.url_api
    payload = {
        "table": "pm_nc0009",
        "func": "layPhienGuiXeTuUID_Da",
        "uidThe": ma_the
    }
    try:
        res = requests.post(api, json=payload)
        raw_data = handle_api_response(res)
        return [models.PhienGuiXe(**item) for item in raw_data] if raw_data else []
    except Exception as e:
        print(f"Lỗi load phiên gửi xe (xe ra) theo mã thẻ {ma_the}: {str(e)}")
        return []