# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4", "playwright"]
# ///
"""Rebuild stack-diagram HTML and both PNG themes from diagrams/*.json.
Usage: uv run scripts/redraw_diagrams.py [slug ...] [--render]
The templates and pictograms follow stack-diagram (MIT), Lucide (ISC).
"""
from pathlib import Path
from html import escape as esc
import json,re,sys,heapq,math
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'diagrams'
COLORS=['blue','amber','violet','green','slate']

def simplify(points):
 out=[]
 for p in points:
  if len(out)>=2 and (out[-2][0]==out[-1][0]==p[0] or out[-2][1]==out[-1][1]==p[1]):out[-1]=p
  else:out.append(p)
 return out

def topology(s,icons):
 nodes=s['nodes']; groups=[];step=s.get('row_step',220);colstep=s.get('column_step',340);W=160+len(s['boundaries'])*colstep;maxn=max(sum(n['group']==str(i) for n in nodes) for i in range(len(s['boundaries'])));H=180+maxn*step
 for i,label in enumerate(s['boundaries']):
  ns=[n for n in nodes if n['group']==str(i)];x=40+i*colstep
  for j,n in enumerate(ns):n['cx']=x+110;n['cy']=150+j*step
  groups.append((x,90,220,maxn*step+50,label,COLORS[i%len(COLORS)]))
 # Hand-composed system maps: main request spine above, support planes below.
 if 'layout' in s:
  layout=s['layout'];groups=layout['groups'];W=layout['width'];H=layout['height']
  for n in nodes:n['cx'],n['cy']=layout['positions'][n['id']]
 obstacles=[(n['cx']-78,n['cy']-8,n['cx']+78,n['cy']+116) for n in nodes]
 # Group headings reserve a separate band above components.
 obstacles += [(x+8,y+6,x+min(w-8,len(l)*12+24),y+34) for x,y,w,h,l,c in groups]
 label_obstacles=[(n["cx"]-34,n["cy"]-6,n["cx"]+34,n["cy"]+60) for n in nodes]+[(n["cx"]-78,n["cy"]+62,n["cx"]+78,n["cy"]+116) for n in nodes]+obstacles[len(nodes):]
 grid=10;nx=math.ceil(W/grid);ny=math.ceil(H/grid)
 blocked=set()
 for x1,y1,x2,y2 in obstacles:
  for x in range(max(1,math.ceil(x1/grid)),min(nx,math.floor(x2/grid))+1):
   for y in range(max(1,math.ceil(y1/grid)),min(ny,math.floor(y2/grid))+1):blocked.add((x,y))
 port_use={};occupancy={};labels=[];segments=[];edgeparts=[];history=set();byid={n['id']:n for n in nodes}
 def ports(n):
  x,y=n['cx'],n['cy'];result=[]
  for side in ['R','L','T','B']:
   k=port_use.get((n['id'],side),0);offset=[0,10,-10,20,-20][k%5]
   if side=='R':result.append(((x+30,y+30+offset),(x+90,y+30+offset),side))
   elif side=='L':result.append(((x-30,y+30+offset),(x-90,y+30+offset),side))
   elif side=='T':result.append(((x+offset,y-5),(x+offset,y-20),side))
   else:result.append(((x+offset,y+110),(x+offset,y+130),side))
  return result
 def route(a,b,forced=None,relaxed=False):
  returning=(b["id"],a["id"]) in history
  history.add((a["id"],b["id"]))
  opts=[]
  for aa,ap,aside in ports(a):
   for ba,bp,bside in ports(b):
    if not relaxed and returning and not forced and ([aside,bside] != (["T","T"] if a["cy"]==b["cy"] else ["R","R"])):continue
    if forced and [aside,bside]!=forced:continue
    # Penalize facing away from the target and unnecessary vertical turns.
    dist=abs(ap[0]-bp[0])+abs(ap[1]-bp[1]);opts.append((dist,aa,ap,ba,bp,aside,bside))
  # Try whole straight corridors first. Avoid grid-snapped staircase segments
  # and short port stubs when a direct architectural connector is available.
  def clear(points):
   for u,v in zip(points,points[1:]):
    for x1,y1,x2,y2 in obstacles:
     if u[0]==v[0] and x1-3<u[0]<x2+3 and max(min(u[1],v[1]),y1-3)<min(max(u[1],v[1]),y2+3):return False
     if u[1]==v[1] and y1-3<u[1]<y2+3 and max(min(u[0],v[0]),x1-3)<min(max(u[0],v[0]),x2+3):return False
    for xx,yy in blocked:
     if u[0]==v[0] and abs(xx*grid-u[0])<3 and min(u[1],v[1])<yy*grid<max(u[1],v[1]):return False
     if u[1]==v[1] and abs(yy*grid-u[1])<3 and min(u[0],v[0])<xx*grid<max(u[0],v[0]):return False
   return True
  candidates=[]
  for _,aa,ap,ba,bp,aside,bside in sorted(opts):
   choices=[]
   if ap[0]==bp[0] or ap[1]==bp[1]:choices.append([ap,bp])
   choices += [[ap,(ap[0],bp[1]),bp],[ap,(bp[0],ap[1]),bp]]
   for mid in [(ap[0]+bp[0])/2,ap[0],bp[0]]:choices.append([ap,(mid,ap[1]),(mid,bp[1]),bp])
   for mid in [(ap[1]+bp[1])/2,ap[1],bp[1]]:choices.append([ap,(ap[0],mid),(bp[0],mid),bp])
   for pts in choices:
    pts=simplify(list(dict.fromkeys(pts)))
    if len(pts)<2 or not clear(pts):continue
    complete=simplify([aa]+pts+[ba])
    # Reject backtracking caused by a side pointing away from the route.
    bad=False
    for u,v,z in zip(complete,complete[1:],complete[2:]):
     if (v[0]-u[0])*(z[0]-v[0])+(v[1]-u[1])*(z[1]-v[1])<0:bad=True
    if bad:continue
    length=sum(abs(u[0]-v[0])+abs(u[1]-v[1]) for u,v in zip(complete,complete[1:]))
    overlap=sum(occupancy.get((round(x/grid),round(y/grid)),0) for x,y in pts)
    candidates.append((length+100*max(0,len(complete)-2)+overlap*60,complete,aside,bside))
  if candidates:
   _,pts,aside,bside=min(candidates,key=lambda c:c[0])
   port_use[(a['id'],aside)]=port_use.get((a['id'],aside),0)+1
   port_use[(b['id'],bside)]=port_use.get((b['id'],bside),0)+1
   for u,v in zip(pts,pts[1:]):
    length=abs(u[0]-v[0])+abs(u[1]-v[1])
    for k in range(0,int(length)+1,10):
     t=k/max(1,length);key=(round((u[0]+(v[0]-u[0])*t)/grid),round((u[1]+(v[1]-u[1])*t)/grid));occupancy[key]=occupancy.get(key,0)+1
   return pts
  for _,aa,ap,ba,bp,aside,bside in sorted(opts)[:8]:
   start=tuple(round(v/grid) for v in ap);end=tuple(round(v/grid) for v in bp)
   if start in blocked or end in blocked:continue
   q=[(0,0,start[0],start[1],-1)];cost={(start[0],start[1],-1):0};prev={};found=None
   while q:
    _,g,x,y,d=heapq.heappop(q)
    if g!=cost.get((x,y,d)):continue
    if (x,y)==end:found=(x,y,d);break
    for nd,(dx,dy) in enumerate([(1,0),(-1,0),(0,1),(0,-1)]):
     xx,yy=x+dx,y+dy
     if not(1<=xx<nx and 8<=yy<ny-2) or (xx,yy) in blocked:continue
     ng=g+10+(20 if d!=-1 and nd!=d else 0)+occupancy.get((xx,yy),0)*22
     key=(xx,yy,nd)
     if ng<cost.get(key,1e30):
      cost[key]=ng;prev[key]=(x,y,d);h=(abs(xx-end[0])+abs(yy-end[1]))*10;heapq.heappush(q,(ng+h,ng,xx,yy,nd))
   if found:
    path=[];k=found
    while k in prev:path.append((k[0]*grid,k[1]*grid));k=prev[k]
    path.append(ap);path.reverse()
    for x,y in path:occupancy[(round(x/grid),round(y/grid))]=occupancy.get((round(x/grid),round(y/grid)),0)+1
    port_use[(a["id"],aside)]=port_use.get((a["id"],aside),0)+1
    port_use[(b["id"],bside)]=port_use.get((b["id"],bside),0)+1
    return simplify([aa]+path+[bp,ba])
  if not relaxed:return route(a,b,None,True)
  raise RuntimeError(f'No orthogonal route: {s["slug"]}: {a["label"]} -> {b["label"]}')
 def recthit(a,b):return a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]
 # Long routes first; local links can then use separate short lanes.
 for e in s['edges']:
  a,b=byid[e['from']],byid[e['to']];pts=route(a,b,e.get('ports'));d='M'+' L'.join(f'{x:g} {y:g}' for x,y in pts);kind='e' if e['kind']=='primary' else 'n';label=e['label'];edgeparts.append(f'<path class="edge-halo" d="{d}"/><path class="{kind}" data-edge="{e["id"]}" d="{d}" marker-end="url(#ar)"/>')
  if label:
   lines=[]
   # Never split a Korean word or a protocol identifier to fit a label.
   for paragraph in label.split('\n'):
    line=''
    for word in paragraph.split():
     candidate=(line+' '+word).strip()
     width=sum(10.5 if ord(c)>255 else 5.5 for c in candidate)
     if width>160 and line:lines.append(line);line=word
     else:line=candidate
    if line:lines.append(line)
   tw=max(sum(10.5 if ord(c)>255 else 5.5 for c in line) for line in lines)+12;th=18*len(lines)+4;poss=[]
   for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
    length=abs(x2-x1)+abs(y2-y1)
    if x1!=x2 and length>=tw+8:
     for frac in [.5,.4,.6,.3,.7,.2,.8,.15,.85,.25,.75,.35,.65]:
      for off in [-10,th+3]:poss.append((length-abs(frac-.5)*30,x1+(x2-x1)*frac,(y1+y2)/2+off))
    elif x1==x2 and length>=th+16:
     for frac in [.5,.4,.6,.3,.7,.2,.8,.15,.85,.25,.75,.35,.65]:
      for off in [tw/2+9,-tw/2-9]:poss.append((length-abs(frac-.5)*30,(x1+x2)/2+off,y1+(y2-y1)*frac+th/2-5))
   placed=None
   for _,x,y in sorted(poss,reverse=True):
    rect=(x-tw/2,y-th+4,x+tw/2,y+7)
    if rect[0]<8 or rect[2]>W-8 or any(recthit(rect,r) for r in label_obstacles+labels+segments):continue
    placed=(x,y,rect);break
   if placed is None:raise RuntimeError(f'No label space: {s["slug"]}: {label} route={pts} width={tw} height={th}')
   x,y,rect=placed;labels.append(rect)
   for xx in range(math.ceil((rect[0]-4)/grid),math.floor((rect[2]+4)/grid)+1):
    for yy in range(math.ceil((rect[1]-4)/grid),math.floor((rect[3]+4)/grid)+1):blocked.add((xx,yy))
   edgeparts.append(f'<text data-edge="{e["id"]}" class="el {"a" if kind=="e" else ""}" x="{x:g}" y="{y-18*(len(lines)-1):g}" text-anchor="middle">{''.join(f'<tspan x="{x:g}" dy="{0 if i==0 else 18}">{esc(line)}</tspan>' for i,line in enumerate(lines))}</text>')
  segments.extend((min(a[0],b[0])-2,min(a[1],b[1])-2,max(a[0],b[0])+2,max(a[1],b[1])+2) for a,b in zip(pts,pts[1:]))
 grouphtml=''.join(f'<div class="group {c}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><div class="g-label">{esc(l)}</div></div>' for x,y,w,h,l,c in groups)
 svg=f'<svg class="edges" viewBox="0 0 {W} {H}" aria-hidden="true"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="context-stroke"/></marker></defs>'+''.join(edgeparts)+'</svg>'
 nodehtml=''.join(f'<div class="node" data-id="{n["id"]}" style="left:{n["cx"]-74}px;top:{n["cy"]}px"><div class="tile"><img src="{icons[n["icon"]]}" alt=""></div><div class="name"><span>{esc(n["label"])}</span></div><div class="role"><span>{esc(n["role"])}</span></div></div>' for n in nodes)
 return grouphtml+svg+nodehtml,W,H

