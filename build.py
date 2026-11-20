# v1〜v5.html を生成。python3 build.py
# 全案の土台＝タダヨミ v3（コンパクト型）の文法：48px級の薄いヘッダー／1行タイトル／小サムネの行リスト。
# 共通部品は common.css、案ごとの差分（密度・見せ方）だけを V[...]["css"] に書く。
BASE="https://yukitchy.github.io/ai-portfolio/"
HEAD='''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AIポートフォリオ {v}｜AIで作ったロゴ・ページ・アプリ</title>
<meta name="description" content="AIで設計・書き出ししたロゴ・ページ・アプリUIの実績集（試作{v}：{feat}）。">
<meta property="og:type" content="website">
<meta property="og:title" content="AIポートフォリオ {v}｜AIで作ったロゴ・ページ・アプリ">
<meta property="og:description" content="ChatGPT・Claudeなどを使い分けて作ったデザイン実績。作品ごとに使用AIを記載。">
<meta property="og:url" content="{base}{v}.html">
<meta property="og:image" content="{base}og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="stylesheet" href="common.css">
<style>{css}</style>
</head>
<body class="{v}">
'''
LOGO='<a class="hd" href="./{v}.html"><img src="assets/icon.png" alt="" width="{s}" height="{s}"><span class="site">AIポートフォリオ</span></a><a class="cta" href="#contact">仕事の相談</a>'
NOTE='<span class="note">試作版：作品データはサンプルです</span>'
FILTERS='<div class="filters"><div class="row" id="catRow" aria-label="種類で絞り込む"></div></div>'
LIST='<ul class="list" id="list"></ul>\n<p id="empty">この種類の作品はまだありません。</p>'
PROFILE='<section id="profile" class="prof"><h2>プロフィール</h2><p class="pn" id="pName"></p><p class="pr" id="pRole"></p><p class="pb" id="pBio"></p></section>'
CONTACT='<section id="contact" class="ct"><h2>お問い合わせ</h2><p class="cl">ロゴ1点から、ページ・アプリ画面まで相談できます。</p><a class="btn" id="pContact" href="#contact">仕事の相談をする</a><p class="cn" id="pNote"></p></section>'
FOOT='<footer>AIポートフォリオ 試作 {v} ／ 作品データはサンプルです ／ <a href="board.html">見比べボードに戻る</a></footer>'
TAIL='''
<script>{js}</script>
<script src="app.js"></script>
</body>
</html>
'''
STD='''<div class="wrap">
<header>{logo}</header>
<p class="proto">{note}</p>
<section class="works"><h2>作品<small><span id="count">–</span>件</small></h2>{filters}{list}</section>
{profile}
{contact}
{foot}
</div>'''
ROW='window.T={card:(it,i)=>`<li class="card${i===0?" first":""}"><span class="tl">${thumb(it)}</span><div class="b">${link(it,esc(it.title),"t")}<p class="d">${esc(it.desc)}</p>${tags(it)}</div></li>`};'
TINY='.card .ph{padding:2px}.card .ph span{display:none}.card .ph small{font-size:0;right:2px;bottom:2px;padding:0 3px}.card .ph small::after{content:"仮";font-size:10px}'
V={}
# ---------- v1 コンパクト・リスト（基準案）
V1CSS='''
.card{display:flex;gap:10px;padding:7px 10px;border-bottom:1px solid var(--line);align-items:center}
.card .tl{flex:0 0 80px;width:80px}
.card .th{border-radius:3px;border:1px solid var(--line)}
.card .b{min-width:0;flex:1}
'''
V["v1"]=dict(feat="タダヨミv3の文法そのままの行リスト（基準案）",s=32,body=STD,js=ROW,css=V1CSS)
# ---------- v2 コンパクト＋グリッド寄り
V["v2"]=dict(feat="サムネ少し大きめの2列。行リストとグリッドの中間",s=32,body=STD,
js='window.T={card:it=>`<li class="card"><span class="tl">${thumb(it)}</span>${link(it,esc(it.title),"t")}${tags(it)}</li>`};',css='''
.list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 8px;padding:8px 10px}
@media(min-width:600px){.list{grid-template-columns:repeat(3,minmax(0,1fr))}}
.card{min-width:0}
.card .th{border-radius:4px;border:1px solid var(--line)}
.card .ph span{font-size:13px;white-space:normal;-webkit-line-clamp:2;display:-webkit-box}
.card .t{margin-top:4px}
.card .tags{margin-top:3px}
''')
# ---------- v3 超コンパクト
V["v3"]=dict(feat="密度最大。最小サムネで10作品がほぼ1画面に入る",s=28,
body=STD.replace('<p class="proto">{note}</p>','<p class="who"><span>AIで作ったロゴ・ページ・アプリ</span>{note}</p>'),
js='window.T={card:it=>`<li class="card"><span class="tl">${thumb(it)}</span><div class="b">${link(it,esc(it.title),"t")}${tags(it)}</div></li>`};',css='''
header{height:44px}
.who{display:flex;align-items:center;gap:8px;padding:3px 10px;font-size:12px;color:var(--sub);white-space:nowrap;overflow:hidden}
.who .note{font-size:11px;padding:0 4px;margin-left:auto}
@media(max-width:359px){.who .note{display:none}}
h2{padding:3px 10px;font-size:13px}
.filters{padding:5px 10px}.chip{padding:1px 10px}
.card{display:flex;gap:8px;padding:5px 10px;border-bottom:1px solid var(--line);align-items:center}
.card .tl{flex:0 0 52px;width:52px}
.card .th{border-radius:2px;border:1px solid var(--line)}
.card .b{min-width:0;flex:1}
.card .t{line-height:1.35}
.card .tags{margin-top:1px}
.scope,.ai{font-size:11px;padding:0 4px;line-height:1.45}
'''+TINY)
# ---------- v4 コンパクト特集型
V["v4"]=dict(feat="先頭の1作品だけ大きく、残りはコンパクトリスト",s=32,body=STD,js=ROW,css='''
.card{display:flex;gap:10px;padding:7px 10px;border-bottom:1px solid var(--line);align-items:center}
.card .tl{flex:0 0 72px;width:72px}
.card .th{border-radius:3px;border:1px solid var(--line)}
.card .b{min-width:0;flex:1}
.card .d{display:none}
.card.first{display:block;padding:10px 10px 12px;border-bottom:2px solid var(--vio)}
.card.first .tl{width:100%}
.card.first .th{border-radius:6px}
.card.first .ph span{font-size:22px;white-space:normal}.card.first .ph small{font-size:12px}
.card.first .b{padding-top:8px}
.card.first .t{font-size:16px}
.card.first .t::before{content:"注目";color:#fff;background:var(--vio);font-size:11px;font-weight:700;border-radius:3px;padding:1px 6px;margin-right:6px;vertical-align:2px}
.card.first .d{display:block;font-size:13px;color:var(--ink);white-space:normal}
.card.first .tags{margin-top:5px}
''')
# ---------- v5 コンパクト・ミニマル
V["v5"]=dict(feat="罫線と文字で見せる。番号＋作品名の行、サムネは右端に小さく",s=28,
body=STD.replace("作品<small>","WORKS<small>"),js=ROW,css='''
header{border-bottom:1px solid var(--ink)}
.cta{background:none;color:var(--ink);border:1px solid var(--ink)}
h2{background:none;color:var(--ink);font-weight:300;letter-spacing:.24em;font-size:12px;padding:12px 12px 2px}
h2 small{letter-spacing:0}
.proto{padding:6px 12px 0}
.filters{padding:6px 12px;border-bottom:1px solid var(--ink)}
.row{gap:14px}
.chip{border:0;border-radius:0;background:none;color:var(--sub);padding:2px 0;font-weight:400}
.chip[aria-pressed=true]{background:none;color:var(--vio-d);font-weight:700;box-shadow:inset 0 -2px var(--vio)}
.list{counter-reset:n}
.card{display:flex;gap:10px;padding:8px 12px;border-bottom:1px solid var(--line);align-items:center;counter-increment:n}
.card::before{content:counter(n,decimal-leading-zero);font-size:12px;font-weight:300;color:var(--vio);flex:none;width:18px;font-variant-numeric:tabular-nums}
.card .b{min-width:0;flex:1}
.card .t{font-weight:600;font-size:14px}
.card .d{display:none}
.card .tl{flex:0 0 44px;width:44px;order:2}
.card .th{border-radius:2px}
.scope{background:none;padding:0 4px 0 0;color:var(--vio-d);font-weight:600}
.prof,.ct{padding:0 12px 14px}
.prof h2,.ct h2{border-top:1px solid var(--ink);margin:6px -12px 0;padding:12px 12px 6px}
.ct .btn{background:none;color:var(--ink);border:1px solid var(--ink)}
'''+TINY)

