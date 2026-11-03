()=>{
const svg=document.querySelector('svg.edges'),isStructure=document.querySelector('.canvas').classList.contains('structure');
const arrows=[...svg.querySelectorAll(':scope > path[marker-end]')],pairs=[];
for(let i=0;i<arrows.length;i++){
 let p=arrows[i],t=isStructure?p.nextElementSibling:svg.querySelector(`text[data-edge="${p.dataset.edge}"]`);
 if(t?.tagName.toLowerCase()==='text'&&t.textContent.trim()&&!t.dataset.note){p.dataset.edge=p.dataset.edge||'s'+i;t.dataset.edge=p.dataset.edge;pairs.push([p,t]);}
}
const labels=new Set(pairs.map(p=>p[1])),vb=svg.viewBox.baseVal,rects=[];
const svgBounds=e=>{let b=e.getBoundingClientRect(),v=svg.getBoundingClientRect();return{x:vb.x+(b.x-v.x)*vb.width/v.width,y:vb.y+(b.y-v.y)*vb.height/v.height,width:b.width*vb.width/v.width,height:b.height*vb.height/v.height};};
for(let e of document.querySelectorAll('.node .tile,.node .name,.node .role,.g-label'))rects.push(svgBounds(e));
for(let e of svg.querySelectorAll(':scope > rect,:scope > text,:scope > circle'))if(!labels.has(e))rects.push(e.getBBox());
const intersect=(a,b,g=3)=>a.x<b.x+b.width+g&&b.x<a.x+a.width+g&&a.y<b.y+b.height+g&&b.y<a.y+a.height+g;
const distance=(p,b)=>{let best=1e9,L=p.getTotalLength();for(let t=0;t<=L;t+=Math.max(1,L/500)){let q=p.getPointAtLength(t),d=Math.hypot(Math.max(b.x-q.x,0,q.x-b.x-b.width),Math.max(b.y-q.y,0,q.y-b.y-b.height));best=Math.min(best,d)}return best};
let moved=0,issues=[];const placed=[];
for(let [p,t] of pairs){
 let b=t.getBBox(),original=[t,...t.querySelectorAll('tspan')].map(e=>[e,e.getAttribute('x'),e.getAttribute('y')]);
 const apply=(dx,dy)=>{for(let [e,x,y] of original){if(x!==null)e.setAttribute('x',Number(x)+dx);if(y!==null)e.setAttribute('y',Number(y)+dy)}};
 const valid=c=>c.x>=vb.x+8&&c.y>=vb.y+8&&c.x+c.width<=vb.x+vb.width-8&&c.y+c.height<=vb.y+vb.height-8&&!rects.some(r=>intersect(c,r,2))&&!placed.some(r=>intersect(c,r,3))&&!arrows.some(other=>other!==p&&distance(other,c)<2);
 if(distance(p,b)<=18&&valid(b)){placed.push(b);continue;}
 const L=p.getTotalLength();let candidates=[];
 for(let f of [.5,.4,.6,.3,.7,.2,.8,.1,.9,.15,.85]){
  let q=p.getPointAtLength(L*f),q1=p.getPointAtLength(Math.max(0,L*f-2)),q2=p.getPointAtLength(Math.min(L,L*f+2));
  if(Math.abs(q2.x-q1.x)>Math.abs(q2.y-q1.y))candidates.push([q.x-b.width/2,q.y-b.height-9],[q.x-b.width/2,q.y+9]);
  else candidates.push([q.x+10,q.y-b.height/2],[q.x-b.width-10,q.y-b.height/2]);
 }
 let found=false;
 for(let [x,y] of candidates){
  apply(x-b.x,y-b.y);let c=t.getBBox();
  if(!valid(c))continue;
  placed.push(c);moved++;found=true;break;
 }
 if(!found){apply(0,0);placed.push(t.getBBox());issues.push(t.textContent.trim());}
}
return {moved,issues};
}
