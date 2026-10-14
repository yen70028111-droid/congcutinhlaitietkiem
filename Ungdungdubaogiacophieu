import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from tensorflow.keras.callbacks import EarlyStopping

# -------------------------
# Cấu hình
# -------------------------
st.set_page_config(
    page_title="AI dự báo giá cổ phiếu",
    page_icon="📈",
    layout="wide"
)

SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)

st.title("📈 Ứng dụng AI dự báo giá cổ phiếu")
st.caption("Mô hình LSTM sử dụng dữ liệu giá đóng cửa lịch sử để dự báo tham khảo.")

with st.sidebar:
    st.header("⚙️ Cài đặt")
    ticker_input = st.text_input(
        "Mã cổ phiếu",
        value="VNM",
        help="Ví dụ Việt Nam: VNM, FPT, VCB, HPG. Mã Yahoo Finance thường có hậu tố .VN."
    )
    years = st.selectbox("Khoảng dữ liệu lịch sử", [3, 5, 8, 10], index=1)
    epochs = st.slider("Số vòng huấn luyện tối đa", min_value=5, max_value=30, value=10, step=5)
    run_button = st.button("🔍 Dự báo giá", type="primary", use_container_width=True)
    st.markdown("---")
    st.caption("Dữ liệu: Yahoo Finance (yfinance). Mô hình: LSTM.")

def normalize_ticker(raw_ticker: str) -> str:
    ticker = raw_ticker.strip().upper().replace(" ", "")
    if not ticker:
        return ""
    # Tự thêm hậu tố .VN cho một số mã Việt Nam phổ biến.
    # Với mã khác, người dùng có thể nhập hậu tố Yahoo Finance đầy đủ, ví dụ ABC.VN.
    vietnam_tickers = {
        "VNM", "FPT", "VCB", "HPG", "VIC", "VHM", "SSI", "MWG", "GAS",
        "MSN", "VRE", "TCB", "MBB", "ACB", "CTG", "BID", "VPB", "HDB",
        "STB", "TPB", "VIB", "SHB", "GVR", "SAB", "PLX", "POW", "PNJ",
        "DGC", "REE", "VND", "DXG", "PDR", "KDH", "NVL", "BMP", "VHC",
        "ANV", "DBC", "HAG", "KBC", "DIG", "CEO", "PVT", "PVS", "PVD"
    }
    if "." not in ticker and ticker in vietnam_tickers:
        ticker = f"{ticker}.VN"
    return ticker

@st.cache_data(ttl=3600, show_spinner=False)
def download_prices(ticker: str, years_back: int) -> pd.DataFrame:
    end_date = pd.Timestamp.today().normalize() + pd.Timedelta(days=1)
    start_date = end_date - pd.DateOffset(years=years_back)
    df = yf.download(
        ticker,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d"),
        auto_adjust=True,
        progress=False,
        threads=False
    )
    if df is None or df.empty:
        return pd.DataFrame()
    # Một số phiên bản yfinance trả về cột MultiIndex.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    if "Close" not in df.columns:
        return pd.DataFrame()
    prices = df[["Close"]].copy()
    prices.columns = ["Close"]
    prices = prices.dropna()
    prices.index = pd.to_datetime(prices.index)
    if prices.index.tz is not None:
        prices.index = prices.index.tz_localize(None)
    return prices

def create_sequences(values: np.ndarray, window_size: int = 60):
    X, y = [], []
    for i in range(window_size, len(values)):
        X.append(values[i-window_size:i, 0])
        y.append(values[i, 0])
    return np.asarray(X, dtype=np.float32).reshape(-1, window_size, 1), np.asarray(y, dtype=np.float32)

