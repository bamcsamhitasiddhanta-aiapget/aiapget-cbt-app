import streamlit as st


def section_title(title):
    st.markdown(
        f"""
        <h2 style="
            color:#1565C0;
            font-weight:700;
            margin-bottom:10px;
        ">
            {title}
        </h2>
        """,
        unsafe_allow_html=True,
    )


def stat_card(title, value, color="#1565C0"):

    st.markdown(
        f"""
        <div style="
            background:white;
            border-radius:14px;
            padding:18px;
            text-align:center;
            border-left:8px solid {color};
            box-shadow:0 3px 12px rgba(0,0,0,.08);
            margin-bottom:12px;
        ">

            <div style="
                font-size:34px;
                font-weight:bold;
                color:{color};
            ">
                {value}
            </div>

            <div style="
                font-size:15px;
                color:#666;
            ">
                {title}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )
