import json,subprocess,urllib.parse,time,sys
UA='ArtCards/3.0 (educational, non-commercial)'
def sparql(q,tries=3):
    for k in range(tries):
        r=subprocess.run(['curl','-s','-m','90','-A',UA,'-H','Accept: application/sparql-results+json',
                          '-G','--data-urlencode','query='+q,'https://query.wikidata.org/sparql'],capture_output=True)
        try: return json.loads(r.stdout)
        except Exception: time.sleep(4*(k+1))
    return None
def works_of(qid,limit=14,prop='P170'):
    """prop: P170=creator(绘画/雕塑) | P84=architect(建筑)"""
    TYPES = ('wd:Q3305213 wd:Q93184 wd:Q11060274 wd:Q860861 wd:Q15711026 wd:Q125191 wd:Q1885014 wd:Q4502142' if prop=='P170'
             else 'wd:Q41176 wd:Q811979 wd:Q1021645 wd:Q24354 wd:Q16970 wd:Q33506 wd:Q11303')
    q=f'''SELECT ?w ?wLabel ?img ?date ?matLabel ?locLabel ?links WHERE {{
  ?w wdt:{prop} wd:{qid}; wdt:P18 ?img; wikibase:sitelinks ?links.
  ?w wdt:P31/wdt:P279* ?type. VALUES ?type {{ {TYPES} }}
  OPTIONAL {{ ?w wdt:P571 ?date. }} OPTIONAL {{ ?w wdt:P186 ?mat. }} OPTIONAL {{ ?w wdt:P276 ?loc. }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "zh,zh-cn,zh-hans,en". }}
}} ORDER BY DESC(?links) LIMIT {limit*3}'''
    d=sparql(q)
    if not d: return []
    seen={}
    for b in d['results']['bindings']:
        w=b['w']['value'].rsplit('/',1)[-1]
        if w in seen: continue
        seen[w]={'qid':w,'t':b['wLabel']['value'],'img':b['img']['value'],
                 'y':b.get('date',{}).get('value','')[:4],
                 'mat':b.get('matLabel',{}).get('value',''),
                 'loc':b.get('locLabel',{}).get('value',''),
                 'links':int(b['links']['value'])}
        if len(seen)>=limit: break
    return list(seen.values())
def qid_of(en_title):
    """英文维基条目名 → QID(最可靠的解析方式)"""
    u='https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageprops&ppprop=wikibase_item&redirects=1&titles='+urllib.parse.quote(en_title)
    for k in range(3):
        r=subprocess.run(['curl','-s','-m','40','-A',UA,u],capture_output=True)
        try:
            p=list(json.loads(r.stdout)['query']['pages'].values())[0]
            return p.get('pageprops',{}).get('wikibase_item')
        except Exception: time.sleep(2)
    return None
