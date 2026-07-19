const button = document.getElementById("btn");

button.addEventListener("click", () => {

    Streamlit.setComponentValue(true);

});

Streamlit.setFrameHeight(60);