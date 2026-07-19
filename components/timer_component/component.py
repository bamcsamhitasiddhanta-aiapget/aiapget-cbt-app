import os

import streamlit.components.v1 as components

_RELEASE = True

if _RELEASE:
    _component_func = components.declare_component(
        "timer_component",
        path=os.path.join(os.path.dirname(__file__), "frontend"),
    )
else:
    _component_func = components.declare_component(
        "timer_component",
        url="http://localhost:3001",
    )


def timer_component():
    return _component_func(default=False)
