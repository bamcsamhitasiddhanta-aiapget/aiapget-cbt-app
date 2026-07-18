import os
import time

import streamlit as st

DEVELOPER_MODE = os.getenv("DEVELOPER_MODE", "False") == "True"

if DEVELOPER_MODE:
    show_monitor()

# ----------------------------------------
# Start timer
# ----------------------------------------


def start_page_timer():
    st.session_state["_page_start"] = time.perf_counter()


# ----------------------------------------
# End timer
# ----------------------------------------


def end_page_timer():

    if "_page_start" not in st.session_state:
        return

    elapsed = time.perf_counter() - st.session_state["_page_start"]

    st.session_state["_page_time"] = elapsed


# ----------------------------------------
# Query counter
# ----------------------------------------


def increment_query():

    if "_query_count" not in st.session_state:
        st.session_state["_query_count"] = 0

    st.session_state["_query_count"] += 1


# ----------------------------------------
# Connection counter
# ----------------------------------------


def increment_connection():

    if "_connection_count" not in st.session_state:
        st.session_state["_connection_count"] = 0

    st.session_state["_connection_count"] += 1


# ----------------------------------------
# Reset counters
# ----------------------------------------


def reset_monitor():

    st.session_state["_query_count"] = 0
    st.session_state["_connection_count"] = 0


# ----------------------------------------
# Sidebar
# ----------------------------------------


def show_monitor():

    st.sidebar.divider()

    st.sidebar.subheader("🔧 Developer")

    st.sidebar.metric(
        "Page Load",
        f"{st.session_state.get('_page_time', 0):.3f} sec",
    )

    st.sidebar.metric(
        "Queries",
        st.session_state.get("_query_count", 0),
    )

    st.sidebar.metric(
        "Connections",
        st.session_state.get("_connection_count", 0),
    )

    st.sidebar.metric(
        "Session Keys",
        len(st.session_state),
    )


def profile(name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start

            if "_function_times" not in st.session_state:
                st.session_state["_function_times"] = {}

            st.session_state["_function_times"][name] = elapsed
            return result

        return wrapper

    return decorator
