// 全案共通：data.json読込・カテゴリ絞り込み（すべて／ロゴ／ページ／アプリ）・プロフィール差し込み
// 各案は window.T = {card(it,i)} で見た目だけ差し替える
const CATS=[["","すべて"],["ロゴ"],["ページ"],["アプリ"]];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const scopeTags=it=>it.scope.map(s=>`<span class="scope">${esc(s)}</span>`).join("");
const aiTags=it=>it.ai.map(a=>`<span class="ai">${esc(a)}</span>`).join("");
const tags=it=>`<div class="tags">${scopeTags(it)}${aiTags(it)}</div>`;
const thumb=it=>it.thumb?`<img class="th" src="${esc(it.thumb)}" alt="${esc(it.title)}の画面" loading="lazy" width="800" height="500">`:`<div class="th ph"><span>${esc(it.short||it.title)}</span><small>仮サムネ</small></div>`;
const link=(it,inner,cls="")=>it.url?`<a class="${cls}" href="${esc(it.url)}" target="_blank" rel="noopener">${inner}</a>`:`<span class="${cls}">${inner}</span>`;
const $=id=>document.getElementById(id);
const APP=window.APP={items:[],cat:""};
APP.render=()=>{
  const list=APP.items.filter(it=>!APP.cat||it.scope.includes(APP.cat));
  $("list").innerHTML=list.map(T.card).join("");
  $("empty").style.display=list.length?"none":"block";
  if($("count"))$("count").textContent=list.length;
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
