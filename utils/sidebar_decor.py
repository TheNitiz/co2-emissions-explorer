import streamlit as st
import requests
from streamlit_lottie import st_lottie


@st.cache_data
def load_lottie(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except (requests.exceptions.RequestException, ValueError):
        return None

def add_sidebar_decoration():
    # st.sidebar.markdown("---")
    lottie_animation = load_lottie("https://lottie.host/40651142-2d9f-4cef-9f4d-9e0f84e100b8/P5MF95xg5d.json")
    if lottie_animation:
        with st.sidebar:
            st_lottie(lottie_animation, height=180, key="sidebar_anim", loop=True, speed=0.8)
    st.sidebar.markdown(
        "<p style='text-align:center; font-size:0.75rem; color:#888;'>Tracking emissions since 1750</p>",
        unsafe_allow_html=True,
    )