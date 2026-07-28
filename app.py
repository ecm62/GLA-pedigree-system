import streamlit as st
import pandas as pd

# --- 1. CONFIG & UI ---
st.set_page_config(page_title="GLA Pedigree & Breeding Elite", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; color: #1E293B !important; }
    .main-header {
        text-align: center; color: #FFFFFF !important; padding: 25px;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
        border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .status-box {
        background: white !important; padding: 15px; border-radius: 10px; flex: 1;
        text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0; border-top: 4px solid #3B82F6;
    }
    .status-label { font-size: 12px; color: #64748B !important; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; }
    .status-value { font-size: 18px; color: #1E3A8A !important; font-weight: 800; }
    .strategy-box { background-color: #EFF6FF !important; border-top: 4px solid #10B981 !important; }
    .badge-grade {
        background-color: #1E3A8A !important; color: #FFFFFF !important;
        padding: 2px 10px; border-radius: 15px; font-weight: bold; font-size: 16px;
    }
    .section-title {
        border-left: 6px solid #1E3A8A; padding-left: 15px;
        color: #1E3A8A !important; font-weight: 800; font-size: 20px; margin: 30px 0 15px 0;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. FILE UPLOADER ENGINE ---
st.markdown('<div class="main-header"><h1>🧬 GLA MULTI-GENERATION PEDIGREE & BREEDING SYSTEM</h1><p style="opacity: 0.8; font-size: 14px;">Advanced Family Tree Structure & Genetic Evaluation Dashboard</p></div>', unsafe_allow_html=True)

st.sidebar.markdown("### 📁 資料檔案上傳專區")
family_file = st.sidebar.file_uploader("上傳 育種_家族階層清單.csv", type=["csv"])
value_file = st.sidebar.file_uploader("上傳 母豬育種價值分析.csv", type=["csv"])

if family_file is not None and value_file is not None:
    df_fam = pd.read_csv(family_file, header=None)
    df_val = pd.read_csv(value_file)
    df_val.columns = [str(c).strip() for c in df_val.columns]
    df_val = df_val.map(lambda x: x.strip() if isinstance(x, str) else x)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        search_query = st.text_input("SEARCH BOAR / SOW ID", placeholder="輸入公豬或母豬耳號 (例如 144-5)...").strip()

    if search_query:
        # --- PART I: 家族樹架構與血統階層 ---
        st.markdown('<p class="section-title">I. 🧬 多代家族樹架構與血統階層</p>', unsafe_allow_html=True)
        mask_fam = df_fam.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        res_fam = df_fam[mask_fam]
        
        if not res_fam.empty:
            st.success(f"成功鎖定 ID「{search_query}」，在家族階層中找到 {len(res_fam)} 筆血統關聯節點：")
            fam_display = []
            for idx, row in res_fam.head(20).iterrows():
                fam_display.append({
                    "父系/公豬資訊 (Sire)": str(row.get(0, '')),
                    "代數 (Gen)": str(row.get(1, '')),
                    "品種": str(row.get(2, '')),
                    "母系/母豬資訊 (Dam)": str(row.get(6, ''))
                })
            st.dataframe(pd.DataFrame(fam_display), use_container_width=True)
        else:
            st.info(f"在家族階層清單中未直接對應到 ID「{search_query}」。")

        # --- PART II: 遺傳育種指數與表現數據 ---
        st.markdown('<p class="section-title">II. 📊 遺傳育種核心指標與評價</p>', unsafe_allow_html=True)
        value_col = '母豬耳號(Sow Ear Tag)'
        res_val = df_val[df_val[value_col].astype(str).str.contains(search_query, case=False, na=False)]
        
        if not res_val.empty:
            for idx, row in res_val.iterrows():
                st.markdown(f"**目標耳號鎖定: `{row.get(value_col)}` (品種: {row.get('品種(Breed)', 'N/A')})**")
                
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f'<div class="status-box"><div class="status-label">累計胎數 (Parity)</div><div class="status-value">{row.get("累計記錄胎數(Total Parities)", "N/A")}</div></div>', unsafe_allow_html=True)
                with c2:
                    idx_score = row.get("🏆 育種選拔指數(Selection Index)", "N/A")
                    st.markdown(f'<div class="status-box"><div class="status-label">選拔指數 (Index)</div><div class="status-value"><span class="badge-grade">{idx_score}</span></div></div>', unsafe_allow_html=True)
                with c3:
                    f_rate = row.get("個體成功分娩率(Farrowing Rate %)", 0)
                    st.markdown(f'<div class="status-box"><div class="status-label">分娩率</div><div class="status-value">{f_rate}%</div></div>', unsafe_allow_html=True)
                with c4:
                    comment = row.get("選拔評價與行動建議(Selection Comment)", "N/A")
                    st.markdown(f'<div class="status-box strategy-box"><div class="status-label">選拔評價 (Comment)</div><div class="status-value" style="font-size:13px;">{comment}</div></div>', unsafe_allow_html=True)
                
                st.markdown("##### 📈 核心遺傳與生產表現數據")
                col_a, col_b, col_c, col_d = st.columns(4)
                with col_a:
                    st.metric(label="總離乳窩重平均 (Avg LWW)", value=str(row.get('40% 總離乳窩重平均(Avg LWW)', '0')))
                with col_b:
                    st.metric(label="育成率平均 (Avg PWS)", value=str(row.get('35% 育成率平均(Avg PWS)', '0')))
                with col_c:
                    st.metric(label="產活仔數平均 (Avg NBA)", value=str(row.get('25% 產活仔數平均(Avg NBA)', '0')))
                with col_d:
                    death_date = row.get('☠️ 死亡日期(Date of Mortality)', '存活')
                    st.metric(label="狀態 / 死亡日期", value=str(death_date))
                
                st.markdown("---")
        else:
            st.warning(f"在育種價值分析表中未找到與 ID「{search_query}」對應的詳細表現紀錄。")
else:
    st.info("👈 請先從左側側邊欄上傳您的兩個 CSV 資料檔案（家族階層清單與母豬育種價值分析），系統即會呈現您的多代家族樹與育種關聯儀表板。")
