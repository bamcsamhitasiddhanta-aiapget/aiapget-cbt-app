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
        padding-top:1.2rem;
        padding-bottom:1rem;
        padding-left:2rem;
        padding-right:2rem;
    }

    /* Buttons */
    div.stButton > button{
        width:100%;
        border-radius:10px;
        height:46px;
        font-size:16px;
        font-weight:600;
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
        padding:20px;
        border-radius:12px;
        background:white;
        border:1px solid #EAEAEA;
        box-shadow:0 2px 6px rgba(0,0,0,.05);
    }

    </style>
    """,
        unsafe_allow_html=True,
    )
