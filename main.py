
import streamlit as st
import tempfile
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from PIL import Image
import io

st.set_page_config(page_title="HTML to PNG (Selenium)", layout="centered")
st.title("HTML → PNG Converter")

st.write("Paste your HTML below, render it via Selenium, and download a screenshot.")

user_html = st.text_area(
    "Enter HTML here", height=300,
    value="<h1>Hello, Streamlit + Selenium!</h1>"
)

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--headless")
options.add_argument("--window-size=1024,800")

@st.cache_resource
def get_driver():
    return webdriver.Chrome(
        service=Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        ),
        options=options,
    )

def render_html_and_screenshot(html_string: str) -> bytes:
    with tempfile.TemporaryDirectory() as tmpdir:
        html_path = os.path.join(tmpdir, "temp.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_string)
        driver = get_driver()
        driver.get(f"file://{html_path}")
        screenshot_path = os.path.join(tmpdir, "screenshot.png")
        driver.save_screenshot(screenshot_path)
        # Read as bytes *before* the directory is deleted
        with open(screenshot_path, "rb") as img_file:
            img_bytes = img_file.read()
        return img_bytes

if st.button("Render & Screenshot HTML"):
    img_bytes = render_html_and_screenshot(user_html)
    st.success("🎉 Screenshot captured!")
    st.image(img_bytes, caption="Rendered HTML Screenshot", use_column_width=True)
    st.download_button(
        label="Download PNG",
        data=img_bytes,
        file_name="rendered_screenshot.png",
        mime="image/png"
    )

