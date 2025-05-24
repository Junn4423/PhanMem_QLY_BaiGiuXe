<html>
  <div id="top">
<div align="center">
  <h1>PHANMEM_QLY_BAIGIUXE</h1>
  <p><em>Automating Parking Management with Python, Computer Vision, and RFID</em></p>

  <img alt="last-commit" src="https://img.shields.io/github/last-commit/Junn4423/PhanMem_QLY_BaiGiuXe?style=flat&logo=git&logoColor=white&color=0080ff" class="inline-block mx-1" />
  <img alt="repo-top-language" src="https://img.shields.io/github/languages/top/Junn4423/PhanMem_QLY_BaiGiuXe?style=flat&color=0080ff" class="inline-block mx-1" />
  <img alt="repo-language-count" src="https://img.shields.io/github/languages/count/Junn4423/PhanMem_QLY_BaiGiuXe?style=flat&color=0080ff" class="inline-block mx-1" />

  <p><em>Built with:</em></p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=python&logoColor=white" class="inline-block mx-1" />
  <img alt="Tkinter" src="https://img.shields.io/badge/Tkinter-339933.svg?style=flat&logo=python&logoColor=white" class="inline-block mx-1" />
  <img alt="MySQL" src="https://img.shields.io/badge/MySQL-4479A1.svg?style=flat&logo=mysql&logoColor=white" class="inline-block mx-1" />
  <img alt="Pydantic" src="https://img.shields.io/badge/Pydantic-00C4CC.svg?style=flat&logo=pydantic&logoColor=white" class="inline-block mx-1" />
  <img alt="Requests" src="https://img.shields.io/badge/Requests-000000.svg?style=flat&logo=requests&logoColor=white" class="inline-block mx-1" />
</div>
<br>
<hr>

<h2>Table of Contents</h2>
<ul class="list-disc pl-4">
  <li><a href="#overview">Overview</a></li>
  <li><a href="#system-architecture">System Architecture</a></li>
  <li><a href="#hardware-integration">Hardware Integration</a></li>
  <li><a href="#core-components">Core Components</a></li>
  <li><a href="#user-interface">User Interface</a></li>
  <li><a href="#vehicle-management">Vehicle Management</a></li>
  <li><a href="#authentication-system">Authentication System</a></li>
  <li><a href="#data-layer">Data Layer</a></li>
  <li><a href="#data-models">Data Models</a></li>
  <li><a href="#api-interface">API Interface</a></li>
  <li><a href="#configuration-setup">Configuration &amp; Setup</a></li>
  <li><a href="#server-components">Server Components</a></li>
  <li><a href="#assets-resources">Assets &amp; Resources</a></li>
</ul>
<hr>

## Overview
PhanMem_QLY_BaiGiuXe is a Python-based parking management system integrating EZVIZ cameras, RFID readers, and license-plate OCR into a unified Tkinter GUI with MySQL persistence.

## System Architecture
- **Entry Point**: `main.py` orchestrates dependency checks (`kiem_tra_va_cai_dat_goi()`), component instantiation, and threading models :contentReference[oaicite:7]{index=7}.  
- **Concurrency**: UI runs on the main thread; camera and reader components each use daemon threads to avoid blocking :contentReference[oaicite:8]{index=8}.  
- **Data Flow**: Hardware events → `QuanLyXe` business logic → API calls → database persistence → UI updates :contentReference[oaicite:9]{index=9}.

## Hardware Integration
- **EZVIZ Cameras** (`QuanLyCamera`): RTSP stream processing at 30 FPS, image capture, OCR API integration :contentReference[oaicite:10]{index=10}.  
- **Card/RFID Readers** (`DauDocThe`): Keyboard-simulated input handling, buffer accumulation and Enter-key triggers :contentReference[oaicite:11]{index=11}.  
- **Configuration**: Zone-based mappings for cameras and gates loaded from JSON and server module :contentReference[oaicite:12]{index=12}.  

## Core Components
- **UI Controller**: `GiaoDienQuanLyBaiXe` manages window layout, tabbed interface, and mode switching :contentReference[oaicite:13]{index=13}.  
- **Vehicle Logic**: `QuanLyXe` controls session workflows (`xu_ly_xe_vao`/`xu_ly_xe_ra`), policy selection, and error handling :contentReference[oaicite:14]{index=14}.  
- **Authentication**: `EnhancedLoginDialog` enforces a login dialog before main app access :contentReference[oaicite:15]{index=15}.

