# 正本 logo-icon-final.webp（描き直し禁止）から 切り出し・縮小・背景処理だけで icon/favicon/apple-touch/og を作る。python3 make_assets.py
from PIL import Image, ImageDraw, ImageFont
import os
SRC=os.path.expanduser("~/ai-portfolio-assets/logo-icon-final.webp")
im=Image.open(SRC).convert("RGB")
# 紫の画素（R<150,B>150）の外接矩形＝角丸四角
px=im.load();W,H=im.size
xs=[x for x in range(0,W,2) if any(px[x,y][0]<150 and px[x,y][2]>150 for y in range(0,H,8))]
ys=[y for y in range(0,H,2) if any(px[x,y][0]<150 and px[x,y][2]>150 for x in range(0,W,8))]
I=10;box=(min(xs)+I,min(ys)+I,max(xs)+1-I,max(ys)+1-I)  # 縁の白にじみを避けて内側へ
sq=im.crop(box);s=max(sq.size);sq=sq.resize((s,s),Image.LANCZOS)  # ほぼ正方形。ずれは数px
vio=sq.getpixel((s//2,int(s*.93)))  # 下端付近の地色
R=int(s*.15)
def rounded(n,rr=R):
    big=sq.resize((n*4,n*4),Image.LANCZOS)
    m=Image.new("L",big.size,0);ImageDraw.Draw(m).rounded_rectangle((0,0,n*4-1,n*4-1),rr*n*4//s,fill=255)
    big.putalpha(m);return big.resize((n,n),Image.LANCZOS)
def bleed(n):  # 角も地色で塗る（iOSが自前で角丸にするため）
    bg=Image.new("RGB",(s,s),vio);r=rounded(s,int(s*.2));bg.paste(r,(0,0),r);return bg.resize((n,n),Image.LANCZOS)
os.makedirs("assets",exist_ok=True)
rounded(256).save("assets/icon.png")
# ファビコンは「Ai」だけを拡大して使う（2026-11-24 ユウキ指示：小サイズでは下の PORTFOLIO が掠れて読めないため）
# sq 内の白字形を走査し、上の塊＝Ai の外接矩形を中心に正方形で切り出す（描き直しなし・切り出しと拡大だけ）
_sp=sq.resize((200,200),Image.LANCZOS);_pp=_sp.load()
def _ispurple(x,y):return _pp[x,y][0]<150 and _pp[x,y][2]>150
_ext=[]  # 行ごとの紫の範囲（角丸の外側の白を字形と誤認しないため）
for _y in range(200):
    _pxs=[x for x in range(200) if _ispurple(x,_y)]
    _ext.append((min(_pxs),max(_pxs)) if _pxs else (0,-1))
def _iswhite(x,y):
    _l,_r=_ext[y]
    return _l<=x<=_r and _pp[x,y][0]>225 and _pp[x,y][1]>225 and _pp[x,y][2]>225
_wrows=[y for y in range(200) if any(_iswhite(x,y) for x in range(200))]
_clusters=[];_st=_pr=_wrows[0]
for _v in _wrows[1:]:
    if _v-_pr>2:_clusters.append((_st,_pr));_st=_v
    _pr=_v
_clusters.append((_st,_pr))
_ay0,_ay1=_clusters[0]  # 最初の塊が Ai（下の塊が PORTFOLIO）
_axl=[x for y in range(_ay0,_ay1+1) for x in range(200) if _iswhite(x,y)]
_gx0,_gx1=min(_axl)/200*s,max(_axl)/200*s
_gy0,_gy1=_ay0/200*s,_ay1/200*s
_side=(_gx1-_gx0)*832/744  # 正本実測の比率：字形幅744に対し切り出し一辺832（余白最小）
_bx0=int((_gx0+_gx1)/2-_side/2);_by0=int((_gy0+_gy1)/2-_side/2)
aicrop=sq.crop((_bx0,_by0,_bx0+int(_side),_by0+int(_side)))
def rounded_from(img,n):  # 角丸は正本アイコンの実測比率 19%
    big=img.resize((n*4,n*4),Image.LANCZOS)
    m=Image.new("L",big.size,0);ImageDraw.Draw(m).rounded_rectangle((0,0,n*4-1,n*4-1),int(n*4*.19),fill=255)
    big=big.convert("RGBA");big.putalpha(m);return big.resize((n,n),Image.LANCZOS)
rounded_from(aicrop,512).save("favicon-ai.png")
aicrop.resize((180,180),Image.LANCZOS).save("assets/apple-touch-icon-ai.png")  # 角は iOS が丸めるので地のまま
# og 1200x630：紫地＋確定アイコン（白縁なし）＋サイト名
og=Image.new("RGB",(1200,630),vio);d=ImageDraw.Draw(og)
ic=rounded(360);ic2=Image.new("RGBA",(372,372),(0,0,0,0))
m=Image.new("L",(372,372),0);ImageDraw.Draw(m).rounded_rectangle((0,0,371,371),int(372*.165),fill=255)
ic2.paste((255,255,255,60),(0,0),m);ic2.paste(ic,(6,6),ic)  # 地色と同化しないよう細い白縁
og.paste(ic2,(110,129),ic2)
F="/System/Library/Fonts/ヒラギノ角ゴシック W{}.ttc"
d.text((560,232),"AIポートフォリオ",font=ImageFont.truetype(F.format(7),64),fill="white")
d.text((562,330),"AIで作ったロゴ・ページ・アプリ",font=ImageFont.truetype(F.format(4),32),fill=(232,224,250))
d.text((562,382),"作品ごとに使用AIを記載",font=ImageFont.truetype(F.format(4),26),fill=(214,202,244))
og.save("og.png",optimize=True)
# og-main 1200x630：og.png と同じ構図で地だけ白（ロゴタイルは紫のまま・白縁なし）。index.html の og:image
ow=Image.new("RGB",(1200,630),"white");dw=ImageDraw.Draw(ow);ow.paste(ic,(116,135),ic)
dw.text((560,232),"AIポートフォリオ",font=ImageFont.truetype(F.format(7),64),fill=vio)
dw.text((562,330),"AIで作ったロゴ・ページ・アプリ",font=ImageFont.truetype(F.format(4),32),fill=(51,51,56))
dw.text((562,382),"作品ごとに使用AIを記載",font=ImageFont.truetype(F.format(4),26),fill=(96,96,104))
ow.save("og-main.png",optimize=True)
print("box",box,"vio",vio)
# 「ロゴ」絞り込み用サムネ 800x500（16:10）。正本 assets/logos/ を切り抜き・縮小・配置だけ。地色は各ロゴの地に合わせる（紫は使わない）
from PIL import ImageChops
def trim(p,bg,cut=0):  # 地色との差が出る範囲で切り抜く（cut=下端の余計な線を落とす行数）
    im=Image.open(f"assets/logos/{p}").convert("RGB");im=im.crop((0,0,im.width,im.height-cut))
    d=ImageChops.difference(im,Image.new("RGB",im.size,bg)).convert("L").point(lambda v:255 if v>14 else 0)
    return im.crop(d.getbbox())
def fit(im,w,h):im=im.copy();im.thumbnail((w,h),Image.LANCZOS);return im
def logo_thumb(out,bg,parts):  # parts=[(画像,中心x,中心y)]
    c=Image.new("RGB",(800,500),bg)
    for im,cx,cy in parts:c.paste(im,(cx-im.width//2,cy-im.height//2))
    c.save(f"thumbs/{out}",quality=90)
W=(255,255,255)
typo=Image.eval(trim("anime-logo-red.webp",(248,248,248)),lambda v:255 if v>=243 else v)  # 地f8を白に寄せる
logo_thumb("logo-anime.webp",W,[(fit(typo,400,200),262,250),(fit(trim("mascot-sd78.webp",W),280,410),615,250)])
logo_thumb("logo-keiri.webp",W,[(fit(trim("keiri-kun-logo-final-aligned.webp",W),640,240),400,250)])
logo_thumb("logo-tadayomi.webp",(246,246,246),[(fit(trim("tadayomi-logo-flat1.png",(246,246,246),cut=7),560,400),400,250)])
