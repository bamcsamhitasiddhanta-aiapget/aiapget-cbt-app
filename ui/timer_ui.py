def get_timer_state(remaining_seconds, total_seconds):
    """
    Returns timer display information.
    """

    if total_seconds <= 0:
        ratio = 0
    else:
        ratio = remaining_seconds / total_seconds

    percent = int(ratio * 100)

    if ratio > 0.50:
        color = "#22c55e"
        status = "Plenty of Time"

    elif ratio > 0.25:
        color = "#eab308"
        status = "Half Time Remaining"

    elif ratio > 0.10:
        color = "#f97316"
        status = "Finish Up"

    else:
        color = "#ef4444"
        status = "Hurry!"

    return {
        "ratio": ratio,
        "percent": percent,
        "color": color,
        "status": status,
    }


def timer_card(timer_info, remaining_seconds):
    """
    Returns HTML for the timer card.
    """

    hours = remaining_seconds // 3600
    minutes = (remaining_seconds % 3600) // 60
    seconds = remaining_seconds % 60

    if hours > 0:
        time_text = f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        time_text = f"{minutes:02}:{seconds:02}"

    width = timer_info["percent"]

    return f"""
<div style="
position:sticky;
top:10px;
z-index:999;

background:white;
border-radius:12px;
padding:15px;
box-shadow:0 2px 8px rgba(0,0,0,.08);
border-left:6px solid {timer_info['color']};
margin-bottom:15px;
">

<div style="
font-size:15px;
font-weight:bold;
color:#444;">
⏱ TIME LEFT
</div>

<div style="
font-size:34px;
font-weight:700;
text-align:center;
margin-top:8px;
margin-bottom:8px;
color:{timer_info['color']};
">
{time_text}
</div>

<div style="
height:10px;
background:#eeeeee;
border-radius:10px;
overflow:hidden;
">

<div style="
width:{width}%;
height:100%;
background:{timer_info['color']};
transition:width .4s ease;
">
</div>

</div>

<div style="
margin-top:10px;
font-weight:bold;
color:{timer_info['color']};
text-align:center;
">

{timer_info["status"]}

</div>

</div>
"""