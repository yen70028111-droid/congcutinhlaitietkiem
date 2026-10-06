import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# 1. CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# 2. CSS GIAO DIỆN
# =========================================================

st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1677ff;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #666666;
        font-size: 18px;
        margin-bottom: 20px;
    }

    .result-title {
        font-size: 24px;
        font-weight: bold;
    }

    [data-testid="stMetricValue"] {
        font-size: 24px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LOGO
# =========================================================

st.image("logo.jpg", width=200)

# =========================================================
# 4. TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="main-title">💰 APP TÍNH LÃI TIỀN GỬI TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Tính toán lãi đơn, lãi kép và theo dõi tăng trưởng tiền gửi'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# 5. HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def format_money(value):
    return f"{value:,.0f}".replace(",", ".") + " VNĐ"


# =========================================================
# 6. NHẬP THÔNG TIN Ở SIDEBAR
# =========================================================

st.sidebar.title("📋 THÔNG TIN KHOẢN GỬI")

tien_gui = st.sidebar.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=1_000_000.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.sidebar.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    max_value=1200,
    value=12,
    step=1
)

lai_suat = st.sidebar.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1
)

loai_lai = st.sidebar.selectbox(
    "🔢 Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc = st.sidebar.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "💡 Bạn có thể thay đổi các thông tin bên trên "
    "để xem kết quả và biểu đồ được cập nhật tự động."
)

# =========================================================
# 7. XÁC ĐỊNH SỐ KỲ TRONG NĂM
# =========================================================

lai_suat_nam = lai_suat / 100

if hinh_thuc == "Lãnh lãi hàng tháng":
    so_ky_nam = 12

elif hinh_thuc == "Lãnh lãi hàng quý":
    so_ky_nam = 4

else:
    so_ky_nam = 1


# =========================================================
# 8. TÍNH LÃI
# =========================================================

if loai_lai == "Lãi đơn":

    # Tổng tiền lãi
    tong_lai = tien_gui * lai_suat_nam * (ky_han / 12)

    # Tổng gốc + lãi
    tong_tien = tien_gui + tong_lai

    # Tiền lãi định kỳ
    if hinh_thuc == "Lãnh lãi hàng tháng":

        lai_dinh_ky = tien_gui * lai_suat_nam / 12

    elif hinh_thuc == "Lãnh lãi hàng quý":

        lai_dinh_ky = tien_gui * lai_suat_nam / 4

    else:

        lai_dinh_ky = tong_lai


else:

    # Lãi suất theo kỳ
    lai_suat_ky = lai_suat_nam / so_ky_nam

    # Số kỳ
    so_ky = ky_han / (12 / so_ky_nam)

    # Tổng tiền cuối kỳ
    tong_tien = tien_gui * (
        (1 + lai_suat_ky) ** so_ky
    )

    # Tổng tiền lãi
    tong_lai = tong_tien - tien_gui

    # Lãi định kỳ
    if hinh_thuc == "Lãnh lãi cuối kỳ":

        lai_dinh_ky = tong_lai

    else:

        lai_dinh_ky = tien_gui * lai_suat_ky


# =========================================================
# 9. HIỂN THỊ KẾT QUẢ
# =========================================================

st.subheader("📊 KẾT QUẢ TÍNH TOÁN")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💵 Tiền gốc",
        format_money(tien_gui)
    )

with col2:
    st.metric(
        "💰 Tiền lãi định kỳ",
        format_money(lai_dinh_ky)
    )

with col3:
    st.metric(
        "📈 Tổng tiền lãi",
        format_money(tong_lai)
    )

with col4:
    st.metric(
        "🏦 Tổng gốc + lãi",
        format_money(tong_tien)
    )

st.divider()

# =========================================================
# 10. THÔNG TIN KHOẢN GỬI
# =========================================================

