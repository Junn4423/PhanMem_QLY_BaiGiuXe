-- Cấu trúc bảng cho bảng `pm_nc0009`
--

DROP TABLE IF EXISTS `pm_nc0009`;
CREATE TABLE IF NOT EXISTS `pm_nc0009` (
  `lv001` int(11) NOT NULL AUTO_INCREMENT,
  `lv002` varchar(100) NOT NULL COMMENT 'UID thẻ (FK → pm_nc0003.lv001)',
  `lv003` varchar(20) NOT NULL COMMENT 'Biển số (FK → pm_nc0002.lv001)',
  `lv004` varchar(20) DEFAULT NULL COMMENT 'Mã vị trí gửi (FK → pm_nc0005.lv001)',
  `lv005` varchar(20) DEFAULT NULL COMMENT 'Mã chính sách giá (FK → pm_nc0008.lv001)',
  `lv006` varchar(20) DEFAULT NULL COMMENT 'Mã cổng vào (FK → pm_nc0007.lv001)',
  `lv007` varchar(20) DEFAULT NULL COMMENT 'Mã cổng ra (FK → pm_nc0007.lv001)',
  `lv008` datetime NOT NULL COMMENT 'Thời gian vào',
  `lv009` datetime DEFAULT NULL COMMENT 'Thời gian ra',
  `lv010` int(11) DEFAULT NULL COMMENT 'Tổng phút gửi',
  `lv011` varchar(255) NOT NULL COMMENT 'Ảnh biển số lúc vào',
  `lv012` varchar(255) DEFAULT NULL COMMENT 'Ảnh biển số lúc ra',
  `lv013` decimal(12,2) DEFAULT NULL COMMENT 'Phí tính được',
  `lv014` enum('DANG_GUI','DA_RA') NOT NULL DEFAULT 'DANG_GUI' COMMENT 'Trạng thái phiên',
  `lv015` varchar(255) DEFAULT NULL COMMENT 'Ảnh khuôn mặt người gửi lúc vào',
  `lv016` varchar(255) DEFAULT NULL COMMENT 'Ảnh khuôn mặt người gửi lúc ra',
  PRIMARY KEY (`lv001`),
  KEY `fk_pn9_the` (`lv002`),
  KEY `fk_pn9_xe` (`lv003`),
  KEY `fk_pn9_vtri` (`lv004`),
  KEY `fk_pn9_cs` (`lv005`),
  KEY `fk_pn9_cong_vao` (`lv006`),
  KEY `fk_pn9_cong_ra` (`lv007`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Lưu trữ phiên gửi/ra xe'; 