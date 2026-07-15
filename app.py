import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
from plotly.subplots import make_subplots
import io
import plotly.io as pio

# Cấu hình trang
st.set_page_config(
    page_title="Hệ thống Mô phỏng Adams-Bashforth", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background: #f0f2f6; }
    .main > div { padding-top: 1rem; background: #f0f2f6; }
    
    .custom-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
        border: none;
    }
    .custom-header h1 { margin: 0; font-size: 2.6rem; font-weight: 700; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.2); }
    .custom-header h2 { margin: 0.3rem 0 0 0; font-weight: 300; font-size: 1.6rem; color: rgba(255, 255, 255, 0.95); }
    
    .badge-container { margin-top: 0.8rem; display: flex; gap: 0.8rem; flex-wrap: wrap; }
    .badge {
        background: rgba(255, 255, 255, 0.2);
        padding: 0.3rem 1.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(5px);
        font-weight: 500;
    }
    
    .stSidebar {
        background: linear-gradient(180deg, #2d1b69 0%, #11998e 100%) !important;
        border-right: none;
    }
    .stSidebar * { color: #FFFFFF !important; }
    .stSidebar label { color: #FFFFFF !important; font-weight: 500 !important; }
    
    .stSidebar .stNumberInput input, .stSidebar .stTextInput input {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stSidebar .stSelectbox div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
    }
    .stSidebar .stSelectbox div[data-baseweb="select"] > div * {
        color: #1a1a2e !important;
        font-weight: 600 !important;
    }

    .stSidebar div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%) !important;
        border: 2px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(0, 176, 155, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    .stSidebar div[data-testid="stButton"] button * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    .stSidebar div[data-testid="stButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 176, 155, 0.5) !important;
    }

    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #ffd700 0%, #ffa500 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: #1a1a2e !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4) !important;
        padding: 0.7rem 1.5rem !important;
        width: 100% !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6) !important;
    }
    
    .info-box {
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
        margin: 0.5rem 0;
    }
    .info-box p { margin: 0.3rem 0; color: #FFFFFF !important; }
    .info-box b { color: #ffd700 !important; }
    
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.7rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.2rem;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    .section-header h3 { color: white; margin: 0; font-weight: 600; text-shadow: 0 2px 4px rgba(0,0,0,0.2); }
    
    .academic-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border-left: 5px solid #667eea;
        margin-bottom: 1.5rem;
    }
    .academic-card h4 { color: #2d1b69; margin-top: 0; font-weight: 700; }
    
    .arena-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    .leaderboard-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem 1.2rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        background: #f8fafc;
        border-left: 4px solid #cbd5e1;
    }
    .rank-1 { background: #fffdf5; border-left-color: #ffd700; }
    .rank-2 { background: #fafaff; border-left-color: #94a3b8; }
    .rank-3 { background: #fffaf5; border-left-color: #b45309; }
    .medal { font-size: 1.4rem; font-weight: bold; }
    
    .footer {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        border: none;
        margin-top: 2rem;
    }
    .footer p { margin: 0; color: white; }
    
    .stNumberInput input {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .tooltip-hint {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #495057;
        border-left: 3px solid #667eea;
    }
    
    .download-hint {
        background: #e7f3ff;
        border: 1px solid #b8d4f0;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        color: #004085;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- PHẦN THUẬT TOÁN -----------------
def rk4_starter(f, t0, h, y0, num_steps):
    T = [t0]
    Y = [y0]
    f_count = 0
    for _ in range(num_steps):
        t = T[-1]
        y = Y[-1]
        k1 = f(t, y)
        k2 = f(t + h/2, y + h/2*k1)
        k3 = f(t + h/2, y + h/2*k2)
        k4 = f(t + h, y + h*k3)
        f_count += 4
        T.append(t + h)
        y_next = y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
        if np.isnan(y_next) or np.isinf(y_next) or abs(y_next) > 1e7:
            Y.append(np.nan)
        else:
            Y.append(y_next)
    return np.array(T), np.array(Y), f_count

def solve_ab2(f, t0, Tmax, y0, N):
    h = (Tmax - t0) / N
    T = np.linspace(t0, Tmax, N + 1)
    Y = np.zeros(N + 1)
    _, Y_start, f_count = rk4_starter(f, t0, h, y0, 1)
    Y[0:2] = Y_start[0:2]
    if np.any(np.isnan(Y[0:2])):
        Y[:] = np.nan
        return T, Y, f_count
    f_hist = np.zeros(N + 1)
    f_hist[0] = f(T[0], Y[0])
    f_hist[1] = f(T[1], Y[1])
    f_count += 2
    for n in range(1, N):
        Y[n+1] = Y[n] + (h/2) * (3*f_hist[n] - f_hist[n-1])
        if np.isnan(Y[n+1]) or np.isinf(Y[n+1]) or abs(Y[n+1]) > 1e7:
            Y[n+1:] = np.nan
            break
        f_hist[n+1] = f(T[n+1], Y[n+1])
        f_count += 1
    return T, Y, f_count

def solve_ab3(f, t0, Tmax, y0, N):
    h = (Tmax - t0) / N
    T = np.linspace(t0, Tmax, N + 1)
    Y = np.zeros(N + 1)
    _, Y_start, f_count = rk4_starter(f, t0, h, y0, 2)
    Y[0:3] = Y_start[0:3]
    if np.any(np.isnan(Y[0:3])):
        Y[:] = np.nan
        return T, Y, f_count
    f_hist = np.zeros(N + 1)
    for i in range(3):
        f_hist[i] = f(T[i], Y[i])
    f_count += 3
    for n in range(2, N):
        Y[n+1] = Y[n] + (h/12) * (23*f_hist[n] - 16*f_hist[n-1] + 5*f_hist[n-2])
        if np.isnan(Y[n+1]) or np.isinf(Y[n+1]) or abs(Y[n+1]) > 1e7:
            Y[n+1:] = np.nan
            break
        f_hist[n+1] = f(T[n+1], Y[n+1])
        f_count += 1
    return T, Y, f_count

def solve_ab4(f, t0, Tmax, y0, N):
    h = (Tmax - t0) / N
    T = np.linspace(t0, Tmax, N + 1)
    Y = np.zeros(N + 1)
    _, Y_start, f_count = rk4_starter(f, t0, h, y0, 3)
    Y[0:4] = Y_start[0:4]
    if np.any(np.isnan(Y[0:4])):
        Y[:] = np.nan
        return T, Y, f_count
    f_hist = np.zeros(N + 1)
    for i in range(4):
        f_hist[i] = f(T[i], Y[i])
    f_count += 4
    for n in range(3, N):
        Y[n+1] = Y[n] + (h/24) * (55*f_hist[n] - 59*f_hist[n-1] + 37*f_hist[n-2] - 9*f_hist[n-3])
        if np.isnan(Y[n+1]) or np.isinf(Y[n+1]) or abs(Y[n+1]) > 1e7:
            Y[n+1:] = np.nan
            break
        f_hist[n+1] = f(T[n+1], Y[n+1])
        f_count += 1
    return T, Y, f_count

# ----------------- HÀM XỬ LÝ PHƯƠNG TRÌNH TỰ DO -----------------
def parse_equation(equation_str):
    equation_str = equation_str.replace('^', '**')
    safe_dict = {
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'exp': np.exp, 'log': np.log, 'log10': np.log10,
        'sqrt': np.sqrt, 'abs': np.abs, 'pi': np.pi,
        'e': np.e
    }
    def f(t, y):
        try:
            local_dict = {'t': t, 'y': y}
            return eval(equation_str, {"__builtins__": {}}, {**safe_dict, **local_dict})
        except:
            return np.nan
    return f

# ----------------- QUẢN LÝ SESSION STATE -----------------
if "current_problem_type" not in st.session_state:
    st.session_state.current_problem_type = "Ứng dụng thực tế sinh động"
if "current_real_choice" not in st.session_state:
    st.session_state.current_real_choice = "☕ Định luật nguội lạnh Newton (Ly cà phê nguội dần)"
if "current_academic_choice" not in st.session_state:
    st.session_state.current_academic_choice = "y' = y - t² + 1"
if "current_free_equation" not in st.session_state:
    st.session_state.current_free_equation = "y - t**2 + 1"
if "current_free_exact" not in st.session_state:
    st.session_state.current_free_exact = "t**2 + 2*t + 1 - 0.5*exp(t)"
if "current_has_exact" not in st.session_state:
    st.session_state.current_has_exact = True

if "y0_val" not in st.session_state:
    st.session_state.y0_val = 90.0
if "Tmax_val" not in st.session_state:
    st.session_state.Tmax_val = 10.0
if "N_val" not in st.session_state:
    st.session_state.N_val = 100
if "h_val" not in st.session_state:
    st.session_state.h_val = 0.1
if "mode" not in st.session_state:
    st.session_state.mode = "Nhập N"

# ----------------- SIDEBAR -----------------
st.sidebar.markdown("""
<div class="sidebar-header">
    <h3>🛠️ CẤU HÌNH HỆ THỐNG</h3>
</div>
""", unsafe_allow_html=True)

# HƯỚNG DẪN NHẬP THAM SỐ
st.sidebar.markdown("""
<div class="tooltip-hint" style="background: rgba(255,255,255,0.1); border-color: rgba(255,215,0,0.5); color: #FFFFFF;">
    💡 <b>Hướng dẫn thay đổi tham số:</b><br>
    • Nhập giá trị mới vào ô tương ứng<br>
    • Nhấn <kbd>Enter</kbd> để cập nhật ngay<br>
    • Hoặc nhấn nút "MÔ PHỎNG" bên dưới
</div>
""", unsafe_allow_html=True)

# PHẦN 1: CHỌN CHỦ ĐỀ
st.sidebar.markdown("##### 1️⃣ CHỌN CHỦ ĐỀ NGHIÊN CỨU")
temp_problem_type = st.sidebar.radio(
    "Lựa chọn chủ đề:",
    ["Ứng dụng thực tế sinh động", "Bài toán mẫu học thuật", "Nhập phương trình tự do"],
    index=["Ứng dụng thực tế sinh động", "Bài toán mẫu học thuật", "Nhập phương trình tự do"].index(st.session_state.current_problem_type)
)

temp_real_choice = None
temp_academic_choice = None
temp_free_equation = "y - t**2 + 1"
temp_has_exact = True
temp_free_exact = "t**2 + 2*t + 1 - 0.5*exp(t)"

if temp_problem_type == "Ứng dụng thực tế sinh động":
    temp_real_choice = st.sidebar.selectbox(
        "Chọn hiện tượng thực tế:",
        [
            "☕ Định luật nguội lạnh Newton (Ly cà phê nguội dần)", 
            "🪂 Sự rơi tự do có lực cản (Nhảy dù)", 
            "📢 Sự lan truyền tin đồn (Mô hình Logistic)"
        ],
        index=[
            "☕ Định luật nguội lạnh Newton (Ly cà phê nguội dần)", 
            "🪂 Sự rơi tự do có lực cản (Nhảy dù)", 
            "📢 Sự lan truyền tin đồn (Mô hình Logistic)"
        ].index(st.session_state.current_real_choice) if st.session_state.current_real_choice in [
            "☕ Định luật nguội lạnh Newton (Ly cà phê nguội dần)", 
            "🪂 Sự rơi tự do có lực cản (Nhảy dù)", 
            "📢 Sự lan truyền tin đồn (Mô hình Logistic)"
        ] else 0
    )
elif temp_problem_type == "Bài toán mẫu học thuật":
    temp_academic_choice = st.sidebar.selectbox(
        "Chọn bài toán mẫu học thuật:",
        ["y' = y - t² + 1", "y' = -2ty", "y' = t + y", "y' = y"],
        index=["y' = y - t² + 1", "y' = -2ty", "y' = t + y", "y' = y"].index(st.session_state.current_academic_choice)
    )
else:
    temp_free_equation = st.sidebar.text_input("Nhập f(t, y) tự do:", value=st.session_state.current_free_equation)
    temp_has_exact = st.sidebar.checkbox("Có nghiệm giải tích?", value=st.session_state.current_has_exact)
    if temp_has_exact:
        temp_free_exact = st.sidebar.text_input("Nhập nghiệm y(t):", value=st.session_state.current_free_exact)

if st.sidebar.button("⚙️ CẬP NHẬT CHỦ ĐỀ"):
    st.session_state.current_problem_type = temp_problem_type
    if temp_problem_type == "Ứng dụng thực tế sinh động":
        st.session_state.current_real_choice = temp_real_choice
        if temp_real_choice == "☕ Định luật nguội lạnh Newton (Ly cà phê nguội dần)":
            st.session_state.y0_val = 90.0
            st.session_state.Tmax_val = 10.0
            st.session_state.N_val = 100
            st.session_state.h_val = 0.1
        elif temp_real_choice == "🪂 Sự rơi tự do có lực cản (Nhảy dù)":
            st.session_state.y0_val = 0.0
            st.session_state.Tmax_val = 15.0
            st.session_state.N_val = 120
            st.session_state.h_val = 0.125
        else:
            st.session_state.y0_val = 10.0
            st.session_state.Tmax_val = 12.0
            st.session_state.N_val = 150
            st.session_state.h_val = 0.08
    elif temp_problem_type == "Bài toán mẫu học thuật":
        st.session_state.current_academic_choice = temp_academic_choice
        st.session_state.y0_val = 0.5
        st.session_state.Tmax_val = 2.0
        st.session_state.N_val = 80
        st.session_state.h_val = 0.025
    else:
        st.session_state.current_free_equation = temp_free_equation
        st.session_state.current_has_exact = temp_has_exact
        st.session_state.current_free_exact = temp_free_exact
        st.session_state.y0_val = 0.5
        st.session_state.Tmax_val = 2.0
        st.session_state.N_val = 80
        st.session_state.h_val = 0.025
    st.rerun()

st.sidebar.markdown("---")

# PHẦN 2: THIẾT LẬP THAM SỐ - KHÔNG CẦN FORM
st.sidebar.markdown("##### 2️⃣ CẤU HÌNH THAM SỐ")

# Dùng session state để lưu giá trị tạm thời
if "temp_Tmax" not in st.session_state:
    st.session_state.temp_Tmax = st.session_state.Tmax_val
if "temp_y0" not in st.session_state:
    st.session_state.temp_y0 = st.session_state.y0_val
if "temp_N" not in st.session_state:
    st.session_state.temp_N = st.session_state.N_val
if "temp_h" not in st.session_state:
    st.session_state.temp_h = st.session_state.h_val

# Tmax
Tmax = st.sidebar.number_input(
    "⏰ Thời gian khảo sát (Tmax):",
    min_value=0.5,
    max_value=20.0,
    value=float(st.session_state.temp_Tmax),
    step=0.5,
    format="%.1f",
    key="Tmax_input",
    help="Nhập giá trị và nhấn Enter để cập nhật"
)
st.session_state.temp_Tmax = Tmax

# y0
y0 = st.sidebar.number_input(
    "🎯 Điều kiện ban đầu y(0):",
    value=float(st.session_state.temp_y0),
    format="%f",
    key="y0_input",
    help="Nhập giá trị và nhấn Enter để cập nhật"
)
st.session_state.temp_y0 = y0

st.sidebar.markdown("---")
st.sidebar.markdown("##### 🔧 Chọn cách nhập bước nhảy:")

# Mode
mode = st.sidebar.radio(
    "Chọn chế độ:",
    ["Nhập N (số bước lưới)", "Nhập h (bước nhảy)"],
    index=0 if st.session_state.mode == "Nhập N" else 1,
    key="mode_radio"
)
st.session_state.mode = mode

if mode == "Nhập N (số bước lưới)":
    N_input = st.sidebar.number_input(
        "📊 Số bước lưới (N):",
        min_value=2,
        max_value=1000,
        value=int(st.session_state.temp_N),
        step=1,
        key="N_input",
        help="Nhập giá trị và nhấn Enter để cập nhật"
    )
    st.session_state.temp_N = N_input
    h_calc = Tmax / N_input
    st.sidebar.info(f"📐 h = Tmax/N = {Tmax}/{N_input} = {h_calc:.6f}")
    h_final = h_calc
    N_final = N_input
else:
    h_input = st.sidebar.number_input(
        "📐 Bước nhảy (h):",
        min_value=0.001,
        max_value=1.0,
        value=float(st.session_state.temp_h),
        format="%.6f",
        step=0.001,
        key="h_input",
        help="Nhập giá trị và nhấn Enter để cập nhật"
    )
    st.session_state.temp_h = h_input
    N_calc = int(Tmax / h_input)
    if N_calc < 2:
        N_calc = 2
    st.sidebar.info(f"📊 N = Tmax/h = {Tmax}/{h_input:.6f} ≈ {N_calc}")
    h_final = h_input
    N_final = N_calc

# Cập nhật session state chính
st.session_state.Tmax_val = Tmax
st.session_state.y0_val = y0
st.session_state.N_val = N_final
st.session_state.h_val = h_final

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div class="info-box">
    <p style="color: #FFFFFF !important;">📐 <b style="color: #ffd700 !important;">Thông số hiện tại:</b></p>
    <p style="color: #FFFFFF !important;">Tmax = {Tmax}</p>
    <p style="color: #FFFFFF !important;">N = {N_final}</p>
    <p style="color: #FFFFFF !important;">h = {h_final:.10f}</p>
</div>
""", unsafe_allow_html=True)

# Nút Mô phỏng - chỉ để chạy lại chứ không cập nhật thông số
if st.sidebar.button("🚀 MÔ PHỎNG", key="simulate_button"):
    st.rerun()

Tmax_use = st.session_state.Tmax_val
y0_use = st.session_state.y0_val
N_use = st.session_state.N_val
h_use = st.session_state.h_val

# ----------------- HEADER CHÍNH + LỊCH SỬ -----------------
st.markdown("""
<div class="custom-header">
    <h1>☕ Hệ thống Mô phỏng Adams-Bashforth</h1>
    <h2>Phương pháp đa bước hiện cho bài toán giá trị ban đầu</h2>
    <div class="badge-container">
        <span class="badge">📊 AB2</span>
        <span class="badge">📈 AB3</span>
        <span class="badge">⭐ AB4</span>
        <span class="badge">🔄 RK4</span>
        <span class="badge">🌍 Ứng dụng thực tế</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- LỊCH SỬ ADAMS-BASHFORTH ---
with st.expander("📜 Lịch sử phương pháp Adams-Bashforth", expanded=False):
    st.markdown("""
    ### 🪐 John Couch Adams và phương pháp đa bước
    
    **John Couch Adams** (1819-1892) là nhà toán học và thiên văn học người Anh. 
    Ông nổi tiếng với việc **dự đoán sự tồn tại của Sao Hải Vương** vào năm 1846 
    bằng cách tính toán quỹ đạo của nó từ những nhiễu loạn trong quỹ đạo của Sao Thiên Vương.
    
    #### Phương pháp Adams-Bashforth:
    - Được phát triển để **tính toán quỹ đạo hành tinh** một cách chính xác
    - Là **phương pháp đa bước hiện** (explicit multistep method)
    - **Ưu điểm:** Chỉ cần gọi hàm f 1 lần mỗi bước, rất nhanh
    - **Nhược điểm:** Vùng ổn định nhỏ hơn các phương pháp ẩn
    
    #### Các biến thể:
    - **AB2:** Sử dụng 2 bước trước, độ chính xác bậc 2
    - **AB3:** Sử dụng 3 bước trước, độ chính xác bậc 3  
    - **AB4:** Sử dụng 4 bước trước, độ chính xác bậc 4
    
    *"Phương pháp Adams-Bashforth là công cụ không thể thiếu trong tính toán quỹ đạo vệ tinh và thiên thể."*
    """)

# ----------------- THIẾT LẬP PHƯƠNG TRÌNH -----------------
f_lambda = None
y_exact_lambda = None
equation_display = ""
real_history = ""
real_physics = ""
real_significance = ""
lambda_stable = -1.0
has_exact = st.session_state.current_has_exact

if st.session_state.current_problem_type == "Ứng dụng thực tế sinh động":
    if st.session_state.current_real_choice == "☕ Định luật nguội lạnh Newton (Ly cà phê nguội dần)":
        f_lambda = lambda t, y: -0.5 * (y - 25.0)
        y_exact_lambda = lambda t: 25.0 + (y0_use - 25.0) * np.exp(-0.5 * t)
        equation_display = "y' = -0.5 * (y - 25)"
        lambda_stable = -0.5
        
        real_history = """
        **📜 Bối cảnh Lịch sử:**
        Vào cuối thế kỷ 17, nhà vật lý học vĩ đại **Isaac Newton** đã thực hiện các thí nghiệm đo tốc độ nguội đi của các vật thể nóng.
        """
        real_physics = f"""
        **🧪 Mô tả Hiện tượng Vật lý:**
        Ly cà phê ban đầu ở mức **{y0_use}°C** được đặt trong phòng có nhiệt độ **25°C**.
        """
        real_significance = """
        **💡 Ý nghĩa của phương pháp Adams-Bashforth:**
        Phương pháp Adams-Bashforth giúp giải quyết bài toán một cách nhanh chóng mà không cần tính toán lại các hàm vi phân phức tạp ở mỗi bước.
        """
    elif st.session_state.current_real_choice == "🪂 Sự rơi tự do có lực cản (Nhảy dù)":
        f_lambda = lambda t, y: 9.8 - 0.3 * y
        y_exact_lambda = lambda t: (9.8 / 0.3) + (y0_use - (9.8 / 0.3)) * np.exp(-0.3 * t)
        equation_display = "y' = 9.8 - 0.3*y"
        lambda_stable = -0.3
        
        real_history = """
        **📜 Bối cảnh Lịch sử:**
        Mô hình lực cản không khí được phát triển từ thế kỷ 20 để bảo vệ tính mạng phi công.
        """
        real_physics = f"""
        **🧪 Mô tả Hiện tượng Vật lý:**
        Người nhảy dù xuất phát với vận tốc ban đầu **{y0_use} m/s**.
        """
        real_significance = """
        **💡 Ý nghĩa của phương pháp Adams-Bashforth:**
        Phương pháp đa bước Adams-Bashforth cực kỳ phù hợp nhờ tốc độ tính toán rất nhanh.
        """
    else:
        f_lambda = lambda t, y: 0.001 * y * (1000.0 - y)
        y_exact_lambda = lambda t: 1000.0 / (1.0 + ((1000.0 / y0_use) - 1.0) * np.exp(-1.0 * t))
        equation_display = "y' = 0.001 * y * (1000 - y)"
        lambda_stable = -1.0
        
        real_history = """
        **📜 Bối cảnh Lịch sử:**
        Mô hình toán học về sự lan truyền bắt đầu từ nghiên cứu của Kermack và McKendrick năm 1927.
        """
        real_physics = f"""
        **🧪 Mô tả Hiện tượng Xã hội:**
        Cộng đồng có 1000 người, ban đầu có **{y0_use} người** biết tin.
        """
        real_significance = """
        **💡 Ý nghĩa của phương pháp Adams-Bashforth:**
        Phương pháp Adams-Bashforth không yêu cầu giải phương trình phi tuyến lặp ở mỗi bước.
        """
    has_exact = True

elif st.session_state.current_problem_type == "Bài toán mẫu học thuật":
    if st.session_state.current_academic_choice == "y' = y - t² + 1":
        f_lambda = lambda t, y: y - t**2 + 1
        y_exact_lambda = lambda t: t**2 + 2*t + 1 - 0.5 * np.exp(t)
        equation_display = "y' = y - t² + 1"
        lambda_stable = 1.0
    elif st.session_state.current_academic_choice == "y' = -2ty":
        f_lambda = lambda t, y: -2*t*y
        y_exact_lambda = lambda t: np.exp(-t**2)
        equation_display = "y' = -2ty"
        lambda_stable = -2.0
    elif st.session_state.current_academic_choice == "y' = t + y":
        f_lambda = lambda t, y: t + y
        y_exact_lambda = lambda t: 2*np.exp(t) - t - 1
        equation_display = "y' = t + y"
        lambda_stable = 1.0
    else:
        f_lambda = lambda t, y: y
        y_exact_lambda = lambda t: np.exp(t)
        equation_display = "y' = y"
        lambda_stable = 1.0
    has_exact = True

else:
    try:
        f_lambda = parse_equation(st.session_state.current_free_equation)
        equation_display = f"y' = {st.session_state.current_free_equation}"
        lambda_stable = -1.0
        if has_exact and st.session_state.current_free_exact:
            def y_exact_lambda(t_val):
                safe_dict = {'sin': np.sin, 'cos': np.cos, 'tan': np.tan, 'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e}
                if isinstance(t_val, (int, float)):
                    return eval(st.session_state.current_free_exact, {"__builtins__": {}}, {**safe_dict, 't': t_val})
                else:
                    return np.array([eval(st.session_state.current_free_exact, {"__builtins__": {}}, {**safe_dict, 't': val}) for val in t_val])
        else:
            y_exact_lambda = None
    except Exception as e:
        st.sidebar.error(f"❌ Lỗi cú pháp phương trình: {str(e)}")
        st.stop()

# --- TÍNH TOÁN NGHIỆM ---
T, Y_ab2, fc_ab2 = solve_ab2(f_lambda, 0.0, Tmax_use, y0_use, N_use)
_, Y_ab3, fc_ab3 = solve_ab3(f_lambda, 0.0, Tmax_use, y0_use, N_use)

start_time = time.perf_counter()
_, Y_ab4, fc_ab4 = solve_ab4(f_lambda, 0.0, Tmax_use, y0_use, N_use)
t_ab4 = time.perf_counter() - start_time

start_time = time.perf_counter()
_, Y_rk4, fc_rk4 = rk4_starter(f_lambda, 0.0, h_use, y0_use, N_use)
t_rk4 = time.perf_counter() - start_time

start_time = time.perf_counter()
_, _, _ = solve_ab2(f_lambda, 0.0, Tmax_use, y0_use, N_use)
t_ab2 = time.perf_counter() - start_time

start_time = time.perf_counter()
_, _, _ = solve_ab3(f_lambda, 0.0, Tmax_use, y0_use, N_use)
t_ab3 = time.perf_counter() - start_time

if has_exact and y_exact_lambda is not None:
    try:
        Y_true = y_exact_lambda(T)
    except:
        Y_true = None
        has_exact = False
else:
    Y_true = None

def max_err(y_num, y_true):
    if y_true is None:
        return np.nan
    mask = ~np.isnan(y_num) & ~np.isnan(y_true)
    if not np.any(mask):
        return np.inf
    return np.max(abs(y_num[mask] - y_true[mask]))

err_ab2 = max_err(Y_ab2, Y_true)
err_ab3 = max_err(Y_ab3, Y_true)
err_ab4 = max_err(Y_ab4, Y_true)
err_rk4 = max_err(Y_rk4, Y_true)

has_diverged = np.any(np.isnan(Y_ab2)) or np.any(np.isnan(Y_ab3)) or np.any(np.isnan(Y_ab4))

# --- HIỂN THỊ HỒ SƠ HỌC THUẬT ---
if st.session_state.current_problem_type == "Ứng dụng thực tế sinh động" and real_history:
    st.markdown("""
    <div class="section-header">
        <h3>🌱 Hồ sơ học thuật của hiện tượng mô phỏng</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_hist, col_phys, col_sig = st.columns(3)
    with col_hist:
        st.markdown(f"""
        <div class="academic-card">
            <h4>{st.session_state.current_real_choice.split('(')[0]}</h4>
            {real_history}
        </div>
        """, unsafe_allow_html=True)
    with col_phys:
        st.markdown(f"""
        <div class="academic-card" style="border-left-color: #00b09b;">
            <h4>Mô tả vật lý</h4>
            {real_physics}
        </div>
        """, unsafe_allow_html=True)
    with col_sig:
        st.markdown(f"""
        <div class="academic-card" style="border-left-color: #ffd700;">
            <h4>Ý nghĩa phương pháp AB</h4>
            {real_significance}
        </div>
        """, unsafe_allow_html=True)

if has_diverged:
    st.warning("""
    ⚠️ **Cảnh báo mất ổn định số!** Hãy giảm bước nhảy $h$ (tăng N).
    """)

# --- BIỂU ĐỒ CHÍNH ---
st.markdown("""
<div class="section-header">
    <h3>📈 Đồ thị so sánh nghiệm số</h3>
</div>
""", unsafe_allow_html=True)

col_chart1, col_chart2 = st.columns([3, 1])

with col_chart2:
    chart_type = st.radio(
        "📊 Loại biểu đồ:",
        ["Tuyến tính", "Semi-log y", "Semi-log x", "Log-log"],
        index=0,
        key="main_chart_type"
    )
    
    # Thêm hướng dẫn tải ảnh
    st.markdown("""
    <div style="background: #e7f3ff; padding: 0.5rem; border-radius: 6px; margin-top: 0.5rem; font-size: 0.8rem; border: 1px solid #b8d4f0;">
        📷 <b>Tải ảnh:</b> Click vào biểu tượng 📷 trên thanh công cụ
    </div>
    """, unsafe_allow_html=True)

with col_chart1:
    fig = go.Figure()
    colors = {'exact': '#00b09b', 'rk4': '#667eea', 'ab2': '#f093fb', 'ab3': '#f5576c', 'ab4': '#ffd700'}
    
    if has_exact and Y_true is not None:
        fig.add_trace(go.Scatter(x=T, y=Y_true, name="Giải tích (Chính xác)", line=dict(color=colors['exact'], width=3), mode='lines'))
    
    fig.add_trace(go.Scatter(x=T, y=Y_rk4, name="RK4 (1 bước)", line=dict(color=colors['rk4'], width=2, dash='dash'), mode='lines+markers', marker=dict(size=4)))
    fig.add_trace(go.Scatter(x=T, y=Y_ab2, name="AB2 (2 bước)", line=dict(color=colors['ab2'], width=2, dash='dot'), mode='lines+markers', marker=dict(size=4)))
    fig.add_trace(go.Scatter(x=T, y=Y_ab3, name="AB3 (3 bước)", line=dict(color=colors['ab3'], width=2, dash='dashdot'), mode='lines+markers', marker=dict(size=4)))
    fig.add_trace(go.Scatter(x=T, y=Y_ab4, name="AB4 (4 bước) ⭐", line=dict(color=colors['ab4'], width=3), mode='lines+markers', marker=dict(size=5)))
    
    type_x = "log" if chart_type in ["Semi-log x", "Log-log"] else "linear"
    type_y = "log" if chart_type in ["Semi-log y", "Log-log"] else "linear"
    fig.update_xaxes(title_text="Thời gian t", type=type_x, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text="Giá trị y(t)", type=type_y, showgrid=True, gridcolor='lightgray')
    fig.update_layout(
        margin=dict(l=60, r=30, t=40, b=60),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.95)", bordercolor="#667eea", borderwidth=2),
        hovermode='x unified', template='plotly_white',
        plot_bgcolor='rgba(255,255,255,0.8)', paper_bgcolor='rgba(255,255,255,0.9)'
    )
    st.plotly_chart(fig, use_container_width=True, key="static_chart_main")
    
    # Hướng dẫn tải ảnh chi tiết cho biểu đồ chính
    with st.expander("📷 Hướng dẫn tải ảnh biểu đồ này"):
        st.markdown("""
        **Các cách tải ảnh biểu đồ:**
        
        1. **Click chuột phải** vào biểu đồ → Chọn:
           - `Download image as PNG` (định dạng ảnh nén)
           - `Download image as SVG` (định dạng vector, chất lượng cao)
        
        2. **Sử dụng thanh công cụ** phía trên bên phải biểu đồ:
           - Click vào biểu tượng **máy ảnh** 📷
           - Chọn định dạng mong muốn
        
        3. **Phím tắt:** Nhấn `Ctrl+S` hoặc `Cmd+S` khi đang focus vào biểu đồ
        
        💡 **Mẹo:** Định dạng SVG cho chất lượng tốt nhất khi in ấn hoặc phóng to
        """)

# --- SO SÁNH HIỆU NĂNG ---
st.markdown("""
<div class="section-header">
    <h3>⚔️ So sánh hiệu năng</h3>
</div>
""", unsafe_allow_html=True)

col_lead1, col_lead2, col_lead3 = st.columns(3)

with col_lead1:
    st.markdown('<div class="arena-card"><h4>📉 Độ Chính Xác (Sai số Max)</h4>', unsafe_allow_html=True)
    sort_err = []
    for n, e in [("AB4", err_ab4), ("RK4", err_rk4), ("AB3", err_ab3), ("AB2", err_ab2)]:
        if not np.isnan(e) and np.isfinite(e):
            sort_err.append((n, e))
    sort_err = sorted(sort_err, key=lambda x: x[1])
    for idx, (name, val) in enumerate(sort_err):
        rank_class = f"rank-{idx+1}" if idx < 3 else ""
        medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else "🏃"
        st.markdown(f"""
        <div class="leaderboard-row {rank_class}">
            <span>{medal} <b>{name}</b></span>
            <span>{val:.4e}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_lead2:
    st.markdown('<div class="arena-card"><h4>⏱️ Tốc Độ Thực Thi</h4>', unsafe_allow_html=True)
    sort_time = sorted([("AB2", t_ab2), ("AB3", t_ab3), ("AB4", t_ab4), ("RK4", t_rk4)], key=lambda x: x[1])
    for idx, (name, val) in enumerate(sort_time):
        rank_class = f"rank-{idx+1}" if idx < 3 else ""
        medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else "🏃"
        st.markdown(f"""
        <div class="leaderboard-row {rank_class}">
            <span>{medal} <b>{name}</b></span>
            <span>{val:.6f}s</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_lead3:
    st.markdown('<div class="arena-card"><h4>🧠 Số lần gọi hàm f</h4>', unsafe_allow_html=True)
    sort_call = sorted([("AB2", fc_ab2), ("AB3", fc_ab3), ("AB4", fc_ab4), ("RK4", fc_rk4)], key=lambda x: x[1])
    for idx, (name, val) in enumerate(sort_call):
        rank_class = f"rank-{idx+1}" if idx < 3 else ""
        medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else "🏃"
        st.markdown(f"""
        <div class="leaderboard-row {rank_class}">
            <span>{medal} <b>{name}</b></span>
            <span>{val} lần</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- BẢN ĐỒ VÙNG ỔN ĐỊNH ---
st.markdown("""
<div class="section-header">
    <h3>🌌 Bản đồ Vùng ổn định Tuyệt đối</h3>
</div>
""", unsafe_allow_html=True)

# Hướng dẫn cách đọc
st.markdown("""
<div style="background: #f0f4ff; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border-left: 4px solid #667eea;">
    <b>📖 Cách đọc bản đồ vùng ổn định:</b><br>
    • <b>Trục hoành (Re(hλ)):</b> Phần thực của tích hλ<br>
    • <b>Trục tung (Im(hλ)):</b> Phần ảo của tích hλ<br>
    • <b>Các đường cong:</b> Ranh giới ổn định của từng phương pháp (AB2, AB3, AB4)<br>
    • <b>🔴 Chấm đỏ:</b> Trạng thái hiện tại của hệ thống với giá trị h và λ đang chọn<br>
    • <b>✅ Nếu chấm đỏ nằm TRONG vùng:</b> Nghiệm ổn định, sai số không bị khuếch đại<br>
    • <b>❌ Nếu chấm đỏ nằm NGOÀI vùng:</b> Nghiệm mất ổn định, cần giảm h (tăng N)
</div>
""", unsafe_allow_html=True)

col_stab1, col_stab2 = st.columns([2, 1])

with col_stab2:
    st.markdown("""
    #### Bản chất của Vùng Ổn Định Tuyệt Đối 🪐
    * **Vùng ổn định:** Tập hợp các giá trị $h\lambda$ mà sai số tiến về 0.
    * **Đặc trưng:** Bậc phương pháp càng cao, vùng ổn định càng co hẹp.
    """)
    h_lambda_point = h_use * lambda_stable
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.05); padding: 1.2rem; border-radius: 10px; border-left: 5px solid #764ba2;">
        <h5>📍 Điểm kiểm thử hiện tại:</h5>
        <p><b>hλ</b> = <b>{h_lambda_point:.4f}</b></p>
        <p style="font-size: 0.9rem; color: #555;">Vị trí của 🔴 chấm đỏ trên đồ thị</p>
    """, unsafe_allow_html=True)
    if h_lambda_point > -0.3:
        st.success("✅ **Nghiệm ổn định!** Chấm đỏ nằm trong vùng ổn định.")
    else:
        st.error("❌ **Nguy cơ phân kỳ!** Chấm đỏ nằm ngoài vùng ổn định. Giảm h!")

with col_stab1:
    theta = np.linspace(0, 2*np.pi, 200)
    z = np.exp(1j * theta)
    h_ab2 = (z**2 - z) / (1.5 * z - 0.5)
    h_ab3 = (z**3 - z**2) / ((23/12)*z**2 - (16/12)*z + (5/12))
    h_ab4 = (z**4 - z**3) / ((55/24)*z**3 - (59/24)*z**2 + (37/24)*z - (9/24))
    
    fig_stab = go.Figure()
    fig_stab.add_trace(go.Scatter(x=np.real(h_ab2), y=np.imag(h_ab2), name="Ranh giới AB2", fill="toself", fillcolor="rgba(240, 147, 251, 0.1)", line=dict(color="#f093fb", width=2)))
    fig_stab.add_trace(go.Scatter(x=np.real(h_ab3), y=np.imag(h_ab3), name="Ranh giới AB3", fill="toself", fillcolor="rgba(245, 87, 108, 0.1)", line=dict(color="#f5576c", width=2)))
    fig_stab.add_trace(go.Scatter(x=np.real(h_ab4), y=np.imag(h_ab4), name="Ranh giới AB4", fill="toself", fillcolor="rgba(255, 215, 0, 0.15)", line=dict(color="#ffd700", width=3)))
    fig_stab.add_trace(go.Scatter(x=[h_lambda_point], y=[0.0], name="🔴 Trạng thái hiện tại (hλ)", mode="markers", marker=dict(color="red", size=16, symbol="star-diamond", line=dict(color="white", width=2))))
    fig_stab.update_xaxes(title_text="Re(hλ)", range=[-2.5, 0.5], showgrid=True, gridcolor='lightgray')
    fig_stab.update_yaxes(title_text="Im(hλ)", range=[-1.5, 1.5], showgrid=True, gridcolor='lightgray')
    fig_stab.update_layout(height=450, margin=dict(l=50, r=20, t=20, b=50), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01), template='plotly_white')
    st.plotly_chart(fig_stab, use_container_width=True, key="stability_map")

# --- BIỂU ĐỒ SAI SỐ ---
if has_exact and Y_true is not None and not has_diverged:
    st.markdown("""
    <div class="section-header">
        <h3>📊 Biểu đồ sai số chi tiết</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Thêm hướng dẫn tải ảnh cho biểu đồ sai số
    st.info("💡 **Hướng dẫn tải ảnh sai số:** Click chuột phải vào biểu đồ → Chọn 'Download image as PNG' hoặc 'Download image as SVG'")
    
    error_chart_type = st.radio(
        "Loại biểu đồ:",
        ["Tuyến tính", "Semi-log y", "Semi-log x", "Log-log"],
        index=0, key="error_chart_type", horizontal=True
    )
    
    fig2 = make_subplots(rows=2, cols=1, subplot_titles=("<b>Sai số tuyệt đối</b>", "<b>Sai số tương đối (%)</b>"), vertical_spacing=0.15, shared_xaxes=True)
    abs_errors = {'AB2': np.abs(Y_ab2 - Y_true), 'AB3': np.abs(Y_ab3 - Y_true), 'AB4': np.abs(Y_ab4 - Y_true), 'RK4': np.abs(Y_rk4 - Y_true)}
    for name, error in abs_errors.items():
        fig2.add_trace(go.Scatter(x=T, y=error, name=name, line=dict(width=2), mode='lines+markers', marker=dict(size=3)), row=1, col=1)
    
    rel_errors = {
        'AB2': np.where(np.abs(Y_true) > 1e-10, np.abs((Y_ab2 - Y_true) / Y_true) * 100, 0),
        'AB3': np.where(np.abs(Y_true) > 1e-10, np.abs((Y_ab3 - Y_true) / Y_true) * 100, 0),
        'AB4': np.where(np.abs(Y_true) > 1e-10, np.abs((Y_ab4 - Y_true) / Y_true) * 100, 0),
        'RK4': np.where(np.abs(Y_true) > 1e-10, np.abs((Y_rk4 - Y_true) / Y_true) * 100, 0)
    }
    for name, error in rel_errors.items():
        fig2.add_trace(go.Scatter(x=T, y=error, name=name, line=dict(width=2), mode='lines+markers', marker=dict(size=3), showlegend=False), row=2, col=1)
    
    type_err_x = "log" if error_chart_type in ["Semi-log x", "Log-log"] else "linear"
    type_err_y = "log" if error_chart_type in ["Semi-log y", "Log-log"] else "linear"
    fig2.update_xaxes(title_text="Thời gian t", type=type_err_x, showgrid=True, gridcolor='lightgray', row=1, col=1)
    fig2.update_xaxes(title_text="Thời gian t", type=type_err_x, showgrid=True, gridcolor='lightgray', row=2, col=1)
    fig2.update_yaxes(title_text="Sai số", type=type_err_y, showgrid=True, gridcolor='lightgray', row=1, col=1)
    fig2.update_yaxes(title_text="Sai số %", type=type_err_y, showgrid=True, gridcolor='lightgray', row=2, col=1)
    fig2.update_layout(height=550, showlegend=True, template='plotly_white', plot_bgcolor='rgba(255,255,255,0.8)', paper_bgcolor='rgba(255,255,255,0.9)')
    st.plotly_chart(fig2, use_container_width=True, key="error_chart")
    
    # Hướng dẫn tải ảnh cho biểu đồ sai số
    with st.expander("📷 Hướng dẫn tải ảnh biểu đồ sai số"):
        st.markdown("""
        **Các cách tải ảnh biểu đồ sai số:**
        
        1. **Click chuột phải** vào biểu đồ → Chọn:
           - `Download image as PNG` 
           - `Download image as SVG` (khuyến nghị cho chất lượng cao)
        
        2. **Sử dụng thanh công cụ** phía trên bên phải biểu đồ:
           - Click vào biểu tượng **máy ảnh** 📷
           - Chọn định dạng mong muốn
        
        3. **Phím tắt:** Nhấn `Ctrl+S` hoặc `Cmd+S` khi đang focus vào biểu đồ
        
        💡 **Lưu ý:** Định dạng SVG là lựa chọn tốt nhất cho báo cáo khoa học và in ấn
        """)

# --- MA TRẬN KẾT QUẢ ---
st.markdown("""
<div class="section-header">
    <h3>📋 Ma trận kết quả số chi tiết</h3>
</div>
""", unsafe_allow_html=True)

df_data = {"Nút thời gian (t)": T, "Nghiệm số RK4": Y_rk4, "Nghiệm số AB4": Y_ab4}
if has_exact and Y_true is not None:
    df_data["Nghiệm Giải tích"] = Y_true
    df_data["Sai số tuyệt đối AB4"] = abs(Y_ab4 - Y_true)
    df_data["Sai số tương đối AB4 (%)"] = np.where(np.abs(Y_true) > 1e-10, abs((Y_ab4 - Y_true) / Y_true) * 100, 0)

df_matrix = pd.DataFrame(df_data)
df_display = df_matrix.copy()
for col in df_display.columns:
    if col == "Nút thời gian (t)":
        df_display[col] = df_display[col].apply(lambda x: f"{x:.2f}")
    elif "Sai số" in col:
        df_display[col] = df_display[col].apply(lambda x: f"{x:.6e}" if not pd.isna(x) and x != 0 else "0.000000")
    else:
        df_display[col] = df_display[col].apply(lambda x: f"{x:.6f}" if not pd.isna(x) else "NaN")

# ===== HIỂN THỊ BẢNG DỮ LIỆU (bỏ background_gradient để tránh lỗi matplotlib) =====
styled_df = df_display
st.dataframe(styled_df, use_container_width=True, height=400)

# --- XUẤT DỮ LIỆU ---
st.markdown("""
<div class="section-header">
    <h3>💾 Xuất dữ liệu</h3>
</div>
""", unsafe_allow_html=True)

col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)

with col_dl1:
    csv = df_matrix.to_csv(index=False, float_format='%.12f').encode('utf-8-sig')
    st.download_button(label="📥 Tải CSV", data=csv, file_name=f"nghiem_AB_{N_use}_{Tmax_use}.csv", mime="text/csv", use_container_width=True)

with col_dl2:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_matrix.to_excel(writer, sheet_name='Nghiem so', float_format='%.12f')
    excel_data = output.getvalue()
    st.download_button(label="📊 Tải Excel", data=excel_data, file_name=f"nghiem_AB_{N_use}_{Tmax_use}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

with col_dl3:
    def format_error(val):
        if np.isnan(val) or np.isinf(val): return 'N/A'
        return f'{val:.6e}'
    report = f"""
BÁO CÁO KẾT QUẢ ADAMS-BASHFORTH
================================
Phương trình: {equation_display}
Số bước N: {N_use}
Bước nhảy h: {h_use:.10f}
Khoảng [t0, Tmax]: [0.0, {Tmax_use}]
y0 = {y0_use}

KẾT QUẢ:
- AB2: Sai số max = {format_error(err_ab2)}, Thời gian = {t_ab2:.6f}s
- AB3: Sai số max = {format_error(err_ab3)}, Thời gian = {t_ab3:.6f}s
- AB4: Sai số max = {format_error(err_ab4)}, Thời gian = {t_ab4:.6f}s
- RK4: Sai số max = {format_error(err_rk4)}, Thời gian = {t_rk4:.6f}s
    """
    st.download_button(label="📄 Tải báo cáo", data=report, file_name=f"bao_cao_AB_{N_use}_{Tmax_use}.txt", mime="text/plain", use_container_width=True)

with col_dl4:
    status_color = "linear-gradient(135deg, #00b09b 0%, #96c93d 100%)" if not has_diverged else "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
    status_text = "✅ Ổn định" if not has_diverged else "⚠️ Phân kỳ!"
    st.markdown(f"""
    <div style="background: {status_color}; padding: 0.8rem; border-radius: 12px; text-align: center; border: none; box-shadow: 0 4px 15px rgba(0,176,155,0.3);">
        <p style="margin: 0; color: white; font-weight: 600;">{status_text}</p>
        <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 0.8rem;">Độ chính xác 12 số</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🌸 Đề tài: Xây dựng phương pháp Adams-Bashforth | Phát triển bằng Streamlit</p>
    <p class="sub-text">📚 Mô phỏng hiện tượng vật lý đời thực | 📊 Biểu đồ tương tác đa hướng | 💾 Xuất báo cáo nâng cao</p>
</div>
""", unsafe_allow_html=True)
