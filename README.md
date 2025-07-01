# Streamlit HTML to PNG App

A simple Streamlit app that takes HTML code and renders it as a PNG image using Python's [html2image](https://pypi.org/project/html2image/) library.

## Features
- Enter or paste HTML code and instantly see the rendered PNG image.
- Accepts `html` as a GET parameter to pre-fill the text area.
- Download the generated PNG directly from the app.
- No backend server needed; everything runs in Python!

## Running locally

```bash
pip install -r requirements.txt
streamlit run main.py
```

## Deploying on Streamlit Community Cloud
- Push all these files to a GitHub repo
- Create a new app on [streamlit.io/cloud](https://streamlit.io/cloud) using the repo
- The app should "just work" (no custom setup needed)

## File Structure

```
project-root/
├── main.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml (optional)
```

---

## Notes
- `html2image` uses a headless browser to generate the PNG. Streamlit Cloud has Chromium pre-installed, so extra setup is not needed.
- If you want to style the image (size, width, background), see the `Html2Image` documentation for options.
