import streamlit as st
st.image("logo.jpg")
# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 APP TÍNH LÃI GỬI TIẾT KIỆM tại NY bank")
st.write("Tính tiền lãi theo phương pháp **lãi đơn** hoặc **lãi kép**.")

st.divider()

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📌 Thông tin khoản gửi")

tien_gui = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10000000.0,
    step=100000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1
)

loai_lai = st.selectbox(
    "🔢 Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_lanh = st.selectbox(
    "💳 Hình thức lãnh lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

# =========================
# NÚT TÍNH
# =========================
st.divider()

if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    r_nam = lai_suat / 100

    # Thời gian tính theo năm
    so_nam = ky_han / 12

    # Lãi suất theo tháng
    r_thang = r_nam / 12

    # =========================
    # LÃI ĐƠN
    # =========================
    if loai_lai == "Lãi đơn":

        # Tổng tiền lãi
        tong_lai = tien_gui * r_nam * so_nam

        # Tổng gốc + lãi
        tong_tien = tien_gui + tong_lai

        # =========================
        # LÃI ĐỊNH KỲ
        # =========================

        if hinh_thuc_lanh == "Lãnh lãi theo tháng":
            lai_dinh_ky = tien_gui * r_thang
            so_ky = ky_han

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":
            lai_dinh_ky = tien_gui * r_thang * 3
            so_ky = ky_han / 3

        else:
            lai_dinh_ky = tong_lai
            so_ky = 1

    # =========================
    # LÃI KÉP
    # =========================
    else:

        # Lãi kép được tính theo tháng
        # Mỗi tháng tiền lãi được nhập vào gốc
        so_thang = ky_han

        tong_tien = tien_gui * ((1 + r_thang) ** so_thang)

        tong_lai = tong_tien - tien_gui

        # =========================
        # LÃI ĐỊNH KỲ
        # =========================

        if hinh_thuc_lanh == "Lãnh lãi theo tháng":

            lai_dinh_ky = None
            so_ky = so_thang

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":

            lai_dinh_ky = None
            so_ky = ky_han / 3

        else:

            lai_dinh_ky = tong_lai
            so_ky = 1

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("✅ Tính toán hoàn tất!")

    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Số tiền gốc",
            format_money(tien_gui)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_lai)
        )

    st.metric(
        "💰 Tổng tiền nhận được",
        format_money(tong_tien)
    )

    st.divider()

    # =========================
    # TIỀN LÃI ĐỊNH KỲ
    # =========================

    st.subheader("💳 Tiền lãi định kỳ")

    if loai_lai == "Lãi đơn":

        if hinh_thuc_lanh == "Lãnh lãi theo tháng":

            st.info(
                f"Tiền lãi mỗi tháng: **{format_money(lai_dinh_ky)}**"
            )

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":

            st.info(
                f"Tiền lãi mỗi quý: **{format_money(lai_dinh_ky)}**"
            )

        else:

            st.info(
                f"Tiền lãi cuối kỳ: **{format_money(lai_dinh_ky)}**"
            )

    else:

        if hinh_thuc_lanh == "Lãnh lãi theo tháng":

            st.info(
                "Với **lãi kép**, tiền lãi được cộng vào vốn mỗi tháng "
                "nên tiền lãi của mỗi tháng sẽ thay đổi."
            )

            # Hiển thị tiền lãi tháng đầu tiên
            lai_thang_dau = tien_gui * r_thang

            st.write(
                f"Tiền lãi tháng đầu tiên: "
                f"**{format_money(lai_thang_dau)}**"
            )

            # Tiền lãi tháng cuối
            tien_truoc_thang_cuoi = tien_gui * (
                (1 + r_thang) ** (so_thang - 1)
            )

            lai_thang_cuoi = tien_truoc_thang_cuoi * r_thang

            st.write(
                f"Tiền lãi tháng cuối: "
                f"**{format_money(lai_thang_cuoi)}**"
            )

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":

            st.info(
                "Với **lãi kép**, tiền lãi mỗi quý thay đổi "
                "do tiền lãi được cộng dồn vào vốn."
            )

            lai_quy_dau = tien_gui * (
                (1 + r_thang) ** 3 - 1
            )

            st.write(
                f"Tiền lãi quý đầu tiên: "
                f"**{format_money(lai_quy_dau)}**"
            )

            if ky_han >= 3:
                so_quy = int(ky_han // 3)

                tien_dau_quy_cuoi = tien_gui * (
                    (1 + r_thang) ** ((so_quy - 1) * 3)
                )

                lai_quy_cuoi = tien_dau_quy_cuoi * (
                    (1 + r_thang) ** 3 - 1
                )

                st.write(
                    f"Tiền lãi quý cuối: "
                    f"**{format_money(lai_quy_cuoi)}**"
                )

        else:

            st.info(
                f"Tiền lãi nhận cuối kỳ: "
                f"**{format_money(tong_lai)}**"
            )

    # =========================
    # TÓM TẮT
    # =========================
    st.divider()

    st.subheader("📋 Tóm tắt khoản gửi")

    st.write(f"**Số tiền gửi:** {format_money(tien_gui)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức tính:** {loai_lai}")
    st.write(f"**Hình thức lãnh:** {hinh_thuc_lanh}")
    st.write(f"**Tổng tiền lãi:** {format_money(tong_lai)}")
    st.write(f"**Tổng gốc + lãi:** {format_money(tong_tien)}")


# =========================
# GHI CHÚ
# =========================
st.divider()

with st.expander("ℹ️ Công thức tính"):
    st.markdown("""
    **Lãi đơn:**

    Tiền lãi = Tiền gốc × Lãi suất năm × Số năm

    **Lãi kép:**

    Tổng tiền = Tiền gốc × (1 + Lãi suất tháng)^(Số tháng)

    **Lưu ý:** App giả định lãi suất không đổi trong toàn bộ kỳ hạn 
    và lãi kép được nhập gốc hàng tháng.
    """)
