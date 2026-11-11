"""Offline checks for page coverage, local assets, fragments and placeholder routes."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.links=[];self.h1=0;self.title=False;self.feed(text)
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.append(d['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  for key in ['href','src','action']:
   if d.get(key):self.links.append(d[key])
errors=[];pages={p.name:Page(p.read_text()) for p in ROOT.glob('*.html')}
for name,page in pages.items():
 if page.h1!=1:errors.append(f'{name}: expected one h1, got {page.h1}')
 if len(page.ids)!=len(set(page.ids)):errors.append(f'{name}: duplicate ids')
 for value in page.links:
  u=urlsplit(value)
  if u.scheme or u.netloc:continue
  if value.startswith('/'):
   errors.append(f'{name}: unresolved root route {value}');continue
  target=unquote(u.path) or name
  if not (ROOT/target).is_file():errors.append(f'{name}: missing local target {value}');continue
  if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{name}: missing fragment {value}')
coverage=json.loads((ROOT/'assets/data/content-coverage.json').read_text())
for page in coverage['generated_pages']:
 if page['page'] not in pages:errors.append('Missing required page '+page['page'])
for name in ['index.html','home.html','how-to-apply.html']:
 if not any(marker in (ROOT/name).read_text() for marker in ['data-enquiry-form','data-registration-form']):errors.append(name+': enquiry form missing')
for name in ['undergraduate-courses.html','postgraduate-courses.html']:
 s=(ROOT/name).read_text()
 if 'data-course="' in s or 'class="sr-only">Explore undergraduate courses' in s:errors.append(name+': placeholder course card remains')
for js in (ROOT/'assets/js').glob('*.js'):
 if js.name in ['form-data.js','course-listings.js','how-to-apply.js']:continue
 if 'TODO(sitecore)' in js.read_text():errors.append(str(js)+': unfinished submission code')
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print(f'PASS: {len(pages)} HTML files; required screens, local links, fragments, assets and course cards verified.')
