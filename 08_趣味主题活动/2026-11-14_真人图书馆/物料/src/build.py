import os, pathlib
OUT=pathlib.Path(__file__).resolve().parent.parent; SRC=OUT/'src'  # 物料/ 目录，跟着仓库走
CSS=(SRC/'common.css').read_text()
def page(body, w, h, extra=''):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>{CSS}
@page{{size:{w} {h};margin:0}} {extra}</style></head><body>{body}</body></html>'''
def stamp(size_mm, top, right, l1, l2, l3=''):
    pos=top if ':' in top else f'top:{top};right:{right}'
    return f'<div class="stamp" style="width:{size_mm}mm;height:{size_mm}mm;{pos}"><div style="line-height:1.25"><div style="font-size:{size_mm*0.12:.1f}mm;letter-spacing:.5mm">{l1}</div><div style="font-size:{size_mm*0.2:.1f}mm;font-weight:700">{l2}</div><div style="font-size:{size_mm*0.1:.1f}mm">{l3}</div></div></div>'

# ---------- 书目卡 ----------
CAT_CSS='''
.a6{width:105mm;height:148mm;position:relative;overflow:hidden;background:var(--paper);padding:9mm 9mm 8mm 13mm}
.a6::before{content:"";position:absolute;left:8.5mm;top:0;bottom:0;border-left:1px solid var(--brick);opacity:.55}
.hd{display:flex;justify-content:space-between;align-items:baseline;font-size:2.7mm;color:var(--green);letter-spacing:.3mm;border-bottom:1.4px solid var(--green);padding-bottom:1.6mm}
.hd b{font-size:3.4mm;letter-spacing:.8mm}
.lab{font-size:2.6mm;color:var(--green);margin-top:3.6mm;letter-spacing:.3mm}
.lab small{color:var(--soft);font-size:2.3mm;margin-left:1mm}
.title{font-size:7mm;font-weight:700;margin-top:1mm;display:flex;align-items:flex-end;height:10mm}
.title .gap{flex:1;border-bottom:1px solid var(--line);margin:0 1mm 1.6mm;height:1px}
.rec{font-size:3.6mm;margin-top:2.6mm;display:flex;align-items:flex-end}
.rec .gap{flex:1;border-bottom:1px solid var(--line);margin:0 1mm .9mm;height:1px}
.ln{height:7.6mm;border-bottom:1px solid var(--line);font-size:3.3mm;line-height:7.6mm;color:var(--green)}
.ft{position:absolute;left:13mm;right:9mm;bottom:6mm;font-size:2.3mm;color:var(--soft);display:flex;justify-content:space-between}
.fill{color:var(--green);font-weight:500}
.ex{position:absolute;top:5.5mm;left:50%;transform:translateX(-50%);background:var(--brick);color:#fff;font-size:2.4mm;padding:.4mm 2.5mm;border-radius:1mm;letter-spacing:.5mm}
'''
def catalog(no, ex=False):
    if ex:
        t='<span>《</span><span class="fill" style="padding:0 2mm">转行</span><span>》</span><span class="gap" style="border:none"></span>'
        r='<span>他推荐：《</span><span class="fill" style="padding:0 1mm">本人推荐</span><span>》</span><span class="gap" style="border:none"></span>'
        intro=['（示例）我在教培待过一段时间，','见过招生和课堂两端。','后来换了一条路，到现在还在找方向。','']
        ask=['为什么进来、后来怎么看这份工作，','如果重新选会怎样。']
        no_=['具体机构的名字、收入。']
    else:
        t='<span>《</span><span class="gap"></span><span>》</span>'
        r='<span>他推荐：《</span><span class="gap"></span><span>》</span>'
        intro=['']*4; ask=['']*2; no_=['']
    L=lambda xs:''.join(f'<div class="ln">{x}</div>' for x in xs)
    return f'''<div class="a6">{'<div class="ex">示例 · 仅供参考</div>' if ex else ''}
<div class="hd"><b>书目卡</b><span>周末出门 · 真人图书馆　No.{no}</span></div>
<div class="lab">书名<small>自己取，一段经历的标签</small></div><div class="title">{t}</div>
<div class="rec">{r}</div><div class="lab" style="margin-top:.6mm"><small style="margin:0">可选。也可以写带来的照片或小物件</small></div>
<div class="lab">简介<small>用「我」来写，一两句也行</small></div>{L(intro)}
<div class="lab">愿意被问的话题</div>{L(ask)}
<div class="lab">这轮先不聊</div>{L(no_)}
<div class="ft"><span>每本约 35 分钟 · 全场围坐一起借阅</span><span>2026.11.14</span></div>
{stamp(17,'bottom:12mm;right:9mm','','周末出门','借阅','宜昌')}
</div>'''
SHEET_CSS='''.sheet{width:210mm;height:297mm;display:grid;grid-template-columns:105mm 105mm;grid-template-rows:148.5mm 148.5mm;position:relative}
.sheet .a6{height:148.5mm}
.cut{position:absolute;border:0 dashed #9a917e}
.cut.v{left:105mm;top:0;bottom:0;border-left-width:.3mm}.cut.h{top:148.5mm;left:0;right:0;border-top-width:.3mm}
.pg{page-break-after:always}'''
nos=['1','2','3','候补']
singles=''.join(f'<div class="pg">{catalog(n)}</div>' for n in nos)
OUTS=[]
def add(name, html, w, h, png_split=None):
    (SRC/f'{name}.html').write_text(html); OUTS.append((name,w,h))
add('书目卡_空白_A6x4页', page(singles,'105mm','148mm',CAT_CSS+'.pg{page-break-after:always}'),105,148)
add('书目卡_示例_转行_A6', page(catalog('示例',True),'105mm','148mm',CAT_CSS),105,148)
add('书目卡_A4拼版4张', page('<div class="sheet">'+''.join(catalog(n) for n in nos)+'<div class="cut v"></div><div class="cut h"></div></div>','210mm','297mm',CAT_CSS+SHEET_CSS),210,297)

# ---------- 还书卡 ----------
RET_CSS=CAT_CSS+SHEET_CSS+'''
table{width:100%;border-collapse:collapse;margin-top:2.4mm;font-size:2.8mm}
th{color:var(--green);font-weight:500;text-align:left;border-bottom:1.2px solid var(--green);padding:.8mm 1mm;font-size:2.5mm}
td{border-bottom:1px solid var(--line);height:7.6mm;padding:0 1mm}
td.d{width:20mm;color:var(--brick);font-size:2.7mm;border-right:1px solid var(--line)}
.ck{font-size:2.8mm;margin-top:3mm;display:flex;gap:4mm}
.ck span::before{content:"";display:inline-block;width:2.6mm;height:2.6mm;border:1px solid var(--ink);margin-right:1mm;vertical-align:-.3mm}
.ln.r{height:8.6mm}
.hole{position:absolute;top:3.4mm;left:50%;width:7mm;height:2.2mm;margin-left:-3.5mm;border-radius:1.2mm;border:1px solid var(--line)}
'''
def ret():
    rows=''.join(f'<tr><td class="d">2026.11.14</td><td>第{c}本　《　　　　　　　　》</td></tr>' for c in '一二三')
    return f'''<div class="a6"><div class="hole"></div>
<div class="hd"><b>还书卡</b><span>周末出门 · 真人图书馆</span></div>
<table><tr><th>日期</th><th>借阅的书名</th></tr>{rows}</table>
<div class="lab">今天借到的一句话</div>
<div class="ln r"></div><div class="ln r"></div><div class="ln r"></div><div class="ln r"></div>
<div class="lab">想对其中一本书说</div>
<div class="ln" style="color:var(--ink)">给《　　　　》：</div><div class="ln"></div>
<div class="ck"><span>我带走这张卡</span><span>留给这本书</span></div>
{stamp(19,'bottom:11mm;right:10mm','','周末出门','已还','2026.11.14')}
</div>'''
add('还书卡_A6', page(ret(),'105mm','148mm',RET_CSS),105,148)
add('还书卡_A4拼版4张', page('<div class="sheet">'+ret()*4+'<div class="cut v"></div><div class="cut h"></div></div>','210mm','297mm',RET_CSS),210,297)

# ---------- 公约 ----------
rules=['全场围坐，同一时间一起借一本书。我们借的是这个人，推荐的书用来开个头。',
'想知道的都可以问。一次一个人说，让正在问的人把话说完。',
'书事先说好不聊的话题，还有单位、收入、家庭这些私事，书可以不答，我们也不追问。',
'每本大约 35 分钟，到点一起把书还回去。',
'书和读者都可以随时叫停这一轮，跟主持说一声就好。',
'不录音、不录像。想拍照，先问过书。',
'圈子里说的话留在圈子里。分享和写还书卡的时候，只讲自己的感受。',
'想跟书加微信，先请主持帮忙问一声。']
POS_CSS='''.a4{width:210mm;height:297mm;position:relative;padding:20mm 22mm 18mm 28mm;overflow:hidden}
.a4::before{content:"";position:absolute;left:20mm;top:0;bottom:0;border-left:1.4px solid var(--brick);opacity:.55}
.a4::after{content:"";position:absolute;inset:8mm;border:1px solid var(--line);pointer-events:none}
.kick{font-size:4mm;color:var(--green);letter-spacing:1.5mm}
h1{font-size:12mm;letter-spacing:1mm;margin-top:3mm;line-height:1.25}
h1 span{color:var(--brick)}
.rule{border-bottom:2px solid var(--green);margin:6mm 0 3mm}
ol{list-style:none;counter-reset:r}
li{counter-increment:r;display:flex;gap:5mm;padding:4.2mm 0;border-bottom:1px solid var(--line);font-size:5mm;line-height:1.6}
li::before{content:counter(r,decimal-leading-zero);color:var(--brick);font-weight:700;font-size:5mm;min-width:9mm;font-family:"Noto Sans CJK SC"}
.tip{margin-top:7mm;background:var(--paper2);border-left:3px solid var(--green);padding:4mm 5mm;font-size:4.2mm;line-height:1.7;color:var(--ink)}
.tip b{color:var(--green)}
.foot{position:absolute;bottom:14mm;left:28mm;right:22mm;display:flex;justify-content:space-between;font-size:3.3mm;color:var(--soft)}'''
pos=f'''<div class="a4"><div class="kick">READING RULES · 借阅公约</div>
<h1>周末出门 · 真人图书馆<br><span>借阅公约</span></h1><div class="rule"></div>
<ol>{''.join(f'<li>{r}</li>' for r in rules)}</ol>
<div class="tip"><b>给今天的书：</b>开场三五分钟讲讲这本书写了什么，可以从你推荐的书说起。遇到不想答的问题，说一句「这件事今天先不聊」就好。累了随时看向主持。</div>
<div class="foot"><span>2026.11.14 · 宜昌</span><span>谢谢你今天来借书，也谢谢你今天当一本书</span></div>
{stamp(26,'top:42mm;right:22mm','','周末出门','借阅','2026.11.14')}</div>'''
add('现场公约_A4海报', page(pos,'210mm','297mm',POS_CSS),210,297)

# ---------- 备用问题卡 ----------
qs=[('通用','你是怎么走到这一步的？',''),
('通用','别人第一次听到这件事，通常会怎么理解？你自己怎么看？',''),
('通用','有没有哪一次选择，现在回头看仍觉得关键？',''),
('通用','这段经历里，有哪一件小事你一直记着？',''),
('通用','如果让现在的你对当时的自己说一句，会说什么？',''),
('推荐书','你为什么想把这本书推荐给大家？','这本书没有推荐书时，换一张。'),
('推荐书','读这本书的时候，你自己正在经历什么？','这本书没有推荐书时，换一张。'),
('推荐书','这本书里，有没有一句话你到现在还记得？','这本书没有推荐书时，换一张。'),
('物件','你带来的这件东西，对你来说意味着什么？','没带物件时可以问：有没有一件东西，一想起这段经历就会想到它？')]
Q_CSS='''.qs{width:210mm;height:297mm;display:grid;grid-template-columns:repeat(3,63mm);grid-template-rows:repeat(3,88mm);justify-content:center;align-content:center;position:relative}
.q{position:relative;border:.3mm dashed #9a917e;padding:6mm 5.5mm;display:flex;flex-direction:column;overflow:hidden;background:var(--paper)}
.q::before{content:"";position:absolute;left:3.6mm;top:0;bottom:0;border-left:1px solid var(--brick);opacity:.45}
.qh{display:flex;justify-content:space-between;font-size:2.5mm;color:var(--green);border-bottom:1.2px solid var(--green);padding-bottom:1.2mm;letter-spacing:.3mm}
.tag{background:var(--green);color:#fff;padding:.2mm 1.6mm;border-radius:.8mm;font-size:2.3mm}
.tag.b{background:var(--brick)}.tag.o{background:#8a7a55}
.qt{flex:1;display:flex;align-items:center;font-size:5mm;line-height:1.65;font-weight:600;letter-spacing:.2mm}
.qn{font-size:2.4mm;color:var(--soft);line-height:1.5;border-top:1px solid var(--line);padding-top:1.4mm;min-height:8mm}
.qf{font-size:2.2mm;color:var(--soft);margin-top:1.2mm;display:flex;justify-content:space-between}'''
cls={'通用':'','推荐书':'b','物件':'o'}
cards=''.join(f'''<div class="q"><div class="qh"><span>备用问题　No.{i+1:02d}</span><span class="tag {cls[t]}">{t}</span></div>
<div class="qt">{q}</div><div class="qn">{n}</div><div class="qf"><span>周末出门 · 真人图书馆</span><span>主持抽一张</span></div></div>''' for i,(t,q,n) in enumerate(qs))
add('备用问题卡_A4拼版9张', page(f'<div class="qs">{cards}</div>','210mm','297mm',Q_CSS),210,297)

# ---------- 封面 ----------
COV_CSS='''.cv{width:1242px;height:1660px;position:relative;overflow:hidden;background:var(--paper)}
.cv{background:radial-gradient(ellipse at 50% 40%,#F7F2E6,#EAE0CB)}
.card{position:absolute;left:110px;right:110px;top:210px;bottom:250px;background:#FAF5EA;border:2px solid #D8CDB4;box-shadow:0 18px 40px rgba(80,60,30,.12);padding:90px 80px 70px 120px;transform:rotate(-1.2deg)}
.card::before{content:"";position:absolute;left:84px;top:0;bottom:0;border-left:3px solid var(--brick);opacity:.6}
.card .lines{position:absolute;left:0;right:0;bottom:70px;height:440px;background:repeating-linear-gradient(to bottom,transparent 0 86px,#D3C8AE 86px 88px)}
.top{position:absolute;top:96px;left:110px;right:110px;display:flex;justify-content:space-between;font-size:34px;color:var(--green);letter-spacing:6px}
.lab2{font-size:30px;color:var(--green);letter-spacing:6px;border-bottom:3px solid var(--green);padding-bottom:16px;display:flex;justify-content:space-between}
.big{font-size:150px;font-weight:700;color:var(--ink);line-height:1.22;margin-top:60px;letter-spacing:6px}
.big em{font-style:normal;color:var(--brick)}
.sub{font-size:52px;color:var(--green);margin-top:44px;letter-spacing:8px;font-weight:600}
.hand{position:relative;z-index:1;font-size:46px;line-height:88px;margin-top:70px}
.hand div{height:88px;border-bottom:2px solid #D3C8AE}
.hand .k{color:var(--soft);font-size:32px;margin-right:18px}
.bottom{position:absolute;bottom:110px;left:110px;right:110px;display:flex;justify-content:space-between;align-items:center;font-size:34px;color:var(--soft)}
.bottom b{color:var(--ink);font-size:42px;letter-spacing:4px}'''
def cover(big, hand_rows, no):
    rows=''.join(f'<div><span class="k">{k}</span>{v}</div>' for k,v in hand_rows)
    return f'''<div class="cv"><div class="top"><span>周末出门 · 真人图书馆</span><span>No.{no}</span></div>
<div class="card">
<div class="lab2"><span>借书卡</span><span>LIBRARY CARD</span></div>
<div class="big">{big}</div><div class="sub">周六 · 宜昌 · 真人图书馆</div>
<div class="hand">{rows}</div></div>
<div class="stamp" style="width:250px;height:250px;right:120px;top:930px;border-width:5px"><div style="line-height:1.3;position:relative"><div style="font-size:26px;letter-spacing:4px">周末出门</div><div style="font-size:54px;font-weight:900">{'招书' if no=='01' else '借阅'}</div><div style="font-size:22px;letter-spacing:2px">宜昌</div></div></div>
<div class="bottom"><span>小红书 @周末出门</span><b>{'评论区或私信报名' if no=='01' else '评论区留「想借书」'}</b></div></div>'''
add('小红书封面_招书', page(cover('来当<br>一本<em>书</em> 📖',[('书名','你自己取'),('内容','你过过的日子'),('门槛','普通的经历就可以'),('开场','带一本你推荐的书也行')],'01'),'1242px','1660px',COV_CSS),'cover','')
add('小红书封面_招读者', page(cover('周六来<br>借一个人<em>读</em>',[('借阅','几位朋友当书'),('方式','围坐着一本一本读'),('每本','约 35 分钟'),('提问','想问的都可以问')],'02'),'1242px','1660px',COV_CSS),'cover','')

# ---------- render ----------
from playwright.sync_api import sync_playwright
import subprocess
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,w,h in OUTS:
        html=(SRC/f'{name}.html').as_uri()
        if w=='cover':
            pg=b.new_page(viewport={'width':1242,'height':1660},device_scale_factor=1)
            pg.goto(html); pg.wait_for_timeout(400)
            pg.screenshot(path=str(OUT/f'{name}.png'),full_page=False); pg.close(); continue
        pg=b.new_page(); pg.goto(html); pg.wait_for_timeout(300)
        pg.pdf(path=str(OUT/f'{name}.pdf'),prefer_css_page_size=True,print_background=True); pg.close()
        subprocess.run(['pdftoppm','-r','200','-png',str(OUT/f'{name}.pdf'),str(OUT/name)],check=True)
    b.close()
