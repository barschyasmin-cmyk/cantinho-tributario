#!/usr/bin/env python3
"""Coleta RSS oficiais e publica notícias com origem, sem inferir efeitos jurídicos."""
import json, re, hashlib, html, unicodedata
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"site/news/updates.json"
SOURCES=[
 ("Receita Federal","https://www.gov.br/receitafederal/pt-br/assuntos/noticias/RSS"),
 ("STJ","https://res.stj.jus.br/hrestp-c-portalp/RSS.xml"),
 ("STJ · Informativo","https://processo.stj.jus.br/jurisprudencia/externo/InformativoFeed"),
 ("Agência Senado","https://www12.senado.leg.br/noticias/feed/todasnoticias/RSS"),
]
TERMS=("tribut","fisc","impost","icms","iss","pis","cofins","cbs","ibs","contribuic","arrecad","aduan","carf","repetitiv","repercussao geral","divida ativa","nfs-e","nfse","nota fiscal","aliquot","incentivo","transacao","receita federal","reforma tributaria","credito presumido","restituicao","irpj","csll","irpf","taxacao","stf","stj")
class Stripper(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[]
 def handle_data(self,d): self.parts.append(d)
def plain(t):
 p=Stripper()
 try:p.feed(html.unescape(t or ""))
 except Exception:pass
 return re.sub(r"\s+"," ",html.unescape(" ".join(p.parts))).strip()
def norm(t):return "".join(c for c in unicodedata.normalize("NFKD",t.lower()) if not unicodedata.combining(c))
def tag(t):return t.rsplit("}",1)[-1]
def child(n,key):
 for c in n:
  if tag(c.tag)==key and c.text:return c.text.strip()
 return ""
def dtparse(t):
 if not t:return None
 try:d=parsedate_to_datetime(t)
 except Exception:
  try:d=datetime.fromisoformat(t.replace("Z","+00:00"))
  except Exception:return None
 return d.replace(tzinfo=timezone.utc).astimezone(timezone.utc) if d.tzinfo is None else d.astimezone(timezone.utc)
def items(xml):
 root=ET.fromstring(xml)
 for n in root.iter():
  if tag(n.tag) not in ("item","entry"):continue
  title=plain(child(n,"title"))
  summary=plain(child(n,"description") or child(n,"summary") or child(n,"content"))
  link=child(n,"link")
  if not link:
   for c in n:
    if tag(c.tag)=="link" and c.attrib.get("rel","alternate") in ("alternate",""):
     link=c.attrib.get("href","");break
  date=dtparse(child(n,"pubDate") or child(n,"published") or child(n,"updated"))
  if title and link.startswith("https://") and date:yield title,summary,link,date
def entry(title,summary,link,dt,org,today):
 date=dt.date().isoformat();summary=summary[:850] or "Consulte a publicação oficial para os detalhes."
 cat="Jurisprudência" if org.startswith("STJ") else ("Reforma Tributária" if any(x in norm(title) for x in ("reforma","ibs","cbs")) else "Atualização tributária")
 return dict(id="auto-"+hashlib.sha256(link.encode()).hexdigest()[:16],automated=True,title=title[:220],date=date,published=date,checked=today,addedAt=dt.isoformat(),org=org,trib="A identificar",category=cat,kind="Notícia oficial (coleta automática)",impact="A avaliar",status="Efeitos jurídicos a verificar",stage="Publicação identificada",summary=summary,source=link,sourceName=org+" · publicação oficial",topics=[org],question="O que esta publicação informa e quais efeitos precisam de conferência?",why="Consulte a fonte e os atos citados para verificar o alcance jurídico.",before="Cenário anterior a verificar na legislação e jurisprudência.",now="Publicação oficial identificada em "+date+".",watch="Conferir íntegra, vigência e próximos eventos.",sections={"aconteceu":org+" publicou: "+title+". "+summary,"contexto":"Os antecedentes exigem leitura dos atos relacionados.","discussao":"A controvérsia precisa de conferência na fonte integral.","decisao":"A identificação da notícia não confirma tese fixada nem julgamento concluído.","mudanca":"É necessário comparar os documentos anteriores e atuais.","impactos":"Verifique sujeitos afetados, riscos, oportunidades e efeitos processuais.","aberto":"Confirmar regulamentações, recursos e pendências.","acompanhar":"Acesse o link oficial para acompanhar os próximos eventos."},timeline=[[date,"Publicação detectada", "Efeitos jurídicos a conferir"]])
def main():
 now=datetime.now(timezone.utc);today=now.date().isoformat();old={}
 if OUT.exists():
  try:old={e["id"]:e for e in json.loads(OUT.read_text()).get("entries",[]) if e.get("id","").startswith("auto-")}
  except Exception:pass
 results={};stats=[];ok=0
 for org,url in SOURCES:
  try:
   req=Request(url,headers={"User-Agent":"Mozilla/5.0 (CantinhoTributario/1.0)","Accept":"application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9"})
   with urlopen(req,timeout=25) as f:xml=f.read(2500000)
   count=0
   for title,summary,link,date in items(xml):
    if date<now-timedelta(days=120) or date>now+timedelta(days=2):continue
    if not any(x in norm(title+" "+summary) for x in TERMS):continue
    e=entry(title,summary,link,date,org,today);results[e["id"]]=e;count+=1
   ok+=1;stats.append({"org":org,"ok":True,"items":count})
  except Exception as ex:stats.append({"org":org,"ok":False,"error":str(ex)[:180]})
 for key,e in old.items():
  if key not in results:
   try:
    if (now.date()-datetime.fromisoformat(e["published"]).date()).days<=120:results[key]=e
   except Exception:pass
 if not ok:
  print("Fontes indisponíveis; arquivo anterior mantido")
  return 0 if OUT.exists() else 1
 data={"kind":"official-publication-feed","checkedAt":now.isoformat(timespec="seconds"),"lastSuccessfulRun":now.isoformat(timespec="seconds"),"sources":stats,"entries":sorted(results.values(),key=lambda e:e["published"],reverse=True)[:250],"notice":"Publicações importadas automaticamente; os efeitos jurídicos ainda exigem conferência."}
 OUT.parent.mkdir(parents=True,exist_ok=True)
 OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
 print("Atualizado:",len(data["entries"]),"publicações;",ok,"fontes consultadas.")
 return 0
if __name__=="__main__":raise SystemExit(main())
