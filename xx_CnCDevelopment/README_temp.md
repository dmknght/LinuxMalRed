# 4. Remote Module Execution – Khái niệm cho C2 Framework
## 4.1. Tại sao C2 không gửi toàn bộ code xuống Client?
- Giảm footprint: ít code trên client → khó bị phân tích.
- Linh hoạt: module nào cần mới gửi.
- Stealth: network traffic nhỏ.
- Cập nhật nhanh module từ server.

Nhược điểm:
- Phụ thuộc vào kết nối.
- Tăng rủi ro detection từ IDS nếu module tải nhiều lần.
- Cần cơ chế ký hoặc mã hóa module để tránh bị giả mạo.

## 4.2. Concept:
- Bytecode
- gRPC
- dynamic execution

## 4.3 Example:
- Python: importlib, bytecode (disam)
- C/Cpp: send dll, use dynload


Code maintainability và modularity.

Documentation cho internal tools

Protocol Obfuscation: Sử dụng các giao thức hợp lệ để blend-in (DNS, ICMP, HTTP/3).

Domain Fronting & CDN Abuse: Ẩn C2 traffic sau các dịch vụ hợp pháp.

Malleable C2 Profiles: Tùy chỉnh C2 behavior để match với traffic pattern của target.

Fallback Channels: Luôn có multiple communication channels (email, cloud storage, social media APIs).

encrypt, evasion
modular

TODO các thành phần chính:
- listener
- cli (control)
- Frameowrk controller: core
- Modules
- Team server

TODO: lựa chọn ngôn ngữ viết client, ưu nhược điểm (base trên tính sẵn sàng, module, ..., và cả remote module execution)