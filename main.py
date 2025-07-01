import streamlit as st
import tempfile, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

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

def render_html_and_screenshot(html_string: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        html_path = os.path.join(tmpdir, "temp.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_string)
        driver = get_driver()
        driver.get(f"file://{html_path}")
        screenshot_path = os.path.join(tmpdir, "screenshot.png")
        driver.save_screenshot(screenshot_path)
        return screenshot_path

if st.button("Render & Screenshot HTML"):
    screenshot_path = render_html_and_screenshot(user_html)
    st.success("🎉 Screenshot captured!")
    st.image(screenshot_path, caption="Rendered HTML Screenshot", use_column_width=True)
    with open(screenshot_path, "rb") as file:
        st.download_button(
            label="Download PNG",
            data=file,
            file_name="rendered_screenshot.png",
            mime="image/png"
        )
