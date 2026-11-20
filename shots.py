# ヘッドレスChromeは窓幅に下限があるため、幅固定のiframeに入れて撮る。
# ボード用スクショ（390×844）をヘッドレスChromeで撮る。python3 shots.py [幅]  ※ python3 -m http.server 8765 を別で起動しておく
import subprocess,sys,os
from PIL import Image
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
w=int(sys.argv[1]) if len(sys.argv)>1 else 390
out="shots" if w==390 else f"/tmp/aip{w}"
os.makedirs(out,exist_ok=True)
open("_frame.html","w").write('<body style="margin:0"><iframe id=f style="border:0;height:844px"></iframe><script>const[s,w]=location.search.slice(1).split("&");f.style.width=w+"px";f.src=s</script>')
for v in [f"v{i}" for i in range(1,11)]:
  png=f"/tmp/aip_{v}_{w}.png"
  subprocess.run([CH,"--headless=new","--hide-scrollbars","--disable-gpu","--window-size=800,844","--virtual-time-budget=4000",f"--screenshot={png}",f"http://localhost:8765/_frame.html?{v}.html&{w}"],capture_output=True)
  Image.open(png).convert("RGB").crop((0,0,w,844)).save(f"{out}/{v}.jpg",quality=86)
os.remove("_frame.html")
print("shots",out)
# ボードのOGP（黒地＋白太字見出し＋紫の短い下線＋v6〜v10の実画面を横一列）。og.png は上書きしない（iPhoneのキャッシュ回避で新しい名前）
if w==390:
  from PIL import ImageDraw,ImageFont
  og=Image.new("RGB",(1200,630),(20,18,23));d=ImageDraw.Draw(og)
  d.text((60,52),"AIポートフォリオ 追加5案の見比べ",font=ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc",58),fill="white")
  d.rectangle((62,146,62+72,146+6),fill=(103,69,183))
  cw,gap=200,25
  for i,v in enumerate(["v6","v7","v8","v9","v10"]):
    sh=Image.open(f"shots/{v}.jpg").resize((cw,cw*844//390),Image.LANCZOS).crop((0,0,cw,630-190))
    m=Image.new("L",sh.size,0);ImageDraw.Draw(m).rounded_rectangle((0,0,cw-1,sh.height+20),12,fill=255)
    og.paste(sh,(60+i*(cw+gap),190),m)
  og.save("og-board2.png",optimize=True);print("og-board2.png")