## User Interface
- **Framework**: Tkinter with `ttk.Notebook` for tabs; real-time camera feeds and status updates via `root.after()` :contentReference[oaicite:16]{index=16}.  
- **Tabs**:  
  - *Vehicle Management*: Live feeds, captured images, entry/exit controls.  
  - *Vehicle List*: Search/filter, statistics cards, and data table.  
- **Controls**: Buttons switch modes (`xe_may`, `oto`, `vao`, `ra`) and reset scanning state :contentReference[oaicite:17]{index=17}.

## Vehicle Management
- **Entry Workflow**: RFID scan → `chup_anh()` → `PhienGuiXe` creation → API `themPhienGuiXe()` :contentReference[oaicite:18]{index=18}.  
- **Exit Workflow**: Plate validation → fee calculation → session update via `capNhatPhienGuiXe()` :contentReference[oaicite:19]{index=19}.  
- **UI Callbacks**: Real-time status (`cap_nhat_trang_thai_xe_vao/ra`) for user feedback :contentReference[oaicite:20]{index=20}.

## Authentication System
- **Dialog**: `EnhancedLoginDialog` extends `simpledialog.Dialog`, with hard-coded `admin/1` credentials and retry logic :contentReference[oaicite:21]{index=21}.  
- **Security Note**: Placeholder implementation; consider secure stores, hashing, and multi-user support :contentReference[oaicite:22]{index=22}.

## Data Layer
- **Pydantic Models**: Type-safe entities (`LoaiPhuongTien`, `PhuongTien`, `TheRFID`, `KhuVuc`, `ChoDo`, `PhienGuiXe`, `NhatKyGuiXe`) :contentReference[oaicite:23]{index=23}.  
- **API**: HTTP POST–based CRUD (`pm_nc0001`, `pm_nc0009`, zone retrieval) with error handling via `res.raise_for_status()` and JSON success flags :contentReference[oaicite:24]{index=24}.

## Data Models
- **Vehicle Types** (`LoaiPhuongTien`), **Vehicles** (`PhuongTien`), **RFID Cards** (`TheRFID`) :contentReference[oaicite:25]{index=25}.  
- **Sessions** (`PhienGuiXe`): Entry/exit timestamps, images, durations, fees :contentReference[oaicite:26]{index=26}.  
- **Audit Logs** (`NhatKyGuiXe`): Event tracking for entry/exit actions :contentReference[oaicite:27]{index=27}.

## API Interface
- **Pattern**: Table–function JSON payloads for all operations :contentReference[oaicite:28]{index=28}.  
- **Functions**:  
  - Vehicle types: `layALLLoaiPhuongTien`, `themLoaiPhuongTien`, etc.  
  - Sessions: `layALLPhienGuiXe`, `themPhienGuiXe`, `capNhatPhienGuiXe`, `loadPhienGuiXeTheoMaThe`.  
  - Zones: `lay_danh_sach_khu` for camera/gate mappings.

## Configuration &amp; Setup
- **Database**: `server/config/db_config.json` with host, user, pass, database `PM`, port 3306 :contentReference[oaicite:29]{index=29}.  
- **RTSP**: EZVIZ URL format `rtsp://user:pass@[IP]:554/h264/ch1/main/av_stream` :contentReference[oaicite:30]{index=30}.  
- **APIs**: OCR at `api_BienSo`, data services at `url_api` constants :contentReference[oaicite:31]{index=31}.  
- **Env**: Python 3.13, VS Code settings to include `server` in analysis paths :contentReference[oaicite:32]{index=32}.

## Server Components
- **Structure**: `server/` package with `data/vehicles.json` for JSON-based storage and `api.py` for HTTP interfaces :contentReference[oaicite:33]{index=33}.  
- **Modularity**: Enables isolated testing and future migration to database systems :contentReference[oaicite:34]{index=34}.

## Assets &amp; Resources
- **Directory**: `assets/` holds `icon.png`, `logo.png`, `sof.png` for GUI branding :contentReference[oaicite:35]{index=35}.  
- **Formats**: 32-bit RGBA PNGs for lossless quality and transparency :contentReference[oaicite:36]{index=36}.  
- **Loading**: Via `PIL.Image.open()` and `ImageTk.PhotoImage()` in Tkinter :contentReference[oaicite:37]{index=37}.

<hr>
<div align="left"><a href="#top">⬆ Return</a></div>
<a href="https://deepwiki.com/Junn4423/PhanMem_QLY_BaiGiuXe"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></a>
</div>
</html>
