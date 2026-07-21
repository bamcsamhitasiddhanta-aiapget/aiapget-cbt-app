import streamlit as st

out = st.components.v2.component(
    "timer-component.timer_component",
    js="index-*.js",
    html='<div class="react-root"></div>',
)


def on_expired_change():
    """Called when expired changes."""
    pass


def timer_component(end_time: int, total_time: int, key=None):

    value = out(
        key=key,
        data={
            "end_time": end_time,
            "total_time": total_time,
        },
        default={
            "expired": False,
        },
        on_expired_change=on_expired_change,
    )

    return value
