import os
from pathlib import Path

services=[d.name for d in Path('.').iterdir() if d.is_dir() and d.name.startswith('service-')]
Path('public').mkdir(exist_ok=True)

def color(p):
    return '#4c1' if p>=50 else '#dfb317' if p>=20 else '#e05d44'

rows=[]
for service in services:
    total=0
    ai=0
    for root,_,files in os.walk(service):
        for file in files:
            if not file.endswith('.java'):
                continue
            inside=False
            with open(os.path.join(root,file),encoding='utf-8') as f:
                for line in f:
                    t=line.strip()
                    if not t:
                        continue
                    total+=1
                    if 'AI START' in t:
                        inside=True
                        continue
                    if 'AI END' in t:
                        inside=False
                        continue
                    if inside:
                        ai+=1
    pct=round(ai*100/total,1) if total else 0
    rows.append((service,pct))
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="150" height="20"><rect width="85" height="20" fill="#555"/><rect x="85" width="65" height="20" fill="%s"/><text x="42" y="14" fill="white" font-size="11" text-anchor="middle">%s</text><text x="117" y="14" fill="white" font-size="11" text-anchor="middle">%s%%</text></svg>'%(color(pct),service,pct)
    open('public/%s.svg'%service,'w').write(svg)

html='<html><body><h2>AI Coverage</h2><table border="1"><tr><th>Service</th><th>Coverage</th></tr>'
for s,p in rows:
    html+='<tr><td>%s</td><td>%s%%</td></tr>'%(s,p)
html+='</table></body></html>'
open('public/index.html','w').write(html)
