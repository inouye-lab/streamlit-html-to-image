import streamlit as st
from html2image import Html2Image
import tempfile
import base64
import os

st.set_page_config(page_title="HTML to PNG Converter", layout="centered")
st.title("HTML to PNG Converter")

tab1, tab2 = st.tabs(["Input HTML", "About"])
with tab2:
    st.markdown("""
    This app takes HTML input (via GET or POST data) and renders it as a PNG image using [html2image](https://pypi.org/project/html2image/).
    - Paste your HTML code below, or call this endpoint with your HTML as GET or POST data.
    """)

with tab1:
    html_input = st.text_area("Enter HTML to convert to PNG:", height=250)
    url_params = st.experimental_get_query_params()
    if 'html' in url_params and not html_input:
        html_input = url_params['html'][0]
        st.info("Loaded HTML from GET parameters.")

    png_data = None

    if st.button("Convert to PNG"):
        if not html_input.strip():
            st.warning("Please provide HTML input.")
        else:
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    hti = Html2Image(output_path=tmpdir)
                    hti.screenshot(html_str=html_input, save_as='output.png')
                    image_path = os.path.join(tmpdir, 'output.png')
                    with open(image_path, "rb") as image_file:
                        png_data = image_file.read()
                st.success("Image generated successfully!")
            except Exception as e:
                st.error(f"Failed to render image: {e}")

    if png_data:
        st.image(png_data, caption="Rendered PNG", use_column_width=True)
        b64 = base64.b64encode(png_data).decode()
        href = f'<a href="data:image/png;base64,{b64}" download="rendered.png">Download PNG</a>'
        st.markdown(href, unsafe_allow_html=True)