@st.cache_data(ttl=3600, show_spinner="Đang huấn luyện mô hình LSTM... Quá trình có thể mất vài phút.")
def train_and_forecast(ticker: str, years_back: int, epochs: int):
    prices = download_prices(ticker, years_back)
    if prices.empty or len(prices) < 120:
        return None

    values = prices[["Close"]].values.astype(float)
    window = 60
    train_size = int(len(values) * 0.8)
    if train_size <= window + 10 or len(values) - train_size < 10:
        return None

    # Chỉ fit scaler trên tập train để hạn chế rò rỉ dữ liệu.
    scaler = MinMaxScaler()
    train_scaled = scaler.fit_transform(values[:train_size])
    all_scaled = scaler.transform(values)

    X_train_all, y_train_all = create_sequences(train_scaled, window)
    val_size = max(1, int(len(X_train_all) * 0.1))
    if len(X_train_all) <= val_size:
        return None
    X_train, y_train = X_train_all[:-val_size], y_train_all[:-val_size]
    X_val, y_val = X_train_all[-val_size:], y_train_all[-val_size:]

    model = Sequential([
        Input(shape=(window, 1)),
        LSTM(50, return_sequences=True),
        LSTM(50),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mean_squared_error")
    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=4,
        restore_best_weights=True
    )
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=32,
        shuffle=False,
        callbacks=[early_stop],
        verbose=0
    )

    # Dự báo tập test: dùng 60 phiên trước đó để dự báo từng phiên test.
    X_test, y_test_scaled = create_sequences(all_scaled[train_size-window:], window)
    # create_sequences trên đoạn bắt đầu trước test 60 phiên tạo đúng các mẫu test.
    if len(X_test) == 0:
        return None
    test_pred_scaled = model.predict(X_test, verbose=0)
    test_pred = scaler.inverse_transform(test_pred_scaled).ravel()
    y_test = scaler.inverse_transform(y_test_scaled.reshape(-1, 1)).ravel()
    test_dates = prices.index[train_size:]

    # Dự báo cuốn chiếu 10 phiên tiếp theo từ 60 giá gần nhất.
    last_window = all_scaled[-window:].reshape(1, window, 1).copy()
    future_scaled = []
    for _ in range(10):
        next_value = model.predict(last_window, verbose=0)[0, 0]
        future_scaled.append(next_value)
        last_window = np.concatenate(
            [last_window[:, 1:, :], np.array(next_value, dtype=np.float32).reshape(1, 1, 1)],
            axis=1
        )
    future_prices = scaler.inverse_transform(np.array(future_scaled).reshape(-1, 1)).ravel()
    future_dates = pd.bdate_range(prices.index[-1] + pd.Timedelta(days=1), periods=10)

    rmse = float(np.sqrt(mean_squared_error(y_test, test_pred)))
    mae = float(mean_absolute_error(y_test, test_pred))
    r2 = float(r2_score(y_test, test_pred)) if len(y_test) > 1 else float("nan")

    test_df = pd.DataFrame({
        "Ngày": test_dates,
        "Giá thật": y_test,
        "Dự báo test": test_pred
    })
    future_df = pd.DataFrame({
        "Phiên dự báo": np.arange(1, 11),
        "Ngày dự kiến": future_dates,
        "Giá dự báo": future_prices
    })
    loss_df = pd.DataFrame({
        "Epoch": np.arange(1, len(history.history["loss"]) + 1),
        "Train Loss": history.history["loss"],
        "Validation Loss": history.history["val_loss"]
    })
    return {
        "prices": prices,
        "test_df": test_df,
        "future_df": future_df,
        "loss_df": loss_df,
        "rmse": rmse,
        "mae": mae,
        "r2": r2
    }

# Chỉ chạy dự báo khi người dùng nhấn nút.
if run_button:
    ticker = normalize_ticker(ticker_input)
    if not ticker:
        st.error("Vui lòng nhập mã cổ phiếu.")
    else:
        st.session_state["last_ticker"] = ticker
        st.session_state["last_years"] = years
        st.session_state["last_epochs"] = epochs
        st.session_state["run_forecast"] = True

