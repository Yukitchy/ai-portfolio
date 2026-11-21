// 全案共通：data.json読込・カテゴリ絞り込み（すべて／ロゴ／ページ／アプリ）・プロフィール差し込み
// 各案は window.T = {card(it,i)} で見た目だけ差し替える
const CATS=[["","すべて"],["ロゴ"],["ページ"],["アプリ"]];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const scopeTags=it=>it.scope.map(s=>`<span class="scope">${esc(s)}</span>`).join("");
const aiTags=it=>it.ai.map(a=>`<span class="ai">${esc(a)}</span>`).join("");
// カテゴリタグは全作品に出す。使用AIが不明（ai空）の作品はAIタグだけ出さない（空チップ・でっちあげタグを作らない）
const tags=it=>`<div class="tags">${scopeTags(it)}${it.ai&&it.ai.length?aiTags(it):""}</div>`;
// サムネは絞り込みに合わせる：data.json の thumbs[カテゴリ]（ロゴ＝ロゴ画像）→ なければ代表 thumb → なければ仮サムネ
const src=it=>(APP.cat&&it.thumbs&&it.thumbs[APP.cat])||it.thumb;
// リスト用：すべて表示で thumb が空でもカテゴリ別サムネ（ロゴ絵）があればそれを出す。流れは src のまま（すべて表示の流れにロゴを混ぜない）
const lsrc=it=>src(it)||Object.values(it.thumbs||{}).find(Boolean);
const thumb=(it,s=lsrc(it))=>s?`<img class="th" src="${esc(s)}" alt="${esc(it.title)}の${APP.cat==="ロゴ"?"ロゴ":"画面"}" loading="lazy" width="800" height="500">`:`<div class="th ph"><span>${esc(it.short||it.title)}</span><small>仮サムネ</small></div>`;
const link=(it,inner,cls="")=>it.url?`<a class="${cls}" href="${esc(it.url)}" target="_blank" rel="noopener">${inner}</a>`:`<span class="${cls}">${inner}</span>`;
const $=id=>document.getElementById(id);
const APP=window.APP={items:[],cat:""};
APP.render=()=>{
  const list=APP.items.filter(it=>!APP.cat||it.scope.includes(APP.cat));
  $("list").innerHTML=list.map(T.card).join("");
  $("empty").style.display=list.length?"none":"block";
  if($("count"))$("count").textContent=list.length;
  flows(list.filter(src));
};
// ヒーローの流れ：絞り込み中の作品のうち実画像のあるものだけ（仮サムネは流さない）。幅を埋める回数だけ並べ、それを2周ぶん入れて半分ずらしでループ。.rev は逆順・逆方向
const flows=real=>{
  for(const f of document.querySelectorAll(".flow")){
    const its=f.classList.contains("rev")?[...real].reverse():real;
    const one=its.map(it=>`<span class="fi">${thumb(it,src(it)).replace(' loading="lazy"',"")}</span>`).join("");
    f.innerHTML=`<div class="tr">${one}</div>`;
    const k=Math.max(1,Math.ceil(Math.max(f.clientWidth,760)/(f.firstChild.scrollWidth||1)));
    f.firstChild.innerHTML=one.repeat(k*2);
    // 枚数が増えても流れる速さは6枚基準のまま（1周の秒数を枚数に比例させる）
    const n=its.length*k,t=f.firstChild;if(n>6)t.style.animationDuration=parseFloat(getComputedStyle(t).animationDuration)*n/6+"s";
  }
};
// 流れを指・マウスで横に流せる：CSSアニメはそのまま、触っている間だけ一時停止して currentTime を指の移動量ぶん動かし、離したらその位置から再生。
// 縦スワイプは touch-action:pan-y でブラウザのスクロールに任せる（横と判定した時だけ動かす）。動かした後のクリックは握りつぶす
for(const f of document.querySelectorAll(".top .flow")){
  let s=null,moved=false;
  f.addEventListener("pointerdown",e=>{
    const t=f.firstChild,a=t&&t.getAnimations()[0];if(!a||e.button)return;
    s={x:e.clientX,y:e.clientY,id:e.pointerId,a,c0:a.currentTime,k:a.effect.getTiming().duration/(t.scrollWidth/2),on:false};moved=false;
  });
  f.addEventListener("pointermove",e=>{
    if(!s||e.pointerId!==s.id)return;const dx=e.clientX-s.x,dy=e.clientY-s.y;
    if(!s.on){if(Math.abs(dx)<6||Math.abs(dx)<Math.abs(dy))return;s.on=moved=true;s.a.pause();try{f.setPointerCapture(s.id)}catch{}f.classList.add("drag")}
    const D=s.a.effect.getTiming().duration;s.a.currentTime=((s.c0-dx*s.k)%D+D)%D;
  });
  const end=e=>{if(!s||e.pointerId!==s.id)return;if(s.on){s.a.play();f.classList.remove("drag")}s=null};
  f.addEventListener("pointerup",end);f.addEventListener("pointercancel",end);
  f.addEventListener("click",e=>{if(moved){e.preventDefault();e.stopPropagation();moved=false}},true);
  f.addEventListener("dragstart",e=>e.preventDefault());
}
$("catRow").innerHTML=CATS.map(([v,l])=>`<button class="chip" data-cat="${v}" aria-pressed="${v===""}">${l||v}</button>`).join("");
$("catRow").addEventListener("click",e=>{
  const b=e.target.closest(".chip");if(!b)return;
  APP.cat=b.dataset.cat;
  for(const c of $("catRow").children)c.setAttribute("aria-pressed",c.dataset.cat===APP.cat);
  APP.render();
});
fetch("data.json").then(r=>r.json()).then(d=>{
  const p=d.profile;
  for(const[k,v]of[["pName",p.name],["pRole",p.role],["pBio",p.bio],["pNote",p.contactNote]])if($(k))$(k).textContent=v;
  if($("pContact"))$("pContact").textContent=p.contactLabel;
  APP.items=d.items;APP.render();
});
// 仕事の相談：ヘッダー .cta とプロフィール #pContact の両方でモーダルを開く。×・背景タップ・ESC（dialog標準）で閉じる。本文タップでは閉じない
const MAIL="japantour@muse.ai",FORM="https://docs.google.com/forms/d/e/1FAIpQLScUAsRq5ExFKlfU7qa3hRLjSBkEPVIRfvZ89BDcUkBsQ1rokQ/viewform";
const mailto=`mailto:${MAIL}?subject=${encodeURIComponent("【AIポートフォリオ】仕事の相談")}&body=${encodeURIComponent(["お名前：","相談の種類：ロゴ・ページ・アプリ画面・その他","相談内容：",""].join("\r\n"))}`;
document.body.insertAdjacentHTML("beforeend",`<dialog id="cdlg" class="cdlg" aria-labelledby="cdlgT"><div class="mb"><button type="button" class="x" aria-label="閉じる">×</button><p class="mt" id="cdlgT">仕事の相談</p><p class="ms">ロゴ1点から、ページ・アプリ画面まで。<br>相談しやすい方法を選んでください。</p><a class="mo mail" href="${esc(mailto)}">メールで相談する<small>${MAIL}</small></a><a class="mo form" href="${FORM}" target="_blank" rel="noopener">フォームで相談する<small>Googleフォームが新しいタブで開きます</small></a></div></dialog>`);
const dlg=$("cdlg");
for(const b of document.querySelectorAll("header .cta,#pContact"))b.addEventListener("click",()=>dlg.showModal());
dlg.addEventListener("click",e=>{if(e.target===dlg||e.target.closest(".x"))dlg.close()});
