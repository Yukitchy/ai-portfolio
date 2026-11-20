// 全案共通：data.json読込・カテゴリ絞り込み（すべて／ロゴ／ページ／アプリ）・プロフィール差し込み
// 各案は window.T = {card(it,i)} で見た目だけ差し替える
const CATS=[["","すべて"],["ロゴ"],["ページ"],["アプリ"]];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const scopeTags=it=>it.scope.map(s=>`<span class="scope">${esc(s)}</span>`).join("");
const aiTags=it=>it.ai.map(a=>`<span class="ai">${esc(a)}</span>`).join("");
// 使用AIが不明（ai空）の作品はタグ欄ごと出さない（空の枠・でっちあげタグを作らない）
const tags=it=>it.ai&&it.ai.length?`<div class="tags">${scopeTags(it)}${aiTags(it)}</div>`:"";
// サムネは絞り込みに合わせる：data.json の thumbs[カテゴリ]（ロゴ＝ロゴ画像）→ なければ代表 thumb → なければ仮サムネ
const src=it=>(APP.cat&&it.thumbs&&it.thumbs[APP.cat])||it.thumb;
const thumb=it=>src(it)?`<img class="th" src="${esc(src(it))}" alt="${esc(it.title)}の${APP.cat==="ロゴ"?"ロゴ":"画面"}" loading="lazy" width="800" height="500">`:`<div class="th ph"><span>${esc(it.short||it.title)}</span><small>仮サムネ</small></div>`;
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
    const one=its.map(it=>`<span class="fi">${thumb(it).replace(' loading="lazy"',"")}</span>`).join("");
    f.innerHTML=`<div class="tr">${one}</div>`;
    const k=Math.max(1,Math.ceil(Math.max(f.clientWidth,760)/(f.firstChild.scrollWidth||1)));
    f.firstChild.innerHTML=one.repeat(k*2);
    // 枚数が増えても流れる速さは6枚基準のまま（1周の秒数を枚数に比例させる）
    const n=its.length*k,t=f.firstChild;if(n>6)t.style.animationDuration=parseFloat(getComputedStyle(t).animationDuration)*n/6+"s";
  }
};
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
  if($("pContact")){$("pContact").href=p.contact;$("pContact").textContent=p.contactLabel}
  APP.items=d.items;APP.render();
});
