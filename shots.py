# ヘッドレスChromeは窓幅に下限があるため、幅固定のiframeに入れて撮る。
# ボード用スクショ（390×844）をヘッドレスChromeで撮る。python3 shots.py [幅]  ※ python3 -m http.server 8765 を別で起動しておく
import subprocess,sys,os
from PIL import Image
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
w=int(sys.argv[1]) if len(sys.argv)>1 else 390
out="shots" if w==390 else f"/tmp/aip{w}"
os.makedirs(out,exist_ok=True)
open("_frame.html","w").write('<body style="margin:0"><iframe id=f style="border:0;height:844px"></iframe><script>const[s,w]=location.search.slice(1).split("&");f.style.width=w+"px";f.src=s</script>')
for v in ["v1","v2","v3","v4","v5"]:
  png=f"/tmp/aip_{v}_{w}.png"
  subprocess.run([CH,"--headless=new","--hide-scrollbars","--disable-gpu","--window-size=800,844","--virtual-time-budget=4000",f"--screenshot={png}",f"http://localhost:8765/_frame.html?{v}.html&{w}"],capture_output=True)
  Image.open(png).convert("RGB").crop((0,0,w,844)).save(f"{out}/{v}.jpg",quality=86)
os.remove("_frame.html")
print("shots",out)