st.subheader("📋 Thông tin khoản gửi")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Số tiền gửi:** {format_money(tien_gui)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")

with col2:
    st.write(f"**Phương pháp:** {loai_lai}")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")

st.divider()

# =========================================================
# 11. TẠO DỮ LIỆU BIỂU ĐỒ TĂNG TRƯỞNG
# =========================================================

data = []

for thang in range(0, ky_han + 1):

    # -----------------------------------------------------
    # LÃI ĐƠN
    # -----------------------------------------------------

    if loai_lai == "Lãi đơn":

        tien_tich_luy = tien_gui * (
            1 + lai_suat_nam * thang / 12
        )

    # -----------------------------------------------------
    # LÃI KÉP
    # -----------------------------------------------------

    else:

        # Lãnh lãi hàng tháng
        if hinh_thuc == "Lãnh lãi hàng tháng":

            tien_tich_luy = tien_gui * (
                1 + lai_suat_nam / 12
            ) ** thang

        # Lãnh lãi hàng quý
        elif hinh_thuc == "Lãnh lãi hàng quý":

            so_quy = thang // 3

            tien_tich_luy = tien_gui * (
                1 + lai_suat_nam / 4
            ) ** so_quy

        # Lãnh lãi cuối kỳ
        else:

            tien_tich_luy = tien_gui * (
                1 + lai_suat_nam
            ) ** (thang / 12)

    tien_lai = tien_tich_luy - tien_gui

    data.append({
        "Tháng": thang,
        "Tổng tiền": tien_tich_luy,
        "Tiền lãi": tien_lai
    })

df = pd.DataFrame(data)

# =========================================================
# 12. BIỂU ĐỒ TĂNG TRƯỞNG
# =========================================================

st.subheader("📈 Biểu đồ tăng trưởng tiền gửi")

st.write(
    f"Biểu đồ thể hiện sự thay đổi của khoản tiền "
    f"trong {ky_han} tháng theo phương pháp **{loai_lai}**."
)

fig = px.line(
    df,
    x="Tháng",
    y="Tổng tiền",
    markers=True,
    title=f"Tăng trưởng tiền gửi - {loai_lai}"
)

fig.update_layout(
    xaxis_title="Thời gian (tháng)",
    yaxis_title="Tổng số tiền (VNĐ)",
    hovermode="x unified"
)

fig.update_yaxes(
    tickformat=",.0f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# 13. BIỂU ĐỒ TIỀN GỐC VÀ TIỀN LÃI
# =========================================================

st.subheader("💵 Tăng trưởng tiền gốc và tiền lãi")

fig2 = px.area(
    df,
    x="Tháng",
    y=["Tổng tiền", "Tiền lãi"],
    title="So sánh tổng tiền và tiền lãi theo thời gian"
)

fig2.update_layout(
    xaxis_title="Thời gian (tháng)",
    yaxis_title="Số tiền (VNĐ)",
    hovermode="x unified"
)

fig2.update_yaxes(
    tickformat=",.0f"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================================================
# 14. BẢNG CHI TIẾT
# =========================================================

st.subheader("📋 Chi tiết tăng trưởng theo từng tháng")

df_display = df.copy()

df_display["Tổng tiền"] = df_display["Tổng tiền"].apply(
    format_money
)

df_display["Tiền lãi"] = df_display["Tiền lãi"].apply(
    format_money
)

st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# 15. NHẬN XÉT
# =========================================================

st.subheader("💡 Nhận xét")

if loai_lai == "Lãi kép":

    st.success(
        "Lãi kép cho phép tiền lãi được cộng vào vốn. "
        "Ở các kỳ tiếp theo, tiền lãi được tính trên cả "
        "vốn ban đầu và phần lãi đã tích lũy. "
        "Do đó, khoản tiền có xu hướng tăng nhanh hơn "
        "khi thời gian gửi dài."
    )

else:

    st.info(
        "Lãi đơn chỉ tính tiền lãi dựa trên số tiền gốc ban đầu. "
        "Vì vậy, tiền lãi tăng đều qua các kỳ."
    )

# =========================================================
# 16. CÔNG THỨC
# =========================================================

with st.expander("📚 Xem công thức tính"):

    if loai_lai == "Lãi đơn":

        st.markdown("### Công thức lãi đơn")

        st.latex(
            r"I = P \times r \times t"
        )

        st.write("Trong đó:")
        st.write("• P: Số tiền gốc")
        st.write("• r: Lãi suất năm")
        st.write("• t: Thời gian gửi tính theo năm")
        st.write("• I: Tổng tiền lãi")

        st.markdown("### Tổng số tiền nhận được")

        st.latex(
            r"A = P + I"
        )

    else:

        st.markdown("### Công thức lãi kép")

        st.latex(
            r"A = P(1+r)^n"
        )

        st.write("Trong đó:")
        st.write("• P: Số tiền gốc")
        st.write("• r: Lãi suất mỗi kỳ")
        st.write("• n: Số kỳ nhập lãi")
        st.write("• A: Tổng số tiền cuối kỳ")

# =========================================================
# 17. FOOTER
# =========================================================

st.divider()

st.caption(
    "💡 Công cụ tính toán mang tính tham khảo. "
    "Lãi suất thực tế có thể thay đổi tùy theo ngân hàng "
    "và sản phẩm tiền gửi."
)
