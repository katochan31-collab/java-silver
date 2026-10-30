from pathlib import Path
import re, html
src=Path('/mnt/data/JavaSilver黒本_模試1回目_改善版_v3_AI解説.md')
out=Path('/mnt/data/black_mock1.html')
md=src.read_text(encoding='utf-8').replace('\\[','[').replace('\\]',']').replace('\\<','<').replace('\\>','>').replace('\\|','|').replace('\\*','*').replace('-\\>','->').replace('\\_','_')
parts=re.split(r'(?m)^## 問題 (\d+)\s*$',md)
qs=[]
for i in range(1,len(parts),2):
    n=int(parts[i]); body=parts[i+1].strip()
    pm=re.search(r'### 問題文・コード・選択肢\s*(.*?)(?=\n### 正答)',body,re.S)
    am=re.search(r'### 正答\s*\n+([^\n]+)',body)
    em=re.search(r'### 解説\s*(.*)$',body,re.S)
    content=pm.group(1).strip() if pm else body
    ans=am.group(1).strip() if am else ''
    exp=em.group(1).strip() if em else ''
    qs.append((n,content,ans,exp))

def inline(x):
    x=html.escape(x,quote=False)
    x=re.sub(r'`([^`]+)`',r'<code>\1</code>',x)
    return x

def render(s):
    ls=s.splitlines(); o=[]; code=False; buf=[]
    for line in ls+['@@END@@']:
        if line.startswith('```'):
            if code:
                o.append('<pre><code>'+html.escape('\n'.join(buf))+'</code></pre>'); code=False; buf=[]
            else: code=True; buf=[]
            continue
        if code: buf.append(line); continue
        if line=='@@END@@': break
        t=line.strip()
        if not t: continue
        if re.match(r'^-\s+',t):
            o.append('<div class="choice">'+inline(re.sub(r'^-\s+','',t))+'</div>')
        else: o.append('<p>'+inline(t)+'</p>')
    return '\n'.join(o)

cards=[]
for n,c,a,e in qs:
    cards.append(f'''<article class="question" id="q{n}">
      <div class="qhead"><span class="badge">問{n}</span></div>
      <section class="body">{render(c)}</section>
      <details class="answer">
        <summary>正答・解説を表示</summary>
        <div class="answer-inner">
          <div class="correct"><b>正答：</b>{inline(a)}</div>
          {render(e)}
        </div>
      </details>
    </article>''')
nav=''.join(f'<a href="#q{n}">{n}</a>' for n,_,_,_ in qs)
css='''
:root { --navy:#12345b; --blue:#1769e8; --pale:#eef4fb; --line:#d7e1ec; --text:#142033; --green:#159447; }
* { box-sizing:border-box; }
html { scroll-behavior:smooth; }
body { margin:0; color:var(--text); background:#f4f7fb; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans JP",sans-serif; line-height:1.75; }
header { background:linear-gradient(120deg,#12345b,#2365dc); color:white; padding:28px max(20px,calc((100% - 980px)/2)); }
header h1 { margin:0; font-size:clamp(24px,4vw,38px); }
header p { margin:6px 0 0; opacity:.92; }
.toolbar { position:sticky; top:0; z-index:10; background:#fff; border-bottom:1px solid var(--line); padding:10px 16px; display:flex; gap:10px; justify-content:center; align-items:center; }
.toolbar button { border:0; border-radius:12px; padding:10px 16px; font-size:16px; font-weight:700; color:#fff; background:var(--blue); cursor:pointer; }
.home-button { border-radius:12px; padding:10px 16px; font-size:16px; font-weight:700; color:var(--navy); background:#e6edf6; text-decoration:none; white-space:nowrap; }
.progress { font-weight:800; min-width:90px; text-align:center; }
main { max-width:980px; margin:22px auto 80px; padding:0 16px; }
.question { scroll-margin-top:76px; background:#fff; border:1px solid var(--line); border-radius:18px; margin:0 0 24px; padding:24px; box-shadow:0 3px 14px #16345b0d; }
.qhead { margin-bottom:8px; }.badge { font-size:25px; font-weight:900; color:var(--navy); }
p { margin:.55em 0; }
pre { margin:14px 0; padding:16px; overflow-x:auto; border:1px solid var(--line); border-radius:13px; background:#f7f9fc; font:15px/1.55 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; white-space:pre; }
code { font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
p code,.answer code { background:#edf2f7; padding:.08em .35em; border-radius:5px; }
.choice { border:2px solid var(--line); border-radius:14px; padding:13px 16px; margin:10px 0; color:#075fc9; font-size:17px; overflow-wrap:anywhere; white-space:pre-wrap; }
.answer { margin-top:22px; border-top:1px solid var(--line); padding-top:16px; }
.answer summary { cursor:pointer; color:var(--blue); font-weight:800; }
.answer-inner { margin-top:14px; padding:16px; background:#f8fbff; border-radius:12px; }
.correct { color:var(--green); font-size:18px; margin-bottom:10px; }
#index { max-width:980px; margin:22px auto; padding:0 16px; }
#index details { background:white; padding:12px 16px; border-radius:14px; border:1px solid var(--line); }
#index nav { display:grid; grid-template-columns:repeat(auto-fill,minmax(45px,1fr)); gap:8px; margin-top:12px; }
#index a { text-align:center; padding:8px 4px; color:var(--blue); text-decoration:none; background:var(--pale); border-radius:8px; font-weight:700; }
@media(max-width:600px) { header{padding:22px 18px}.toolbar{flex-wrap:wrap;justify-content:space-between}.home-button{width:100%;text-align:center}.question{padding:18px 16px;border-radius:14px}pre{font-size:13px}.choice{font-size:16px} }
@media print { .toolbar,#index{display:none}.question{break-inside:avoid;box-shadow:none}details.answer:not([open])>*:not(summary){display:block}details.answer summary{display:none} }
'''
js='''const qs=[...document.querySelectorAll('.question')];
let idx=0;
function go(d){idx=Math.max(0,Math.min(qs.length-1,idx+d));qs[idx].scrollIntoView({behavior:'smooth',block:'start'});update();}
function update(){document.getElementById('pos').textContent=(idx+1)+' / '+qs.length;}
const obs=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){idx=qs.indexOf(e.target);update();}})},{rootMargin:'-35% 0px -55%'});
qs.forEach(q=>obs.observe(q));update();'''
doc=f'''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>Java Silver 黒本 模擬試験1</title>
  <style>\n{css}\n  </style>
</head>
<body>
  <header>
    <h1>Java Silver 黒本 模擬試験①</h1>
    <p>全{len(qs)}問。正答・解説は各問題の下で開閉できます。</p>
  </header>
  <div class="toolbar">
    <a class="home-button" href="index.html">はじめの画面に戻る</a>
    <button type="button" onclick="go(-1)">前へ</button>
    <span class="progress" id="pos">1 / {len(qs)}</span>
    <button type="button" onclick="go(1)">次へ</button>
  </div>
  <section id="index">
    <details><summary>問題一覧</summary><nav>{nav}</nav></details>
  </section>
  <main>
    {''.join(cards)}
  </main>
  <script>\n{js}\n  </script>
</body>
</html>'''
out.write_text(doc,encoding='utf-8')
print('[OK]',out,'questions=',len(qs),'bytes=',out.stat().st_size)
