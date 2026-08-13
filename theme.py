import streamlit as st


def apply_theme():
    st.markdown(
        """
    <style>

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Reduce top whitespace */
    .block-container{
        padding-top:1rem;
        padding-bottom:1rem;
        padding-left:2rem;
        padding-right:2rem;
        max-width:1600px;
    }

    .stApp{
       background:#F5F7FB;
    }
    /* Buttons */
    div.stButton > button{
        width:100%;
        height:48px;
        border-radius:12px;
        font-size:15px;
        font-weight:600;
        border:1px solid #D1D5DB;
        background:#FFFFFF;
        transition:all .2s ease;
    }

    div.stButton > button:hover{
        border-color:#2563EB;
        box-shadow:0 4px 10px rgba(37,99,235,.15);
    }

    /* Input boxes */
    div[data-baseweb="input"]{
        border-radius:10px;
    }

    /* Metrics */
    div[data-testid="metric-container"]{
        border-radius:12px;
        padding:12px;
        border:1px solid #E6E6E6;
        background:#FAFAFA;
    }

    /* Cards */
    .card{
        background:#FFFFFF;
        border:1px solid #E5E7EB;
        border-radius:16px;
        padding:18px;
        margin-bottom:18px;
        box-shadow:0 6px 16px rgba(0,0,0,.06);
    }

    /* ===========================================
        DASHBOARD CARD
    =========================================== */

    .dashboard-card{
        background:#FFFFFF;
        border:1px solid #E5E7EB;
        border-radius:16px;
        padding:18px;
        margin-bottom:18px;
        box-shadow:0 6px 16px rgba(0,0,0,.06);
    }

    .dashboard-title{
        font-size:20px;
        font-weight:700;
        color:#2F3640;
        text-align:center;
        margin-top:0;
        margin-bottom:10px;
        padding-top:0;
    }

    .dashboard-subtitle{
        font-size:18px;
        font-weight:600;
        color:#374151;
        margin-bottom:12px;
    }

    .dashboard-divider{
        border-top:1px solid #ECEFF5;
        margin:16px 0;
    }

    /* ===========================================
       EXAM PROGRESS CARD
    =========================================== */

    .progress-card{
        background:#FFFFFF;
        border:1px solid #E5E7EB;
        border-radius:16px;
        padding:18px;
        margin-bottom:18px;
        box-shadow:0 6px 16px rgba(15,23,42,.06);
    }

    .progress-header{
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:14px;
        font-size:18px;
        font-weight:700;
        color:#2F3640;
    }

    .progress-percentage{
        font-size:18px;
        font-weight:700;
        color:#2563EB;
    }

    .progress-track{
        width:100%;
        height:10px;
        background:#E5E7EB;
        border-radius:999px;
        overflow:hidden;
    }

    .progress-fill{
        height:100%;
        background:#2563EB;
        border-radius:999px;
        transition:width .3s ease;
    }

    .progress-footer{
        display:flex;
        justify-content:space-between;
        margin-top:12px;
        font-size:13px;
        color:#6B7280;
    }

    /* ===========================================
       QUESTION SUMMARY
    =========================================== */

    .summary-title{
        font-size:20px;
        font-weight:700;
        color:#2F3640;
        margin-top:20px;
        margin-bottom:14px;
    }

    .summary-grid{
        display:grid;
        grid-template-columns:1fr 1fr;
        gap:10px;
        margin-bottom:18px;
    }

    .summary-item{
        background:#FFFFFF;
        border:1px solid #E5E7EB;
        border-radius:12px;
        padding:12px;
        min-height:72px;
        box-sizing:border-box;
    }

    .summary-status{
        display:flex;
        align-items:center;
        gap:7px;
        font-size:12px;
        font-weight:600;
        color:#4B5563;
    }

    .status-dot{
        width:10px;
        height:10px;
        border-radius:3px;
        display:inline-block;
    }

    .answered-dot{
        background:#10B981;
    }

    .not-answered-dot{
        background:#F97316;
    }

    .review-dot{
        background:#8B5CF6;
    }

    .not-visited-dot{
        background:#D8BFE8;
    }

    .summary-number{
        font-size:25px;
        font-weight:700;
        color:#1F2937;
        margin-top:5px;
    }

    /* ===========================================
       QUESTION PALETTE
    =========================================== */

    .palette-title{
        font-size:19px;
        font-weight:700;
        color:#2F3640;
        margin-top:0;
        margin-bottom:10px;
    }
    /* Palette buttons */

    div.stButton > button{
        transition:
            transform .15s ease,
            box-shadow .15s ease,
            background .15s ease;
    }

    /*
       Palette buttons are deliberately compact.
       This allows many questions to fit vertically.
    */

    div.stButton > button[kind="secondary"]{
        min-height:42px;
    }

   
    </style>
    """,
        unsafe_allow_html=True,
    )


def dashboard_card_start(title):
    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="dashboard-title">
                {title}
            </div>
        """,
        unsafe_allow_html=True,
    )


def dashboard_card_end():
    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )
