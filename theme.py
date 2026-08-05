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

    </style>
    """,
        unsafe_allow_html=True,
    )
