import streamlit as st
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================

st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# LOGO
# =========================

try:
    st.image("logo.jpg", width=200)
except:
    pass

# =========================
# TIÊU ĐỀ
# =========================

st.title("💰 APP TÍNH LÃI GỬI TIẾT KIỆM")
st.subheader("👩‍💻 Phạm Thị Vũ Ngọc Yến")

st.write(
    "Tính tiền lãi theo phương pháp **lãi đơn**, "
    "**lãi kép** và **gửi tiết kiệm định kỳ hàng tháng**."
)

st.divider()


# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================

def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================================================
# PHẦN 1: TÍNH LÃI KHOẢN GỬI BAN ĐẦU
# =========================================================

st.header("💰 1. Tính lãi khoản gửi")

st.subheader("📌 Thông tin khoản gửi")

tien_gui = st.number_input(
    "💵 Số tiền gửi ban đầu (VNĐ)",
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

st.divider()

# =========================
# NÚT TÍNH LÃI
# =========================

if st.button(
    "🧮 TÍNH LÃI",
    use_container_width=True
):

    if tien_gui <= 0:
        st.error("❌ Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    # Lãi suất
    r_nam = lai_suat / 100

    # Số năm
    so_nam = ky_han / 12

    # Lãi suất tháng
    r_thang = r_nam / 12

    # =====================================================
    # LÃI ĐƠN
    # =====================================================

    if loai_lai == "Lãi đơn":

        tong_lai = tien_gui * r_nam * so_nam

        tong_tien = tien_gui + tong_lai

        if hinh_thuc_lanh == "Lãnh lãi theo tháng":

            lai_dinh_ky = tien_gui * r_thang

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":

            lai_dinh_ky = tien_gui * r_thang * 3

        else:

            lai_dinh_ky = tong_lai

    # =====================================================
    # LÃI KÉP
    # =====================================================

    else:

        so_thang = ky_han

        tong_tien = tien_gui * (
            (1 + r_thang) ** so_thang
        )

        tong_lai = tong_tien - tien_gui

        if hinh_thuc_lanh == "Lãnh lãi cuối kỳ":

            lai_dinh_ky = tong_lai

        else:

            lai_dinh_ky = None

    # =====================================================
    # HIỂN THỊ KẾT QUẢ
    # =====================================================

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

    # =====================================================
    # TIỀN LÃI ĐỊNH KỲ
    # =====================================================

    st.subheader("💳 Tiền lãi định kỳ")

    if loai_lai == "Lãi đơn":

        if hinh_thuc_lanh == "Lãnh lãi theo tháng":

            st.info(
                f"Tiền lãi mỗi tháng: "
                f"**{format_money(lai_dinh_ky)}**"
            )

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":

            st.info(
                f"Tiền lãi mỗi quý: "
                f"**{format_money(lai_dinh_ky)}**"
            )

        else:

            st.info(
                f"Tiền lãi cuối kỳ: "
                f"**{format_money(lai_dinh_ky)}**"
            )

    else:

        if hinh_thuc_lanh == "Lãnh lãi theo tháng":

            lai_thang_dau = tien_gui * r_thang

            tien_truoc_thang_cuoi = tien_gui * (
                (1 + r_thang) ** (ky_han - 1)
            )

            lai_thang_cuoi = (
                tien_truoc_thang_cuoi * r_thang
            )

            st.info(
                "Với **lãi kép**, tiền lãi được cộng vào vốn "
                "mỗi tháng nên tiền lãi thay đổi theo thời gian."
            )

            st.write(
                f"💵 Tiền lãi tháng đầu tiên: "
                f"**{format_money(lai_thang_dau)}**"
            )

            st.write(
                f"💵 Tiền lãi tháng cuối: "
                f"**{format_money(lai_thang_cuoi)}**"
            )

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":

            if ky_han >= 3:

                lai_quy_dau = tien_gui * (
                    (1 + r_thang) ** 3 - 1
                )

                so_quy = ky_han // 3

                tien_dau_quy_cuoi = tien_gui * (
                    (1 + r_thang) ** ((so_quy - 1) * 3)
                )

                lai_quy_cuoi = tien_dau_quy_cuoi * (
                    (1 + r_thang) ** 3 - 1
                )

                st.info(
                    "Với **lãi kép**, tiền lãi mỗi quý "
                    "thay đổi do tiền lãi được cộng dồn."
                )

                st.write(
                    f"💵 Tiền lãi quý đầu tiên: "
                    f"**{format_money(lai_quy_dau)}**"
                )

                st.write(
                    f"💵 Tiền lãi quý cuối: "
                    f"**{format_money(lai_quy_cuoi)}**"
                )

            else:

                st.warning(
                    "Kỳ hạn chưa đủ 3 tháng để tính lãi theo quý."
                )

        else:

            st.info(
                f"Tiền lãi nhận cuối kỳ: "
                f"**{format_money(tong_lai)}**"
            )

    # =====================================================
    # TÓM TẮT
    # =====================================================

    st.divider()

    st.subheader("📋 Tóm tắt khoản gửi")

    st.write(
        f"**Số tiền gửi:** {format_money(tien_gui)}"
    )

    st.write(
        f"**Kỳ hạn:** {ky_han} tháng"
    )

    st.write(
        f"**Lãi suất:** {lai_suat:.2f}%/năm"
    )

    st.write(
        f"**Hình thức tính:** {loai_lai}"
    )

    st.write(
        f"**Hình thức lãnh:** {hinh_thuc_lanh}"
    )

    st.write(
        f"**Tổng tiền lãi:** {format_money(tong_lai)}"
    )

    st.write(
        f"**Tổng gốc + lãi:** {format_money(tong_tien)}"
    )


# =========================================================
# PHẦN 2: GỬI TIẾT KIỆM ĐỊNH KỲ HÀNG THÁNG
# =========================================================

st.divider()

st.header("⭐ 2. Gửi tiết kiệm định kỳ hàng tháng")

st.write(
    "Tính số tiền nhận được khi bạn gửi thêm "
    "một khoản tiền cố định vào mỗi tháng."
)

# =========================
# NHẬP THÔNG TIN
# =========================

tien_gui_thang = st.number_input(
    "💵 Số tiền gửi thêm mỗi tháng (VNĐ)",
    min_value=0.0,
    value=1000000.0,
    step=100000.0,
    format="%.0f"
)

ky_han_dinh_ky = st.number_input(
    "📅 Thời gian gửi định kỳ (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

lai_suat_dinh_ky = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1
)

loai_dinh_ky = st.selectbox(
    "🔢 Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ],
    key="loai_dinh_ky"
)

# =========================
# TÍNH ĐỊNH KỲ
# =========================

if st.button(
    "🧮 TÍNH TIỀN GỬI ĐỊNH KỲ",
    use_container_width=True
):

    if tien_gui_thang <= 0:

        st.error(
            "❌ Vui lòng nhập số tiền gửi mỗi tháng lớn hơn 0."
        )

    else:

        # Lãi suất tháng
        r_thang_dinh_ky = (
            lai_suat_dinh_ky / 100 / 12
        )

        danh_sach = []

        # =================================================
        # LÃI ĐƠN
        # =================================================

        if loai_dinh_ky == "Lãi đơn":

            tong_goc = 0
            tong_lai_dinh_ky = 0

            for thang in range(
                1,
                ky_han_dinh_ky + 1
            ):

                # Gửi tiền mỗi tháng
                tong_goc += tien_gui_thang

                # Số tháng khoản tiền này được sinh lãi
                so_thang_sinh_lai = (
                    ky_han_dinh_ky - thang + 1
                )

                lai_khoan_nay = (
                    tien_gui_thang
                    * r_thang_dinh_ky
                    * so_thang_sinh_lai
                )

                tong_lai_dinh_ky += lai_khoan_nay

                tong_tien = (
                    tong_goc
                    + tong_lai_dinh_ky
                )

                danh_sach.append({
                    "Tháng": thang,
                    "Tiền đã gửi": tong_goc,
                    "Tiền lãi": tong_lai_dinh_ky,
                    "Tổng tiền": tong_tien
                })

        # =================================================
        # LÃI KÉP
        # =================================================

        else:

            tong_tien = 0

            for thang in range(
                1,
                ky_han_dinh_ky + 1
            ):

                # Tiền cũ sinh lãi
                tong_tien = (
                    tong_tien
                    * (1 + r_thang_dinh_ky)
                )

                # Gửi thêm tiền vào cuối tháng
                tong_tien += tien_gui_thang

                tong_goc = (
                    tien_gui_thang * thang
                )

                tong_lai_dinh_ky = (
                    tong_tien - tong_goc
                )

                danh_sach.append({
                    "Tháng": thang,
                    "Tiền đã gửi": tong_goc,
                    "Tiền lãi": tong_lai_dinh_ky,
                    "Tổng tiền": tong_tien
                })

        # =================================================
        # DATAFRAME
        # =================================================

        df_dinh_ky = pd.DataFrame(
            danh_sach
        )

        tong_goc_cuoi = (
            tien_gui_thang
            * ky_han_dinh_ky
        )

        tong_lai_cuoi = (
            df_dinh_ky.iloc[-1]["Tiền lãi"]
        )

        tong_tien_cuoi = (
            df_dinh_ky.iloc[-1]["Tổng tiền"]
        )

        # =================================================
        # KẾT QUẢ
        # =================================================

        st.success(
            "✅ Tính toán gửi định kỳ hoàn tất!"
        )

        st.subheader("📊 Kết quả gửi định kỳ")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "💵 Tổng tiền đã gửi",
                format_money(tong_goc_cuoi)
            )

        with col2:

            st.metric(
                "📈 Tổng tiền lãi",
                format_money(tong_lai_cuoi)
            )

        st.metric(
            "💰 Tổng tiền nhận được",
            format_money(tong_tien_cuoi)
        )

        # =================================================
        # BẢNG CHI TIẾT
        # =================================================

        st.divider()

        st.subheader(
            "📋 Chi tiết khoản tiền theo từng tháng"
        )

        df_hien_thi = df_dinh_ky.copy()

        df_hien_thi["Tiền đã gửi"] = (
            df_hien_thi["Tiền đã gửi"]
            .apply(format_money)
        )

        df_hien_thi["Tiền lãi"] = (
            df_hien_thi["Tiền lãi"]
            .apply(format_money)
        )

        df_hien_thi["Tổng tiền"] = (
            df_hien_thi["Tổng tiền"]
            .apply(format_money)
        )

        st.dataframe(
            df_hien_thi,
            use_container_width=True,
            hide_index=True
        )

        # =================================================
        # BIỂU ĐỒ
        # =================================================

        st.subheader(
            "📈 Biểu đồ tăng trưởng khoản tiết kiệm"
        )

        chart_data = df_dinh_ky.set_index(
            "Tháng"
        )[[
            "Tiền đã gửi",
            "Tổng tiền"
        ]]

        st.line_chart(
            chart_data
        )

        # =================================================
        # NHẬN XÉT
        # =================================================

        st.divider()

        st.subheader("💡 Nhận xét")

        st.info(
            f"Bạn gửi thêm **{format_money(tien_gui_thang)} "
            f"mỗi tháng** trong **{ky_han_dinh_ky} tháng**. "
            f"Tổng số tiền bạn đã gửi là "
            f"**{format_money(tong_goc_cuoi)}**. "
            f"Tiền lãi dự kiến là "
            f"**{format_money(tong_lai_cuoi)}**. "
            f"Tổng số tiền cuối kỳ là "
            f"**{format_money(tong_tien_cuoi)}**."
        )


# =========================================================
# PHẦN 3: CÔNG THỨC
# =========================================================

st.divider()

with st.expander("ℹ️ Công thức tính"):

    st.markdown("""
    ### 1. Lãi đơn

    **Tiền lãi = Tiền gốc × Lãi suất năm × Số năm**

    **Tổng tiền = Tiền gốc + Tiền lãi**

    ---

    ### 2. Lãi kép

    **Tổng tiền = Tiền gốc × (1 + Lãi suất tháng)^Số tháng**

    **Tiền lãi = Tổng tiền - Tiền gốc**

    ---

    ### 3. Gửi tiết kiệm định kỳ

    Mỗi tháng người dùng gửi thêm một khoản tiền cố định.

    Với **lãi kép**, tiền của các tháng trước tiếp tục
    sinh lãi và được cộng dồn vào số dư.

    **Lưu ý:** App giả định khoản tiền được gửi thêm
    vào **cuối mỗi tháng** và lãi suất không thay đổi
    trong toàn bộ thời gian gửi.
    """)


# =========================================================
# CHÂN TRANG
# =========================================================

st.divider()

st.caption(
    "💰 App tính lãi gửi tiết kiệm | "
    "Phạm Thị Vũ Ngọc Yến"
)