# ---------- v6〜v10：v1（確定土台）＋作品サムネが流れるヒーロー。流れは app.js が .flow に実サムネを詰める（common.css の .flow）
HD='<header>{logo}</header>'
def hero(html,keep=True):return STD.replace(HD,(HD if keep else "")+html)
# v6 ヒーロー全面に大きなサムネ1段＋暗幕、その上にヘッダーとタイトルを重ねる
V["v6"]=dict(feat="ヒーロー全面に作品が流れ、ロゴ・タイトルを重ねる",s=32,js=ROW,
body=hero('<div class="hero"><div class="flow" aria-hidden="true"></div><header>{logo}</header><p class="hc"><small>AIで作った</small>ロゴ・ページ・アプリ</p></div>',keep=False),css=V1CSS+'''
.hero{position:relative;height:clamp(196px,56vw,300px);overflow:hidden;background:var(--ink)}
.hero .flow{position:absolute;inset:0;--g:4px;--dur:110s}
.hero .tr,.hero .fi{height:100%}
.hero .fi{width:auto;aspect-ratio:16/10}
.hero .flow .th{height:100%;border-radius:0}
.hero .ph span{font-size:18px}.hero .ph small{font-size:11px}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(rgba(20,18,23,.62),rgba(20,18,23,.1) 38%,rgba(20,18,23,.2) 55%,rgba(20,18,23,.82))}
.hero header{position:relative;z-index:2;border:0}
.hero .site{color:#fff;font-weight:400}
.hc{position:absolute;z-index:2;left:12px;right:12px;bottom:14px;color:#fff;font-weight:800;font-size:clamp(21px,6.6vw,30px);line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hc small{display:block;font-size:12px;font-weight:400;letter-spacing:.24em;opacity:.85;margin-bottom:2px}
''')
# v7 ヘッダー直下に細い帯で1段だけ流す
V["v7"]=dict(feat="ヘッダー直下に細い帯で作品が1段流れる",s=32,js=ROW,
body=hero('<div class="flow band" aria-hidden="true"></div>'),css=V1CSS+'''
.band{--w:88px;--g:6px;--dur:90s;padding:6px 0;border-bottom:1px solid var(--line)}
.band .th{border:1px solid var(--line)}
''')
# v8 薄紫の地に2段、上下で逆方向に流す
V["v8"]=dict(feat="2段のサムネが上下で逆方向に流れる",s=32,js=ROW,
body=hero('<div class="duo" aria-hidden="true"><div class="flow"></div><div class="flow rev"></div></div>'),css=V1CSS+'''
.duo{background:var(--vio-l);padding:10px 0;display:grid;gap:8px}
.duo .flow{--w:124px;--g:8px;--dur:100s}
.duo .th{border-radius:4px;box-shadow:0 1px 3px rgba(40,20,90,.12)}
''')
# v9 白く沈めた流れの上に、大きな文字組だけを置く
V["v9"]=dict(feat="淡く沈めた流れの上に大きな文字組だけを置く",s=32,js=ROW,
body=hero('<div class="type"><div class="flow" aria-hidden="true"></div><p class="k">AIで作った</p><h1>ロゴ・ページ・アプリ</h1></div>'),css=V1CSS+'''
.type{position:relative;overflow:hidden;padding:30px 14px 26px}
.type .flow{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);--w:210px;--g:10px;--dur:120s;filter:grayscale(1)}
.type::before{content:"";position:absolute;inset:0;z-index:1;background:rgba(255,255,255,.8)}
.type .k,.type h1{position:relative;z-index:2}
.type .k{font-size:13px;font-weight:300;letter-spacing:.32em;color:var(--vio-d)}
.type h1{font-size:clamp(27px,8.4vw,44px);font-weight:800;line-height:1.2;letter-spacing:-.01em;margin-top:4px}
''')
# v10 流れは控えめ（小さく遅く）、差はリストの磨きでつける
V["v10"]=dict(feat="流れは控えめ。余白・区切り・タグの見せ方を磨いたリスト",s=32,js=ROW,
body=hero('<div class="flow mini" aria-hidden="true"></div>'),css=V1CSS+'''
.mini{--w:56px;--g:4px;--dur:140s;padding:5px 0}
.proto{padding:6px 14px 0}
h2{background:none;color:var(--ink);font-size:15px;padding:14px 14px 4px}
h2 small{font-weight:400}
.filters{padding:6px 14px 8px;border-bottom:0}
.chip{border-color:#d9d4e3;padding:3px 12px}
.card{gap:12px;padding:12px 14px;border-bottom:0}
.card+.card::before{content:"";position:absolute;top:0;left:110px;right:14px;border-top:1px solid var(--line)}
.card .tl{flex-basis:84px;width:84px}
.card .th{border-radius:4px;border:0;box-shadow:0 0 0 1px var(--line)}
.card .t{font-size:14px}
.tags{gap:4px;margin-top:5px}
.card:hover{background:#faf8fd}
.prof,.ct{padding-top:6px}
.prof p,.ct p{padding:0 14px}.btn{margin:0 14px}
footer{padding:16px 14px 32px}
''')

if __name__=="__main__":
  for v,d in V.items():
    body=d["body"].format(logo=LOGO.format(v=v,s=d["s"]),note=NOTE,filters=FILTERS,list=LIST,profile=PROFILE,contact=CONTACT,foot=FOOT.format(v=v))
    open(f"{v}.html","w").write(HEAD.format(v=v,feat=d["feat"],base=BASE,css=d["css"])+body+TAIL.format(js=d["js"]))
  print("ok",list(V))