CSS='''
body{padding:24px;background:var(--color-paper);font-family:var(--font-body)}
.page{max-width:100%;margin:auto;width:fit-content}.head{display:none}.scroller{max-width:100%;overflow:auto;border:1px solid var(--color-rule-2);border-radius:8px}.canvas{position:relative;background-color:var(--color-paper);background-image:linear-gradient(var(--color-rule) 1px,transparent 1px),linear-gradient(90deg,var(--color-rule) 1px,transparent 1px);background-size:20px 20px;overflow:visible}
.diagram-title{position:absolute;left:30px;top:22px;font-size:20px;font-weight:750;letter-spacing:-.02em;color:var(--color-ink)}.diagram-kicker{position:absolute;left:30px;top:55px;font:11px var(--font-mono);color:var(--color-muted)}
.group{position:absolute;border:1.3px solid var(--group-stroke);background:var(--group-fill);border-radius:6px;z-index:0}.group.blue,.group.gb{--group-stroke:#78b3d0;--group-fill:#e6f3fc66;--group-ink:#286d94}.group.amber{--group-stroke:#c6a16b;--group-fill:#fcf1dd66;--group-ink:#8f642d}.group.violet{--group-stroke:#aaa0d7;--group-fill:#f0ecfc66;--group-ink:#6e55a0}.group.green{--group-stroke:#80bba6;--group-fill:#e6f6ec66;--group-ink:#337a60}.group.slate{--group-stroke:#a0afbf;--group-fill:#edf1f666;--group-ink:#566577}
[data-theme=dark] .group{background:color-mix(in srgb,var(--group-stroke) 9%,transparent);border-color:color-mix(in srgb,var(--group-stroke) 70%,transparent)}[data-theme=dark] .g-label{color:var(--color-ink-2)}
.g-label{position:absolute;top:14px;left:14px;font-size:12px;font-weight:700;line-height:1.4;color:var(--group-ink);max-width:calc(100% - 28px)}
.edges,svg.edges{position:absolute;inset:0;width:100%;height:100%;z-index:1;overflow:visible}.edges .e{fill:none;stroke:var(--color-accent);stroke-width:1.7}.edges .n{fill:none;stroke:var(--color-neutral);stroke-width:1.45}.edge-halo{fill:none;stroke:var(--color-paper);stroke-width:5}.edges .el{font-family:var(--font-body);font-size:12px;fill:var(--color-neutral);paint-order:stroke;stroke:var(--color-paper);stroke-width:5;stroke-linejoin:round;letter-spacing:0}.edges .el.a{fill:var(--color-accent)}
.node{position:absolute;width:148px;text-align:center;z-index:2}.node .tile{width:54px;height:54px;margin:0 auto;background:#fff;border:1px solid #c9d2db;border-radius:7px;box-shadow:0 1px 2px #23374b12;display:flex;align-items:center;justify-content:center}.node .tile img{max-width:34px;max-height:34px;width:34px;height:34px}.node .name,.node .role,.g-label{word-break:keep-all;overflow-wrap:normal}.node .name{font:700 14px/1.45 var(--font-body);color:var(--color-ink);margin-top:9px}.node .role{font:11px/1.5 var(--font-body);color:var(--color-muted);margin-top:3px;letter-spacing:0}.node .name span,.node .role span{background:var(--color-veil);box-shadow:3px 0 var(--color-veil),-3px 0 var(--color-veil)}
.structure .node{width:132px}.structure .node .tile{width:60px;height:60px}.structure .node .name{font-size:14px;margin-top:7px}.structure .node .role{font-size:11px}.structure .edges .el{font-size:14px}.structure .group:nth-of-type(3n+2){--group-stroke:#c6a16b;--group-fill:#fcf1dd66;--group-ink:#8f642d}.structure .group:nth-of-type(3n+3){--group-stroke:#aaa0d7;--group-fill:#f0ecfc66;--group-ink:#6e55a0}
.legend{font:12px/1.6 var(--font-body);margin:14px 0;color:var(--color-muted);letter-spacing:0}.foot{font:11px/1.7 var(--font-body);margin-top:12px;color:var(--color-muted);letter-spacing:0}.foot a{color:inherit}.caption{font:13px/1.8 var(--font-body);max-width:1050px;margin:16px 0;color:var(--color-ink-2)}
'''

