
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import tempfile
import base64
import os
import shutil

st.set_page_config(page_title="HTML to PNG Converter (Selenium)", layout="centered")
st.title("HTML to PNG Converter (Selenium)")

def get_chromium_bin():
    candidates = [
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome"
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

@st.cache_resource(show_spinner=False)
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=800,600")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chromium_bin = get_chromium_bin()
    if chromium_bin:
        options.binary_location = chromium_bin
    chromedriver_path = shutil.which("chromedriver")
    if chromedriver_path:
        service = Service(executable_path=chromedriver_path)
    else:
        service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

tab1, tab2 = st.tabs(["Input HTML", "About"])
with tab2:
    st.markdown("""
    This app takes HTML input and renders it as a PNG image using Selenium and headless Chrome.
    - Paste your HTML code below, or call this endpoint with your HTML as a `GET` parameter (e.g., `?html=...`).
    - Useful for rendering HTML snippets or quick preview screenshots.
    - **Note:** For best results, use valid HTML.
    """)

with tab1:
    html_input = st.text_area("Enter HTML to convert to PNG:", height=250)
    url_params = st.experimental_get_query_params()
    if 'html' in url_params and not html_input:
        html_input = url_params['html'][0]
        st.info("Loaded HTML from GET parameters.")

    png_data = None

    if st.button("Convert to PNG (Selenium)"):
        if not html_input.strip():
            st.warning("Please provide HTML input.")
        else:
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    driver = get_driver()
                    tmp_html = os.path.join(tmpdir, "page.html")
                    with open(tmp_html, "w") as f:
                        f.write(html_input)
                    driver.get(f"file://{tmp_html}")
                    driver.implicitly_wait(2)
                    png_data = driver.get_screenshot_as_png()
                    driver.quit()
                st.success("Image generated successfully!")
            except Exception as e:
                st.error(f"Failed to render image: {e}")

    if png_data:
        st.image(png_data, caption="Rendered PNG (Selenium)", use_column_width=True)
        b64 = base64.b64encode(png_data).decode()
        href = f'<a href="data:image/png;base64,{b64}" download="rendered.png">Download PNG</a>'
        st.markdown(href, unsafe_allow_html=True)
