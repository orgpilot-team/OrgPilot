"""Local Markdown link inventory. No network or product code is used."""
from pathlib import Path
import re, unicodedata
from urllib.parse import unquote

def active_text(text):
    lines=[];fence=None
    for line in text.splitlines(True):
        m=re.match(r'^\s{0,3}(`{3,}|~{3,})',line)
        if m:
            if fence is None:fence=m[1][0]
            elif m[1][0]==fence:fence=None
            lines.append('\n');continue
        lines.append(line if fence is None else '\n')
    return re.sub(r'<!--.*?-->','', ''.join(lines),flags=re.S)

def anchors(text):
    text=active_text(text)
    found=set(re.findall(r'<(?:a|h[1-6])\b[^>]*(?:id|name)=["\']([^"\']+)',text,re.I))
    used={}
    for line in text.splitlines():
        m=re.match(r'^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$',line)
        if not m:continue
        heading=re.sub(r'<[^>]*>','',m[1]);heading=re.sub(r'!?\[([^]]*)\]\([^)]*\)',r'\1',heading)
        slug=''.join(c for c in heading.lower() if c in ['-','_',' '] or unicodedata.category(c)[0] in ['L','M','N'] or c=='\u200c').replace(' ','-')
        n=used.get(slug,0);used[slug]=n+1;found.add(slug+(f'-{n}' if n else ''))
    return found

def markdown_links(text):
    """Yield span, URL, line, kind. Parentheses in destinations are balanced."""
    active=active_text(text)
    for m in re.finditer(r'!?\[[^\]\n]*\]\(',active):
        start=m.end();pos=start;level=1;angle=pos<len(active) and active[pos]=='<'
        if angle:
            end=active.find('>',pos+1)
            if end<0:continue
            url=active[pos+1:end];span=(pos+1,end)
        else:
            while pos<len(active):
                c=active[pos]
                if c=='\\':pos+=2;continue
                if c=='(':level+=1
                if c==')':
                    level-=1
                    if level==0:break
                if c.isspace() and level==1:break
                pos+=1
            url=active[start:pos];span=(start,pos)
        if url:yield span,url,active[:m.start()].count('\n')+1,'inline'
    for m in re.finditer(r'^ {0,3}\[[^]]+\]:\s*(?:<([^>]+)>|(\S+))',active,re.M):
        which=1 if m[1] is not None else 2
        yield m.span(which),m[which],active[:m.start()].count('\n')+1,'reference-definition'
    for m in re.finditer(r'\b(?:href|src)=["\']([^"\']+)["\']',active,re.I):
        yield m.span(1),m[1],active[:m.start()].count('\n')+1,'html'

def resolve(root,origin,url):
    if re.match(r'^(?:[A-Za-z][A-Za-z0-9+.-]*:|//)',url):return dict(state='External or host URL',target='',anchor='')
    name,_,fragment=url.partition('#');name=unquote(name).split('?',1)[0];fragment=unquote(fragment)
    target=(root/name.lstrip('/')) if name.startswith('/') else (origin.parent/name) if name else origin
    target=target.resolve()
    if not target.exists():state='Missing file'
    elif fragment and target.suffix.lower()=='.md' and fragment not in anchors(target.read_text(encoding='utf-8-sig')):state='Missing anchor'
    else:state='Resolved'
    try:rel=target.relative_to(root).as_posix()
    except ValueError:rel=str(target)
    return dict(state=state,target=rel,anchor=fragment)

def inventory(root,paths):
    rows=[]
    for path in paths:
        text=path.read_text(encoding='utf-8-sig')
        for _,url,line,kind in markdown_links(text):
            rows.append(dict(source_file=path.relative_to(root).as_posix(),line=line,url=url,kind=kind,**resolve(root,path,url)))
    return rows
