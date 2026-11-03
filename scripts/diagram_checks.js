()=>{
let svg=document.querySelector('svg.edges'),v=svg.viewBox.baseVal,c=document.querySelector('.canvas'),topology=c.classList.contains('topology');
const paths=[...svg.querySelectorAll(':scope > path[marker-end]')],labels=[...svg.querySelectorAll(':scope > text[data-edge]')];let issues=[];
let hit=(a,b,g=0)=>a.x<b.x+b.width-g&&b.x<a.x+a.width-g&&a.y<b.y+b.height-g&&b.y<a.y+a.height-g;
function dist(p,b){let L=p.getTotalLength(),d=1e9;for(let k=0;k<=L;k+=Math.max(1,L/500)){let q=p.getPointAtLength(k);d=Math.min(d,Math.hypot(Math.max(b.x-q.x,0,q.x-b.x-b.width),Math.max(b.y-q.y,0,q.y-b.y-b.height)))}return d}
for(let t of svg.querySelectorAll(':scope > text')){let b=t.getBBox();if(b.x<v.x||b.y<v.y||b.x+b.width>v.x+v.width||b.y+b.height>v.y+v.height)issues.push(['bounds',t.textContent]);}
for(let t of labels){let b=t.getBBox(),p=paths.find(p=>p.dataset.edge===t.dataset.edge);if(!p)issues.push(['missing-edge',t.textContent]);else if(dist(p,b)>22)issues.push(['distant-label',t.textContent,dist(p,b)]);
 for(let other of paths)if(other!==p&&dist(other,b)<1)issues.push(['other-edge-crosses-label',t.textContent,other.dataset.edge]);
}
for(let i=0;i<labels.length;i++)for(let j=i+1;j<labels.length;j++)if(hit(labels[i].getBBox(),labels[j].getBBox(),1))issues.push(['label-overlap',labels[i].textContent,labels[j].textContent]);
const sr=svg.getBoundingClientRect();let nodes=[...document.querySelectorAll('.node')];
for(let n of nodes){let b=n.getBoundingClientRect();if(b.left<sr.left-1||b.right>sr.right+1||b.top<sr.top-1||b.bottom>sr.bottom+1)issues.push(['node-bounds',n.innerText]);}
return {topology,arrows:paths.length,labels:labels.length,issues};
}
