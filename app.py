import streamlit as st
st.image("logo.jpg")
# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==============================
# TIÊU ĐỀ
# ==============================
st.title("💰 APP TÍNH LÃI TIỀN GỬI TIẾT KIỆM- Phạm Thị Vũ Ngọc Yến")
st.write(
    "Tính toán tiền lãi theo **lãi đơn** hoặc **lãi kép**, "
    "với nhiều hình thức nhận lãi."
)

st.divider()

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# ==============================
# NHẬP THÔNG TIN
# ==============================
st.subheader("📋 Thông tin khoản tiền gửi")

# Số tiền gửi
tien_gui = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

# Kỳ hạn
ky_han = st.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    max_value=1200,
    value=12,
    step=1
)

# Lãi suất
lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1
)

# Loại lãi
loai_lai = st.selectbox(
    "🔢 Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

# Hình thức nhận lãi
hinh_thuc = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.divider()

# ==============================
# NÚT TÍNH TOÁN
# ==============================
if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if tien_gui <= 0:
        st.error("❌ Số tiền gửi phải lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("❌ Lãi suất không được âm.")
        st.stop()

    # Chuyển lãi suất % sang số thập phân
    r = lai_suat / 100

    # Kỳ hạn tính theo năm
    so_nam = ky_han / 12

    # ==============================
    # LÃI ĐƠN
    # ==============================
    if loai_lai == "Lãi đơn":

        # Tổng tiền lãi
        tong_lai = tien_gui * r * so_nam

        # Tổng cả gốc và lãi
        tong_tien = tien_gui + tong_lai

        # Tiền lãi định kỳ
        if hinh_thuc == "Lãnh lãi hàng tháng":
            lai_dinh_ky = tien_gui * r / 12

        elif hinh_thuc == "Lãnh lãi hàng quý":
            lai_dinh_ky = tien_gui * r / 4

        else:
            lai_dinh_ky = tong_lai

    # ==============================
    # LÃI KÉP
    # ==============================
    else:

        # Xác định số lần nhập lãi trong năm
        if hinh_thuc == "Lãnh lãi hàng tháng":
            so_lan_nhap_lai_nam = 12

        elif hinh_thuc == "Lãnh lãi hàng quý":
            so_lan_nhap_lai_nam = 4

        else:
            so_lan_nhap_lai_nam = 1

        # Tổng số kỳ nhập lãi
        so_ky = ky_han / (12 / so_lan_nhap_lai_nam)

        # Lãi suất mỗi kỳ
        lai_suat_ky = r / so_lan_nhap_lai_nam

        # Tổng tiền cuối kỳ
        tong_tien = tien_gui * (
            (1 + lai_suat_ky) ** so_ky
        )

        # Tổng tiền lãi
        tong_lai = tong_tien - tien_gui

        # Tiền lãi định kỳ
        if hinh_thuc == "Lãnh lãi hàng tháng":
            lai_dinh_ky = tien_gui * lai_suat_ky

        elif hinh_thuc == "Lãnh lãi hàng quý":
            lai_dinh_ky = tien_gui * lai_suat_ky

        else:
            lai_dinh_ky = tong_lai

    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================
    st.success("✅ Tính toán thành công!")

    st.subheader("📊 KẾT QUẢ")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_lai)
        )

    with col2:
        st.metric(
            "🏦 Tiền gốc",
            format_money(tien_gui)
        )

        st.metric(
            "💰 Tổng gốc + lãi",
            format_money(tong_tien)
        )

    st.divider()

    # ==============================
    # THÔNG TIN KHOẢN GỬI
    # ==============================
    st.subheader("📋 Thông tin khoản gửi")

    st.write(f"**Số tiền gửi:** {format_money(tien_gui)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Phương pháp:** {loai_lai}")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")

    # ==============================
    # CÔNG THỨC
    # ==============================
    with st.expander("📚 Xem công thức tính"):

        if loai_lai == "Lãi đơn":

            st.markdown("### Lãi đơn")

            st.latex(
                r"I = P \times r \times t"
            )

            st.write(
                "Trong đó:"
            )
            st.write("• P: Số tiền gốc")
            st.write("• r: Lãi suất năm")
            st.write("• t: Thời gian gửi tính theo năm")
            st.write("• I: Tổng tiền lãi")

        else:

            st.markdown("### Lãi kép")

            st.latex(
                r"A = P(1+r)^n"
            )

            st.write(
                "Trong đó:"
            )
            st.write("• P: Số tiền gốc")
            st.write("• r: Lãi suất mỗi kỳ")
            st.write("• n: Số kỳ nhập lãi")
            st.write("• A: Tổng số tiền nhận được")

# ==============================
# FOOTER
# ==============================
st.divider()

st.caption(
    "💡 Công cụ tính toán mang tính tham khảo. "
    "Lãi suất thực tế có thể phụ thuộc vào chính sách của từng ngân hàng."
)
