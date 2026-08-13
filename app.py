import streamlit as st
import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt

# 1. 页面基本配置
st.set_page_config(page_title="A股价值线随心刷", layout="centered", page_icon="📈")

# 设置 Matplotlib 中文字体支持
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

st.title("📈 A股价值线随心刷")
st.caption("点击下方按钮，随机抽取一家 A 股上市公司并生成简易价值线图表")

# 2. 抽卡按钮
if st.button("🎲 随机换一家公司", type="primary", use_container_width=True):
    with st.spinner("正在从全市场 5000+ 家公司中抽取并拉取数据..."):
        try:
            # 随机获取一家 A 股公司
            spot_df = ak.stock_zh_a_spot_em()
            random_stock = spot_df.sample(1).iloc[0]
            
            code = str(random_stock['代码'])
            name = str(random_stock['名称'])
            pe_ttm = random_stock['市盈率-动态']
            pb = random_stock['市净率']
            price = random_stock['最新价']

            st.success(f"🎉 抽中公司：{name} ({code})")
            
            # 卡片式显示核心估值
            col1, col2, col3 = st.columns(3)
            col1.metric("最新股价", f"￥{price}")
            col2.metric("市盈率 PE(TTM)", f"{pe_ttm} 倍")
            col3.metric("市净率 PB", f"{pb} 倍")

            # 在线官方免下载年报预览入口
            cninfo_url = f"http://www.cninfo.com.cn/new/disclosure/stock?stockCode={code}#annualReports"
            st.markdown(f"👉 **[点击直接在手机上翻阅该公司巨潮官方在线年报 (免下载)]({cninfo_url})**")

        except Exception as e:
            st.error(f"数据请求超时或接口异常，请再点击一次按钮重试：{e}")
else:
    st.info("👈 点击上方按钮开始抽取你的第一家随机公司！")
