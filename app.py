import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO
import base64

# --- CẤU HÌNH ---
st.set_page_config(page_title="QR Generator Pro", page_icon="🔥", layout="wide")
st.markdown("""<style>.stButton>button {width: 100%; border-radius: 8px;}</style>""", unsafe_allow_html=True)

# --- HÀM TẠO QR CÓ LOGO ---
def create_qr_with_logo(data, logo_file=None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, # Mức sửa lỗi cao
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

    if logo_file:
        try:
            logo = Image.open(logo_file)
            qr_width, qr_height = img_qr.size
            logo_max_size = int(qr_width * 0.25)
            logo.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
            logo_pos = ((qr_width - logo.size[0]) // 2, (qr_height - logo.size[1]) // 2)
            
            # Tạo viền trắng nhẹ quanh logo
            white_bg_size = (logo.size[0] + 10, logo.size[1] + 10)
            white_bg = Image.new("RGBA", white_bg_size, "WHITE")
            white_bg_pos = (logo_pos[0] - 5, logo_pos[1] - 5)
            
            img_qr.paste(white_bg, white_bg_pos) # Dán nền trắng
            img_qr.paste(logo, logo_pos, mask=logo if logo.mode == 'RGBA' else None) # Dán logo
            
        except Exception as e:
            st.error(f"Lỗi tải logo: {e}")
    return img_qr

def get_download_link(img, filename, label):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a href="data:file/png;base64,{img_str}" download="{filename}" style="text-decoration:none;background:#10b981;color:white;padding:10px 20px;border-radius:8px;display:block;text-align:center;">📥 {label}</a>'

# --- MENU ---
with st.sidebar:
    st.title("QR-Python Pro")
    menu = st.radio("Chọn công cụ:", ["Danh bạ", "URL", "Wifi", "Văn bản"])

# 1. DANH BẠ (Đã cập nhật đầy đủ trường)
if menu == "Danh bạ":
    st.header("📇 Tạo QR Danh bạ")
    col1, col2 = st.columns(2)
    with col1:
        ln = st.text_input("Họ", "Nguyễn")
        fn = st.text_input("Tên *", "Văn A")
        org = st.text_input("Công ty")
        title = st.text_input("Chức danh")
    with col2:
        ph = st.text_input("Số điện thoại", "09xxx")
        em = st.text_input("Email")
        addr = st.text_input("Địa chỉ")
        web = st.text_input("Website")
    
    logo = st.file_uploader("Chọn Logo (nếu muốn)", type=['png', 'jpg', 'jpeg'], key="logo_vcard")
    
    if st.button("Tạo QR"):
        if not fn: st.error("Thiếu tên!")
        else:
            # Tạo chuỗi vCard đầy đủ
            vcard = f"""BEGIN:VCARD
VERSION:3.0
N;CHARSET=UTF-8:{ln};{fn};;;
FN;CHARSET=UTF-8:{fn} {ln}
ORG;CHARSET=UTF-8:{org}
TITLE;CHARSET=UTF-8:{title}
TEL;TYPE=CELL:{ph}
EMAIL:{em}
ADR;TYPE=WORK;CHARSET=UTF-8:;;{addr};;;;
URL:{web}
END:VCARD"""
            
            img = create_qr_with_logo(vcard, logo)
            st.image(img, width=300)
            st.markdown(get_download_link(img, "contact.png", "Tải về"), unsafe_allow_html=True)

# 2. URL
elif menu == "URL":
    st.header("🔗 Tạo QR URL")
    url = st.text_input("Đường dẫn *", "https://google.com")
    logo = st.file_uploader("Chọn Logo", type=['png', 'jpg'], key="logo_url")
    if st.button("Tạo QR"):
        if not url: st.error("Thiếu URL!")
        else:
            img = create_qr_with_logo(url, logo)
            st.image(img, width=300)
            st.markdown(get_download_link(img, "url-qr.png", "Tải về"), unsafe_allow_html=True)

# 3. WIFI
elif menu == "Wifi":
    st.header("📶 Tạo QR Wifi")
    ssid = st.text_input("Tên Wifi *")
    pw = st.text_input("Mật khẩu")
    enc = st.selectbox("Loại", ["WPA", "nopass"])
    logo = st.file_uploader("Chọn Logo", type=['png', 'jpg'], key="logo_wifi")
    if st.button("Tạo QR"):
        if not ssid: st.error("Thiếu SSID!")
        else:
            s = f"WIFI:T:{enc};S:{ssid};"
            if enc != "nopass": s += f"P:{pw};"
            s += ";"
            img = create_qr_with_logo(s, logo)
            st.image(img, width=300)
            st.markdown(get_download_link(img, "wifi.png", "Tải về"), unsafe_allow_html=True)

# 4. VĂN BẢN
elif menu == "Văn bản":
    st.header("📝 Tạo QR Văn bản")
    txt = st.text_area("Nội dung")
    logo = st.file_uploader("Chọn Logo", type=['png', 'jpg'], key="logo_txt")
    if st.button("Tạo QR"):
        if not txt: st.error("Thiếu nội dung!")
        else:
            img = create_qr_with_logo(txt, logo)
            st.image(img, width=300)
            st.markdown(get_download_link(img, "text.png", "Tải về"), unsafe_allow_html=True)