import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import datetime

# 設定網頁標題
st.set_page_config(page_title="台積電股價追蹤器")
st.title("📈 台積電 (2330.TW) 股價互動圖表")

# 側邊欄：讓使用者輸入參數
st.sidebar.header("設定查詢區間")
start_date = st.sidebar.date_input("開始日期", datetime.date(2024, 1, 1))
end_date = st.sidebar.date_input("結束日期", datetime.date.today())

if start_date < end_date:
    # 下載數據
    ticker = "2330.TW"
    data = yf.download(ticker, start=start_date, end=end_date)

    if not data.empty:
        # 顯示最新股價資訊
        latest_price = data['Close'].iloc[-1]
        st.metric(label="最新收盤價", value=f"{latest_price:.2f} TWD")

        # 繪製圖表
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data.index, data['Close'], label='Close Price', color='#0077b6')
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (TWD)")
        ax.grid(True, alpha=0.3)
        
        # 將 Matplotlib 圖表顯示在網頁上
        st.pyplot(fig)

        # 額外功能：顯示原始數據表格
        if st.checkbox("顯示原始數據"):
            st.write(data)
    else:
        st.error("此區間抓不到數據，請重新選擇日期。")
else:
    st.warning("錯誤：開始日期必須早於結束日期。")