def build(s,icons,head):
 if s['mode']=='topology':inner,w,h=topology(s,icons);cls='topology';top=0
 else:
  soup=BeautifulSoup(s['canvas'],'html.parser');canvas=soup.select_one('.canvas');inner=''.join(str(x) for x in canvas.contents);w=s['width'];h=s['height']+85;inner=f'<div style="position:absolute;left:0;top:85px;width:{w}px;height:{s["height"]}px">{inner}</div>';cls='structure'
 title=esc(s['title']);chapter=s['chapter'].split('-')[0];kicker='FUNDAMENTALS' if s['chapter']=='fundamentals' else f'CHAPTER {chapter}'
 body=f'<body><main class="page"><div class="scroller"><div class="canvas {cls}" style="width:{w:g}px;height:{h:g}px"><div class="diagram-title">{title}</div><div class="diagram-kicker">{kicker} · STACK DIAGRAM</div>{inner}</div></div><div class="legend">파랑 실선: 주요 요청·데이터 흐름 · 회색 실선: 보조 경로 · 점선: 도식에 표시한 비동기·제어 관계 · 그룹: 논리적 역할 경계</div><p class="caption">{esc(s["caption"])}</p><footer class="foot">책의 설계 범위를 바탕으로 재구성 · icons: {s.get("icon_sources","Lucide")} · made with <a href="https://stack-diagram.com/">stack-diagram</a></footer></main></body></html>'
 return re.sub(r'<title>.*?</title>',f'<title>{title}</title>',head)+f'<style>{CSS}</style></head>'+body