if st.session_state.get("run_forecast", False):
    ticker = st.session_state.get("last_ticker", normalize_ticker(ticker_input))
    years_back = st.session_state.get("last_years", years)
    epochs_used = st.session_state.get("last_epochs", epochs)

    try:
        with st.spinner(f"Đang tải dữ liệu và phân tích {ticker}..."):
            result = train_and_forecast(ticker, years_back, epochs_used)

        if result is None:
            st.error(
                "Không đủ dữ liệu hoặc không tìm thấy mã cổ phiếu. "
                "Hãy kiểm tra mã, ví dụ VNM, FPT, VCB hoặc mã Yahoo Finance như AAPL."
            )
        else:
            prices = result["prices"]
            latest_price = float(prices["Close"].iloc[-1])
            latest_date = prices.index[-1].strftime("%d/%m/%Y")
            final_forecast = float(result["future_df"]["Giá dự báo"].iloc[-1])
            change_pct = (final_forecast / latest_price - 1) * 100 if latest_price else 0

            st.subheader(f"Kết quả phân tích: {ticker}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Giá đóng cửa gần nhất", f"{latest_price:,.2f}", help=f"Dữ liệu đến {latest_date}")
            c2.metric("Dự báo phiên thứ 10", f"{final_forecast:,.2f}", f"{change_pct:+.2f}% so với giá gần nhất")
            c3.metric("RMSE tập kiểm tra", f"{result['rmse']:,.2f}")
            c4.metric("MAE tập kiểm tra", f"{result['mae']:,.2f}")

            st.caption(
                f"Dữ liệu lịch sử: {prices.index[0].strftime('%d/%m/%Y')} – {latest_date}. "
                "Ngày dự báo là ngày làm việc dự kiến, chưa loại trừ tất cả ngày nghỉ của từng sàn."
            )

            st.subheader("📊 Biểu đồ giá thật và dự báo")
            fig, ax = plt.subplots(figsize=(12, 5.5))
            test_df = result["test_df"]
            future_df = result["future_df"]
            ax.plot(test_df["Ngày"], test_df["Giá thật"], label="Giá thật", linewidth=1.5)
            ax.plot(test_df["Ngày"], test_df["Dự báo test"], label="Dự báo test", linewidth=1.7)
            ax.plot(
                future_df["Ngày dự kiến"], future_df["Giá dự báo"],
                marker="o", markersize=4, linewidth=2, label="10 phiên tới"
            )
            ax.axvline(prices.index[-1], linestyle="--", linewidth=1, alpha=0.6)
            ax.set_xlabel("Ngày")
            ax.set_ylabel("Giá đóng cửa")
            ax.set_title(f"Giá cổ phiếu {ticker}: thực tế và dự báo")
            ax.grid(True, alpha=0.25)
            ax.legend()
            fig.autofmt_xdate()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            st.subheader("🔮 Bảng dự báo 10 phiên tiếp theo")
            display_future = future_df.copy()
            display_future["Ngày dự kiến"] = display_future["Ngày dự kiến"].dt.strftime("%d/%m/%Y")
            display_future["Giá dự báo"] = display_future["Giá dự báo"].map(lambda x: f"{x:,.2f}")
            st.dataframe(display_future, use_container_width=True, hide_index=True)

            with st.expander("Xem biểu đồ sai số huấn luyện"):
                loss_df = result["loss_df"]
                fig_loss, ax_loss = plt.subplots(figsize=(9, 4))
                ax_loss.plot(loss_df["Epoch"], loss_df["Train Loss"], label="Train Loss")
                ax_loss.plot(loss_df["Epoch"], loss_df["Validation Loss"], label="Validation Loss")
                ax_loss.set_xlabel("Epoch")
                ax_loss.set_ylabel("MSE Loss")
                ax_loss.set_title("Loss Train vs Validation")
                ax_loss.grid(True, alpha=0.25)
                ax_loss.legend()
                st.pyplot(fig_loss, use_container_width=True)
                plt.close(fig_loss)

            st.download_button(
                "⬇️ Tải bảng dự báo CSV",
                data=result["future_df"].to_csv(index=False).encode("utf-8-sig"),
                file_name=f"du_bao_{ticker.replace('.', '_')}.csv",
                mime="text/csv"
            )

            st.info(
                "Lưu ý: Đây là mô hình học từ giá đóng cửa lịch sử, không sử dụng đầy đủ "
                "tin tức, báo cáo tài chính hay yếu tố vĩ mô. Dự báo có thể sai lệch lớn và "
                "không phải lời khuyên đầu tư."
            )
    except Exception as e:
        st.error(f"Không thể hoàn tất dự báo: {e}")
        st.caption("Kiểm tra kết nối Internet, mã cổ phiếu và dữ liệu Yahoo Finance rồi thử lại.")
else:
    st.markdown(
        """
        ### Cách sử dụng
        1. Nhập mã cổ phiếu ở thanh bên trái.
        2. Chọn khoảng dữ liệu lịch sử và số vòng huấn luyện.
        3. Nhấn **Dự báo giá** và chờ mô hình xử lý.

        **Ví dụ mã:** `VNM`, `FPT`, `VCB`, `HPG` (Việt Nam) hoặc `AAPL`, `MSFT` (Mỹ).
        """
    )
    st.warning("Mô hình cần kết nối Internet để tải dữ liệu. Lần chạy đầu có thể mất vài phút.")
