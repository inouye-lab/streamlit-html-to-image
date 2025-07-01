from fastapi import FastAPI, Query, Request, Response
from fastapi.responses import StreamingResponse, HTMLResponse
import tempfile, os, io, base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

app = FastAPI()

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--headless")
options.add_argument("--window-size=1024,800")

def get_driver():
    return webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=options,
    )

def html_to_png_bytes(html_string: str) -> bytes:
    with tempfile.TemporaryDirectory() as tmpdir:
        html_path = os.path.join(tmpdir, "temp.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_string)
        driver = get_driver()
        driver.get(f"file://{html_path}")
        screenshot_path = os.path.join(tmpdir, "screenshot.png")
        driver.save_screenshot(screenshot_path)
        with open(screenshot_path, "rb") as img_file:
            return img_file.read()

@app.get("/", response_class=HTMLResponse)
def gui():
    return """
    <html>
    <head><title>HTML → PNG Screenshot</title></head>
    <body>
      <h2>HTML → PNG Screenshot (API & GUI)</h2>
      <form action="/gui_screenshot" method="post">
        <textarea name="html" rows="10" cols="80" placeholder="<h1>Hello!</h1>"></textarea><br>
        <button type="submit">Get Screenshot</button>
      </form>
      <h4>API Usage:</h4>
      <ul>
        <li>GET <code>/screenshot?html=... (raw URL-encoded HTML)</code></li>
        <li>GET <code>/screenshot_base64?html=... (base64-encoded HTML)</code></li>
      </ul>
    </body>
    </html>
    """

@app.post("/gui_screenshot")
async def gui_screenshot(request: Request):
    form = await request.form()
    html = form.get("html", "")
    try:
        img_bytes = html_to_png_bytes(html)
    except Exception as e:
        return HTMLResponse(f"Error: {e}", status_code=400)
    img_b64 = base64.b64encode(img_bytes).decode()
    html_out = f"""
    <html>
      <head><title>Screenshot Result</title></head>
      <body>
        <h2>Screenshot</h2>
        <img src="data:image/png;base64,{img_b64}" /><br>
        <a download="screenshot.png" href="data:image/png;base64,{img_b64}">Download PNG</a>
        <hr>
        <a href="/">Back</a>
      </body>
    </html>
    """
    return HTMLResponse(html_out)

@app.get("/screenshot")
def screenshot_get(html: str = Query(..., description="Raw URL-encoded HTML")):
    try:
        img_bytes = html_to_png_bytes(html)
    except Exception as e:
        return Response(str(e), status_code=400)
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")

@app.get("/screenshot_base64")
def screenshot_base64(html: str = Query(..., description="Base64-encoded HTML")):
    try:
        html_decoded = base64.urlsafe_b64decode(html).decode("utf-8")
        img_bytes = html_to_png_bytes(html_decoded)
    except Exception as e:
        return Response(str(e), status_code=400)
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")
