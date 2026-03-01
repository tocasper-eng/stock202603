import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import datetime

# 1. 網頁基本設定
st.set_page_config(page_title="台積電股價追蹤器", layout="centered")
st.title("📈 台積電 (2330.TW) 股價互動圖表")
st.markdown("輸入日期區間，即時查看台積電走勢。")

# 2. 側邊欄設定
st.sidebar.header("查詢條件")
ticker = "2330.TW"

# 設定預設日期：從一年前到今天
default_start = datetime.date.today() - datetime.timedelta(days=365)
start_date = st.sidebar.date_input("開始日期", default_start)
end_date = st.sidebar.date_input("結束日期", datetime.date.today())

# 3. 主要邏輯
if start_date < end_date:
    with st.spinner('正在從 Yahoo Finance 抓取資料...'):
        # 下載數據
        df = yf.download(ticker, start=start_date, end=end_date)
        
    if not df.empty:
        # --- 重要修正：處理 yfinance 的多重索引問題 ---
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        # ------------------------------------------

        # A. 顯示最新資訊卡片
        latest_price = float(df['Close'].iloc[-1])
        price_diff = latest_price - float(df['Close'].iloc[-2])
        
        col1, col2 = st.columns(2)
        col1.metric(label="最新收盤價", value=f"{latest_price:.2f} TWD", delta=f"{price_diff:.2f}")
        col2.metric(label="資料筆數", value=len(df))

        # B. 繪製圖表
        st.subheader("股價走勢圖")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df.index, df['Close'], color='#0077b6', linewidth=2, label='收盤價')
        ax.set_ylabel("價格 (TWD)")
        ax.set_xlabel("日期")
        ax.grid(True, linestyle='--', alpha=0.5)
        
        # 讓 X 軸日期不要擠在一起
        plt.xticks(rotation=45)
        
        st.pyplot(fig)

        # C. 顯示原始數據表格（可選）
        with st.expander("查看原始數據表格"):
            st.write(df.sort_index(ascending=False))
            
    else:
        st.error("❌ 此日期區間沒有數據。可能是因為日期太近（股市尚未開盤）或日期格式有誤。")
else:
    st.warning("⚠️ 提醒：開始日期必須早於結束日期。")

st.info("提示：台股數據通常有 15-20 分鐘的延遲。")