REPAIR_LABELS=(ROOT/'scripts/diagram_label_layout.js').read_text()

def main():
 args=sys.argv[1:];render='--render' in args;slugs=[a for a in args if not a.startswith('--')];icons=json.loads((DATA/'icons.json').read_text());head=(DATA/'template-head.html').read_text();paths=[]
 for spec in sorted(DATA.glob('*.json')):
  if spec.name=='icons.json' or '.layout.' in spec.name:continue
  s=json.loads(spec.read_text())
  if slugs and s['slug'] not in slugs:continue
  folder=ROOT/'fundamentals' if s['chapter']=='fundamentals' else ROOT/'chapters'/s['chapter'];p=folder/'assets'/f'{s["slug"]}.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(build(s,icons,head));paths.append(p);print('built',s['slug'],flush=True)
 if render:
  from playwright.sync_api import sync_playwright
  with sync_playwright() as pw:
   browser=pw.chromium.launch(args=['--font-render-hinting=none']);page=browser.new_page(device_scale_factor=1.5)
   for p in paths:
    page.goto(p.as_uri());page.evaluate('document.fonts.ready');w=page.locator('.canvas').evaluate('(e)=>e.offsetWidth');h=page.locator('.canvas').evaluate('(e)=>e.offsetHeight');page.set_viewport_size({'width':int(w)+80,'height':int(h)+80});page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
    receipt=page.evaluate(REPAIR_LABELS);p.write_text(page.content());print('labels',p.stem,receipt,flush=True)
    for theme,suffix in [('light',''),('dark','-dark')]:
     page.evaluate('(v)=>document.documentElement.dataset.theme=v',theme);page.locator('.canvas').screenshot(path=str(p.with_name(p.stem+suffix+'.png')))
    print('rendered',p.stem,flush=True)
   browser.close()
if __name__=='__main__':main()
