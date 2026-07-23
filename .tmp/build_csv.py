#!/usr/bin/env python3
import json, re, csv, os, sys
from collections import defaultdict

TR = "/Users/casey/.claude/projects/-Users-casey-fs-tq-marvin-template/abede70a-5ff6-479b-bcc4-00bc6320b595/tool-results"
TMP = "/Users/casey/fs-tq-marvin-template/.tmp"
OUT = "/Users/casey/fs-tq-marvin-template/energy-contacts-FULL__CaseyClark__20260618.csv"

RUN_ID = "CaseyClark-20260618"
EXTRACTED_BY = "Casey Clark"
EXTRACTED_DATE = "2026-06-18"

SOURCES = {
    "Gmail":   (os.path.join(TR, "toolu_01YFgoEwtBHu9Kaq3rXxb7Xe.json"), "wrapped", "Email"),
    "Slack":   (os.path.join(TR, "toolu_013izhmsH9BenU6eCFwT5HLn.json"), "wrapped", "Slack"),
    "Calendar":(os.path.join(TR, "energy_contacts.json"), "raw", "Calendar"),
    "Granola": (os.path.join(TR, "toolu_01Q1v8Ey8UF8ynB7GMoPM3rf.json"), "wrapped", "Granola"),
    "Drive":   (os.path.join(TR, "toolu_01EST5jYpcAXzuA1j6Dvzj4g.json"), "wrapped", "Drive"),
    "Notion":  (os.path.join(TMP, "src_notion.json"), "raw", "Notion"),
    "Kaiser":  (os.path.join(TMP, "src_kaiser.json"), "raw", "Kaiser"),
}
# fill priority (lower = authoritative, fills first)
PRIO = {"Kaiser":1,"Drive":2,"Gmail":3,"Granola":4,"Calendar":5,"Notion":6,"Slack":7}

def extract_json_array(text):
    arrays = []
    for m in re.finditer(r"```json\s*(.*?)```", text, re.DOTALL):
        blk = m.group(1).strip()
        try:
            v = json.loads(blk)
            if isinstance(v, list): arrays.append(v)
        except Exception: pass
    if arrays:
        return max(arrays, key=len)
    # fallback: first balanced [ ... ]
    start = text.find('[')
    if start < 0: return []
    depth=0
    for i in range(start, len(text)):
        if text[i]=='[': depth+=1
        elif text[i]==']':
            depth-=1
            if depth==0:
                try:
                    v=json.loads(text[start:i+1])
                    if isinstance(v,list): return v
                except Exception: pass
                break
    return []

def load_source(name):
    path, kind, _ = SOURCES[name]
    raw = open(path, encoding="utf-8").read()
    if kind == "raw":
        data = json.loads(raw)
        if data and isinstance(data[0], dict) and "_site_map" in data[0]:
            data = data[1:]
        return data
    # wrapped: [{type,text},...]
    try:
        parts = json.loads(raw)
        text = "".join(p.get("text","") for p in parts if isinstance(p,dict))
    except Exception:
        text = raw
    return extract_json_array(text)

SITE_MAP = {
 "IND1":("Meridian Compute - New Lebanon, IN","MISO","IN"),
 "BUF1":("TeraWulf - Buffalo, NY","NYISO","NY"),
 "SNK1":("Cipher - Colorado City, TX","ERCOT","TX"),
 "MSY1":("Hut8 - Riverbend, LA","MISO","LA"),
 "LBB1":("Fluidstack - Abernathy, TX","ERCOT","TX"),
 "TUL1":("Coatue - Okmulgee, OK","SPP","OK"),
 "IAH1":("Stream - Houston, TX","ERCOT","TX"),
 "HOU2":("CleanSpark - Sealy, TX","ERCOT","TX"),
 "1000JCT":("Ascendant Energy - Mountain Home, TX","ERCOT","TX"),
 "1000TPL":("BKV - Temple, TX","ERCOT","TX"),
 "1000ZOS":("Brookhaven - Yaphank, NY","NYISO","NY"),
 "1000WPC":("Captus Generation - Pincher Creek, AB","Other","Alberta"),
 "1000PPA":("Fermi America - Amarillo, TX","ERCOT","TX"),
 "1000FST":("Pacifico Energy - Fort Stockton, TX","ERCOT","TX"),
 "DYS1":("Trailblazer Infrastructure - Sweetwater, TX","ERCOT","TX"),
 "1000AUS":("Zydeco - Bastrop, TX","ERCOT","TX"),
 "PHL2":("PSEG - Trenton, NJ","PJM","NJ"),
 "MDW1":("Vistra - Minooka, IL","PJM","IL"),
 "HTS2":("Cleveland Cliffs - Ashland, KY","PJM","KY"),
 "1000ABE":("Prologis / Northampton PA","PJM","PA"),
}

US_ABBR = {"texas":"TX","indiana":"IN","virginia":"VA","ohio":"OH","new york":"NY","new jersey":"NJ",
 "illinois":"IL","kentucky":"KY","louisiana":"LA","oklahoma":"OK","arizona":"AZ","florida":"FL",
 "alabama":"AL","georgia":"GA","pennsylvania":"PA","new mexico":"NM","colorado":"CO","michigan":"MI",
 "california":"CA","arkansas":"AR","west virginia":"WV","tennessee":"TN","north carolina":"NC"}

REGION = {
 "NY":"Northeast","NJ":"Northeast","CT":"Northeast","MA":"Northeast","RI":"Northeast","VT":"Northeast","NH":"Northeast","ME":"Northeast","PA":"Mid-Atlantic","VA":"Mid-Atlantic","MD":"Mid-Atlantic","DE":"Mid-Atlantic","DC":"Mid-Atlantic","WV":"Mid-Atlantic",
 "FL":"Southeast","GA":"Southeast","AL":"Southeast","MS":"Southeast","SC":"Southeast","NC":"Southeast","TN":"Southeast","KY":"Southeast","LA":"Southeast","AR":"Southeast",
 "IN":"Midwest","IL":"Midwest","OH":"Midwest","MI":"Midwest","WI":"Midwest","MN":"Midwest","IA":"Midwest","MO":"Midwest","KS":"Midwest","ND":"Midwest","SD":"Midwest","NE":"Midwest",
 "TX":"Texas",
 "CO":"Mountain West","AZ":"Mountain West","NM":"Mountain West","UT":"Mountain West","NV":"Mountain West","MT":"Mountain West","WY":"Mountain West","ID":"Mountain West","OK":"Other",
 "CA":"West Coast","OR":"West Coast","WA":"West Coast",
}
TZ = {
 "NY":"ET","NJ":"ET","CT":"ET","MA":"ET","RI":"ET","VT":"ET","NH":"ET","ME":"ET","PA":"ET","VA":"ET","MD":"ET","DE":"ET","DC":"ET","WV":"ET","FL":"ET","GA":"ET","SC":"ET","NC":"ET","OH":"ET","MI":"ET","IN":"ET","KY":"ET","TN":"CT",
 "TX":"CT","IL":"CT","WI":"CT","MN":"CT","IA":"CT","MO":"CT","KS":"CT","NE":"CT","ND":"CT","SD":"CT","LA":"CT","AR":"CT","MS":"CT","AL":"CT","OK":"CT",
 "CO":"MT","AZ":"MT","NM":"MT","UT":"MT","WY":"MT","MT":"MT","ID":"MT",
 "CA":"PT","OR":"PT","WA":"PT","NV":"PT",
}
ISO_BY_STATE = {"TX":"ERCOT","IN":"MISO","LA":"MISO","OK":"SPP","NY":"NYISO","NJ":"PJM","VA":"PJM","PA":"PJM","OH":"PJM","IL":"PJM","KY":"PJM","WV":"PJM","MD":"PJM","DE":"PJM","NC":"PJM",
 "FL":"Non-ISO","GA":"Non-ISO","AL":"Non-ISO","MS":"Non-ISO","SC":"Non-ISO","TN":"Non-ISO","CA":"CAISO","AZ":"Non-ISO","NM":"Non-ISO","CO":"Non-ISO","NV":"Non-ISO","UT":"Non-ISO"}
NERC_BY_ISO = {"ERCOT":"Texas RE","PJM":"RF","NYISO":"NPCC","SPP":"MRO","CAISO":"WECC","MISO":"MRO","ISO-NE":"NPCC"}

VALID_ISO = {"ERCOT","MISO","PJM","NYISO","SPP","SERC","CAISO","ISO-NE","Non-ISO","Other","Unknown"}

def norm_state(rec):
    s = (rec.get("state_guess") or rec.get("state") or "").strip()
    if not s: return ""
    # may contain multiple like "OH / AZ / IN" -> take first 2-letter
    toks = re.split(r"[/,;]", s)
    for t in toks:
        t=t.strip()
        if len(t)==2 and t.isalpha(): return t.upper()
        if t.lower() in US_ABBR: return US_ABBR[t.lower()]
    # try search words
    low = s.lower()
    for name,ab in US_ABBR.items():
        if name in low: return ab
    if "alberta" in low: return ""
    return ""

def clean_phone(p):
    if not p: return ""
    p=str(p)
    digits = re.sub(r"[^\d+]","",p)
    d = re.sub(r"\D","",p)
    if p.strip().startswith("+"):
        return "+"+d
    if len(d)==10: return "+1"+d
    if len(d)==11 and d.startswith("1"): return "+"+d
    return p.strip()

def classify_org(rec):
    """return (org_type, stakeholder_class, ownership, value_chain, commodity)"""
    name=(rec.get("org_name") or "").lower()
    g=(rec.get("org_type_guess") or "").lower()
    sg=(rec.get("stakeholder_class_guess") or "").lower()
    # IMPORTANT: classify from identity fields only (org_name + guesses).
    # Do NOT include relationship_summary/notes/project_hints — they mention
    # third-party orgs and contaminate the match.
    blob=" ".join([name,g,sg])
    def has(*ks): return any(k in blob for k in ks)
    ot=None
    # regulators first
    if has("ferc"): ot="Regulator — Federal (FERC)"
    elif has("nerc","reliabilityfirst","texas re","serc reliability","reliability entity"): ot="Regulator — Reliability (NERC/RE)"
    elif has("puct","public utility commission","iurc","psc","public service commission"," scc","corporation commission","puc "): ot="Regulator — State (PUC/PSC)"
    elif has("environmental","air permit","deq","ecology","epa "," tceq"): ot="Environmental/Permitting Agency"
    elif has("economic development","chamber","edd","ed3 economic","enterprise zone","edc "): ot="Economic Development Agency"
    # ISO/RTO
    elif name.strip() in ("ercot","pjm","miso","nyiso","spp","caiso","iso-ne","isone") or has("iso/rto","independent system operator","grid operator","rto "): ot="ISO/RTO"
    # transmission
    elif has("transmission service","tsp","itc transmission"," tso") or ("transmission" in name): ot="Transmission Owner/Operator (TO/TSP/TSO)"
    # gas
    elif has("interstate pipeline","midstream","transwestern","energy transfer","marabou","gas pipeline"): ot="Interstate Gas Pipeline"
    elif has("gas utility","ldc","atmos","one gas","spire","texas gas service","gas company"): ot="Gas Utility/LDC"
    elif has("gas marketer","gas supplier"): ot="Gas Marketer/Supplier"
    # federal power
    elif has("tva","tennessee valley","bonneville","bpa","wapa","western area power"): ot="Federal Power Authority (TVA/BPA/WAPA)"
    # cooperatives
    elif has("g&t","generation and transmission","aeci","hoosier energy","wvpa","wabash valley"): ot="Electric Co-op (G&T)"
    elif has("cooperative","co-op","recc","rec ","emc","electric coop","tonto"): ot="Electric Co-op (Distribution)"
    # muni / public power
    elif has("lcra","municipal","public power","muni ","nypa","bwl","board of water and light","city of "): ot="Electric Muni/Public Power"
    # IOU
    elif has("aep","american electric power","appalachian power","duke energy","dominion","ppl","nipsco","aes indiana","oncor","centerpoint","pseg","public service enterprise","pg&e","pacific gas","national grid","con edison","consolidated edison","evergy","entergy","xcel","alabama power","southern company","georgia power","fpl","florida power","nextera energy","tnmp","texas-new mexico","ed3","tucson electric","aps ","arizona public","investor-owned","iou"): ot="Electric IOU"
    # BTM / onsite gen
    elif has("fuel cell","bloom","microgrid","behind-the-meter","behind the meter","btm","voltagrid","propwr","propower","reciprocating","onsite generation","solar turbines","caterpillar gas"): ot="Behind-the-Meter/Onsite Generation"
    # generation / IPP
    elif has("ipp","independent power","generation developer","vistra","talen","calpine","nrg","tenaska","ls power","cpv","clearway","brookfield","orsted","edp","capital power","bkv","beowulf","captus","bilateral energy","terrapower","power producer"," genco"): ot="Generation Developer/IPP"
    # offtaker / end user
    elif has("anthropic","openai","microsoft","meta ","amazon","google","oracle","coatue","hyperscaler","offtaker","end user","data center customer"): ot="Data Center End User/Offtaker"
    # outside counsel
    elif has("llp","attorney","counsel","law firm"," law "): ot="Outside Counsel"
    # power systems modeling
    elif has("pss/e","pss-e","pscad","emt model","power systems modeling","load flow"): ot="Power Systems Modeling Firm"
    # EPC / engineering
    elif has("epc","engineering","hdr","burns & mcdonnell","burns and mcdonnell","black & veatch","b&v","kimley","stantec","jacobs","bowman","colliers eng","ramboll","quanta","qisg","adag","fusion","aecom","sargent","ulteig","power engineers"): ot="Engineering/EPC"
    # equipment
    elif has("transformer","switchgear","gsu","abb","schneider","powell","sieyuan","trane","carrier","equipment","hypertec","gis ","breaker"): ot="Equipment Supplier"
    # consultant / advisor
    elif has("consultant","advisor","advisory","orennia","geoforge","analytics","diligence","ramboll"): ot="Energy Consultant/Advisor"
    # brokers / land developers -> Other
    elif has("broker","brokerage","newmark","cbre","real estate","powered-land developer","powered land developer","land divestiture","seller","originator","raeden","blackbird","velox","cleveland-cliffs","cleveland cliffs","prologis"): ot="Other"
    else: ot="Other"

    # marketing arm of a utility -> wholesale supplier, not IOU
    if ot=="Electric IOU" and ("marketing" in name or "marketer" in name or "wholesale" in name):
        ot="Power Marketer/Wholesale Supplier"

    # fallback: rescue common energy types from the agent's guess before settling on Other
    if ot=="Other":
        if has("power developer","power producer","generation","ipp","genco","energy developer","power plant","hydrogen power","renewable","solar","wind","gas turbine power"): ot="Generation Developer/IPP"
        elif has("fuel cell","onsite generation","microgrid","reciprocating","distributed generation","dg "): ot="Behind-the-Meter/Onsite Generation"
        elif has("crypto","miner","mining","compute","offtaker","data center customer","hyperscaler","end user"): ot="Data Center End User/Offtaker"
        elif has("consult","advisor","advisory","analytics","diligence"): ot="Energy Consultant/Advisor"
        elif has("engineering","epc"): ot="Engineering/EPC"
        elif has("equipment","supplier","hardware","manufactur"): ot="Equipment Supplier"
        elif has("utility","iou") and "water" not in name: ot="Electric IOU"
        elif has("gas marketer","gas supplier"): ot="Gas Marketer/Supplier"
        elif has("midstream","pipeline","gas transport"): ot="Interstate Gas Pipeline"
        elif has("county","city of","chamber","economic development","authority","port "): ot="Economic Development Agency"

    # stakeholder_class
    grid={"Electric IOU","Electric Co-op (Distribution)","Electric Co-op (G&T)","Electric Muni/Public Power","Federal Power Authority (TVA/BPA/WAPA)","Gas Utility/LDC","Interstate Gas Pipeline","ISO/RTO","Transmission Owner/Operator (TO/TSP/TSO)","Merchant/Independent Transmission Developer","Generation Developer/IPP","Behind-the-Meter/Onsite Generation"}
    commercial={"Gas Marketer/Supplier","Power Marketer/Wholesale Supplier","Retail Electric Provider (REP)","QSE/Scheduling Coordinator","Hedge/Financial Counterparty","Capacity/ZRC/REC Counterparty","Demand Response/Curtailment"}
    regpol={"Regulator — State (PUC/PSC)","Regulator — Federal (FERC)","Regulator — Reliability (NERC/RE)","Environmental/Permitting Agency","Economic Development Agency"}
    advisory={"Energy Consultant/Advisor","Power Systems Modeling Firm","Engineering/EPC","Outside Counsel"}
    if ot in grid: sc="Supply/Grid"
    elif ot in commercial: sc="Commercial/Portfolio"
    elif ot in regpol: sc="Regulatory/Policy"
    elif ot in advisory: sc="Advisory"
    elif ot=="Equipment Supplier": sc="Equipment/Vendor"
    elif ot=="Data Center End User/Offtaker": sc="End User/Customer"
    else: sc="Other"

    # ownership
    own_map={"Electric IOU":"Investor-Owned","Gas Utility/LDC":"Investor-Owned","Interstate Gas Pipeline":"Private/Independent","Gas Marketer/Supplier":"Private/Independent",
     "Electric Co-op (Distribution)":"Cooperative","Electric Co-op (G&T)":"Cooperative",
     "Electric Muni/Public Power":"State/Public Authority","Federal Power Authority (TVA/BPA/WAPA)":"Federal",
     "ISO/RTO":"Private/Independent","Transmission Owner/Operator (TO/TSP/TSO)":"Investor-Owned",
     "Generation Developer/IPP":"Private/Independent","Behind-the-Meter/Onsite Generation":"Private/Independent",
     "Regulator — State (PUC/PSC)":"Government Agency","Regulator — Federal (FERC)":"Government Agency","Regulator — Reliability (NERC/RE)":"Government Agency",
     "Environmental/Permitting Agency":"Government Agency","Economic Development Agency":"Government Agency",
     "Energy Consultant/Advisor":"Private/Independent","Power Systems Modeling Firm":"Private/Independent","Engineering/EPC":"Private/Independent","Outside Counsel":"Private/Independent",
     "Equipment Supplier":"Private/Independent","Data Center End User/Offtaker":"Private/Independent"}
    own=own_map.get(ot,"Unknown")
    if "lcra" in blob or "nypa" in blob: own="State/Public Authority"

    # value chain
    vc_map={"Electric IOU":"Distribution","Electric Co-op (Distribution)":"Distribution","Electric Co-op (G&T)":"Generation","Electric Muni/Public Power":"Distribution","Federal Power Authority (TVA/BPA/WAPA)":"Generation",
     "Gas Utility/LDC":"Distribution","Interstate Gas Pipeline":"Transmission","Gas Marketer/Supplier":"Wholesale Market",
     "ISO/RTO":"Wholesale Market","Transmission Owner/Operator (TO/TSP/TSO)":"Transmission",
     "Generation Developer/IPP":"Generation","Behind-the-Meter/Onsite Generation":"Generation",
     "Regulator — State (PUC/PSC)":"Regulatory","Regulator — Federal (FERC)":"Regulatory","Regulator — Reliability (NERC/RE)":"Regulatory","Environmental/Permitting Agency":"Regulatory","Economic Development Agency":"Regulatory",
     "Equipment Supplier":"Equipment","Data Center End User/Offtaker":"Customer"}
    vc=vc_map.get(ot,"Unknown")

    # commodity
    cf_guess=(rec.get("commodity_focus_guess") or "").lower()
    if ot in ("Gas Utility/LDC","Interstate Gas Pipeline","Gas Marketer/Supplier"): cf="Gas"
    elif ot=="Behind-the-Meter/Onsite Generation":
        cf="Gas" if has("gas","fuel cell","bloom","turbine") else "Electric"
    elif "both" in cf_guess or has("combined electric+gas","electric and gas"): cf="Both"
    elif ot in grid or ot in ("Transmission Owner/Operator (TO/TSP/TSO)","ISO/RTO"): cf="Electric"
    elif "gas" in cf_guess: cf="Gas"
    elif "electric" in cf_guess: cf="Electric"
    elif ot in regpol or ot in advisory or ot=="Equipment Supplier": cf="N/A"
    else: cf="Unknown"
    return ot,sc,own,vc,cf

def seniority(title):
    t=(title or "").lower()
    if not t: return "Unknown"
    if any(k in t for k in ["ceo","cfo","cto","coo","chief","president","founder","owner","partner","managing director"]): return "C-Suite"
    if any(k in t for k in ["svp","evp","executive vice","senior vice"]): return "SVP/EVP"
    if "vice president" in t or re.search(r"\bvp\b",t): return "VP"
    if "director" in t or "head of" in t: return "Director"
    if any(k in t for k in ["manager","lead","principal"]): return "Manager"
    if any(k in t for k in ["coordinator","analyst","engineer","specialist","associate","representative"]): return "IC"
    return "Unknown"

def decision_role(title):
    t=(title or "").lower()
    if not t: return "Unknown"
    if any(k in t for k in ["ceo","president","founder","owner","chief","managing director"]): return "Decision Maker"
    if any(k in t for k in ["svp","evp","vp","vice president","director","head of"]): return "Influencer"
    if any(k in t for k in ["engineer","analyst","coordinator","planner","specialist","technical"]): return "Technical/SME"
    return "Unknown"

def norm_conf(c):
    c=(c or "").lower()
    if "high" in c: return "High"
    if "med" in c: return "Medium"
    if "low" in c: return "Low"
    return "Low"

def norm_verif(v):
    v=(v or "").lower()
    if "needs review" in v or "ambiguous" in v: return "Needs Review"
    if v.startswith("verified") or v=="verified": return "Verified"
    if "verified" in v and "unverified" not in v: return "Verified"
    return "Unverified"

def map_engagement(rec):
    blob=" ".join([(rec.get("engagement_type_hints") or ""),(rec.get("agreement_type_hints") or ""),(rec.get("relationship_summary") or ""),(rec.get("project_hints") or "")]).lower()
    out=[]
    if any(k in blob for k in ["interconnection","lgia","sgia","gia","study","queue","poi","substation","energization","ciac","large load","feasibility"]): out.append("Interconnection")
    if any(k in blob for k in ["pricing","tariff","rate schedule","commercial","term sheet","demand charge","economic development rate","retail"]): out.append("Pricing/Commercial")
    if any(k in blob for k in ["ppa","tolling","physical","fuel supply","gas supply","nomination"]): out.append("Energy Portfolio (Physical)")
    if any(k in blob for k in ["hedge","swap","isda","financial","ftr","crr"]): out.append("Energy Portfolio (Financial)")
    if any(k in blob for k in ["regulatory","docket","filing","permit","rate case","intervenor","puc","psc","ferc"]): out.append("Regulatory")
    if any(k in blob for k in ["procurement","transformer","switchgear","rfq","long-lead","equipment","sourcing"]): out.append("Procurement")
    if not out: out.append("Other")
    # dedupe preserve order
    seen=set(); res=[]
    for x in out:
        if x not in seen: seen.add(x); res.append(x)
    return ";".join(res)

AGREE_TOKENS=["LGIA","SGIA","ISA","GIA","ICA","TFA","MPESA","ESA","VPPA","PPA","Tolling","EEI Master","ISDA","CIAC Agreement","CIAC","Construction Agreement","Easement","LOI","MOU","NDA","Term Sheet","Service Agreement","Tariff/Rate Schedule","Tariff","Rate Schedule"]
def map_agreement(rec):
    blob=" ".join([(rec.get("agreement_type_hints") or ""),(rec.get("contract_status_hint") or ""),(rec.get("relationship_summary") or "")])
    found=[]
    bl=blob.lower()
    mapping=[("lgia","LGIA"),("sgia","SGIA"),(" isa","ISA"),("interconnection study","Service Agreement"),("llis","Service Agreement"),("gia","GIA"),("vppa","VPPA"),("ppa","PPA"),("tolling","Tolling"),("eei master","EEI Master"),("isda","ISDA"),("ciac","CIAC Agreement"),("construction agreement","Construction Agreement"),("easement","Easement"),("term sheet","Term Sheet"),("loi","LOI"),("mou","MOU"),("nda","NDA"),("service agreement","Service Agreement"),("tariff","Tariff/Rate Schedule"),("rate schedule","Tariff/Rate Schedule"),("purchase agreement","Service Agreement"),("lease colo","Service Agreement")]
    for k,v in mapping:
        if k in bl and v not in found: found.append(v)
    return ";".join(found)

def map_contract_status(rec):
    h=(rec.get("contract_status_hint") or "").lower()
    if not h: return ""
    if "execut" in h or "committed" in h or "signed" in h: return "Executed"
    if "negotiat" in h or "redline" in h or "draft" in h: return "In Negotiation"
    if "active" in h or "operational" in h: return "Active/Operational"
    if "prospect" in h or "exploratory" in h or "pending" in h: return "Prospect"
    if "expired" in h or "terminated" in h: return "Expired/Terminated"
    return "Unknown"

def site_from_hints(rec):
    """try to extract a known site code; else ''"""
    for f in ("site_code","site_code_hints","project_hints","notes"):
        v=(rec.get(f) or "").upper()
        if not v: continue
        for code in SITE_MAP:
            if re.search(r"\b"+re.escape(code)+r"\b", v):
                return code
    return ""

# ---------- load all ----------
all_recs=[]
counts={}
for name in SOURCES:
    try:
        recs=load_source(name)
    except Exception as e:
        print(f"!! {name} load error: {e}", file=sys.stderr); recs=[]
    n=0
    for r in recs:
        if not isinstance(r,dict): continue
        if "_site_map" in r: continue
        r["_src"]=name
        all_recs.append(r); n+=1
    counts[name]=n
print("Raw record counts by source:", counts, "total raw:", len(all_recs))

# ---------- build keys + group ----------
def slug(rec):
    fn=(rec.get("contact_first_name") or "").strip()
    ln=(rec.get("contact_last_name") or "").strip()
    nm=(rec.get("contact_name") or "").strip()
    base = (fn+" "+ln).strip() or nm
    if not base:
        base = (rec.get("org_name") or "unknown")+" desk"
    s=re.sub(r"[^a-z0-9]+","-",base.lower()).strip("-")
    return s or "unknown"

def email_of(rec):
    e=(rec.get("email") or "").strip().lower()
    if e and "@" in e and not e.startswith("@"): return e
    return ""

groups=defaultdict(list)
for r in all_recs:
    sc=site_from_hints(r)
    em=email_of(r)
    key = (em if em else slug(r)) + "|" + sc
    r["_site_code"]=sc; r["_email"]=em; r["_key"]=key
    groups[key].append(r)

# kaiser email roster for in_kaiser cross-check
kaiser_emails=set()
for r in all_recs:
    if r["_src"]=="Kaiser" and r["_email"]:
        kaiser_emails.add(r["_email"])

def pick(recs, field):
    # authoritative-first non-empty
    for r in sorted(recs, key=lambda x:PRIO.get(x["_src"],9)):
        v=r.get(field)
        if v not in (None,"",[]): return v
    return ""

def longest(recs, field):
    best=""
    for r in recs:
        v=r.get(field) or ""
        if len(str(v))>len(best): best=str(v)
    return best

def all_dates(recs, *fields):
    ds=[]
    for r in recs:
        for f in fields:
            v=r.get(f)
            if v and re.match(r"^\d{4}-\d{2}-\d{2}$",str(v)): ds.append(str(v))
    return ds

HEADER="record_id,contact_name,contact_first_name,contact_last_name,contact_title,department,seniority_level,decision_role,org_name,org_type,parent_company,org_ownership_model,stakeholder_class,value_chain_segment,commodity_focus,org_domain,org_stock_ticker,geographic_region,market_iso,nerc_region,balancing_authority,service_territory,state,country,regulatory_jurisdiction,timezone,email,email_secondary,office_phone,mobile_phone,preferred_contact_method,assistant_name,assistant_email,linkedin_url,office_location,first_contacted_date,last_contacted_date,last_inbound_date,last_meeting_date,last_contact_channel,contact_cadence,interaction_count_estimate,meeting_count_estimate,last_contact_summary,relationship_summary,sentiment,relationship_strength,engagement_score,relationship_status,responsiveness,introduced_by,relationship_owner,relationship_owner_detail,internal_fs_owner,internal_fs_backup,relationship_sensitivity,nda_status,mnpi_flag,do_not_contact,project_name,site_code,slack_channel,deal_priority,associated_site_mw,lifecycle_stage,engagement_type,agreement_type,contract_status,pricing_structure,rate_schedule,portfolio_position,equipment_or_service,docket_or_filing,current_blocker,risk_flags,next_milestone,next_milestone_date,queue_position,poi_substation,interconnection_voltage,power_commitment_status,study_status,target_energization_date,contact_source,source_artifacts,source_links,in_kaiser,verification_status,last_verified_date,confidence,data_quality_flags,possible_duplicate_of,next_action,tags,notes,schema_version,run_id,extracted_by,extracted_date,email_integration_used".split(",")
assert len(HEADER)==100, len(HEADER)

def cadence(recs):
    for r in sorted(recs,key=lambda x:PRIO.get(x["_src"],9)):
        c=(r.get("contact_cadence_hint") or r.get("contact_cadence") or "").strip()
        if c:
            cl=c.lower()
            for opt in ["Weekly","Biweekly","Monthly","Quarterly","Ad-hoc","Dormant"]:
                if opt.lower() in cl or (opt=="Biweekly" and "bi-weekly" in cl): return opt
    return ""

def sentiment(recs):
    for r in sorted(recs,key=lambda x:PRIO.get(x["_src"],9)):
        s=(r.get("sentiment") or "").lower()
        if "positive" in s: return "Positive"
        if "negative" in s: return "Negative"
        if "mixed" in s: return "Mixed"
        if "neutral" in s: return "Neutral"
    return ""

def strength(recs):
    for r in sorted(recs,key=lambda x:PRIO.get(x["_src"],9)):
        s=(r.get("relationship_strength") or "").lower()
        if "strong" in s: return "Strong"
        if "develop" in s or "warming" in s or "active" in s or "new" in s: return "Developing"
        if "cold" in s or "exploratory" in s or "early" in s: return "Cold"
    return ""

rows=[]
email_to_keys=defaultdict(list)
for key,recs in groups.items():
    merged={}
    fields_union=set()
    for r in recs: fields_union|=set(r.keys())
    for f in fields_union:
        merged[f]=pick(recs,f)
    # better long-text
    for f in ("relationship_summary","last_contact_summary","notes"):
        merged[f]=longest(recs,f) or merged.get(f,"")
    srcs=sorted({r["_src"] for r in recs})
    src_disp = srcs[0] if len(srcs)==1 else "Multiple"
    email=recs[0]["_email"]
    site=recs[0]["_site_code"]

    ot,sc,own,vc,cf=classify_org(merged)
    st=norm_state(merged)
    # site overrides geography
    proj=merged.get("project_name") or ""
    miso=""
    if site and site in SITE_MAP:
        sp,smiso,sst=SITE_MAP[site]
        if not proj: proj=sp
        miso=smiso
        if not st and sst and len(sst)==2: st=sst
    # market iso
    mg=(merged.get("market_iso_guess") or merged.get("market_iso") or "").upper().replace(" ","")
    if not miso:
        if mg in {x.upper().replace(" ","") for x in VALID_ISO}:
            for v in VALID_ISO:
                if v.upper().replace(" ","")==mg: miso=v;break
        elif st in ISO_BY_STATE: miso=ISO_BY_STATE[st]
        else: miso="Unknown"
    if miso not in VALID_ISO: miso="Unknown"
    region=REGION.get(st,"Unknown") if st else "Unknown"
    if st=="" and "alberta" in (merged.get("state_guess","")+merged.get("notes","")).lower(): region="Other"
    tz=TZ.get(st,"Unknown") if st else "Unknown"
    nerc=NERC_BY_ISO.get(miso,"Unknown")

    title=merged.get("contact_title") or ""
    # project_name from hints if still empty
    if not proj:
        proj=(merged.get("project_name") or "").strip() or (merged.get("project_hints") or "").strip()
    proj=proj.replace("\n"," ").strip()
    if len(proj)>120: proj=proj[:117]+"..."

    # in_kaiser
    if "Kaiser" in srcs: in_k="Yes"
    elif email and email in kaiser_emails: in_k="Yes"
    elif email: in_k="No"
    else: in_k="Unknown"

    conf=norm_conf(pick(recs,"confidence"))
    verif=norm_verif(pick(recs,"verification_status"))
    # name
    cn=merged.get("contact_name") or (((merged.get("contact_first_name") or "")+" "+(merged.get("contact_last_name") or "")).strip())
    fn=merged.get("contact_first_name") or (cn.split()[0] if cn and " " in cn else (cn if cn else ""))
    ln=merged.get("contact_last_name") or (cn.split()[-1] if cn and " " in cn else "")

    dqf=merged.get("data_quality_flags") or ""
    if not email and "missing_email" not in dqf:
        dqf=("; ".join([x for x in [dqf,"missing_email"] if x])).strip("; ")
    # dedupe dqf tokens
    if dqf:
        seen=set(); toks=[]
        for t in re.split(r"[;]+",dqf):
            t=t.strip()
            if t and t.lower() not in seen: seen.add(t.lower()); toks.append(t)
        dqf="; ".join(toks)
    # last contact channel
    chan_map={"Email":"Email","Slack":"Slack","Calendar":"Calendar/Meeting","Granola":"Calendar/Meeting","Drive":"Other","Notion":"Other","Kaiser":"Other"}
    lcc=chan_map.get(srcs[0],"Other")
    if len(srcs)>1:
        # prefer most "live" channel present
        for s in ["Email","Slack","Calendar","Granola"]:
            if s in srcs: lcc=chan_map[s];break

    fdates=all_dates(recs,"first_contacted_date","first_meeting_date")
    ldates=all_dates(recs,"last_contacted_date","last_meeting_date","last_inbound_date")
    mdates=all_dates(recs,"last_meeting_date")
    first_c=min(fdates+ldates) if (fdates or ldates) else ""
    last_c=max(ldates) if ldates else ""
    last_m=max(mdates) if mdates else ""
    last_in=pick(recs,"last_inbound_date") or ""

    def maxint(field):
        vals=[]
        for r in recs:
            v=r.get(field)
            try: vals.append(int(v))
            except: pass
        return max(vals) if vals else ""

    # sensitivity / mnpi
    deal_linked = bool(site or proj)
    public_org = ot.startswith("Regulator") or ot in ("ISO/RTO","Environmental/Permitting Agency","Economic Development Agency")
    if public_org: sens="Public"
    elif deal_linked: sens="Confidential"
    else: sens="Internal"
    is_public_co = ot in ("Electric IOU","Gas Utility/LDC","Transmission Owner/Operator (TO/TSP/TSO)") or any(k in (merged.get("org_name","").lower()) for k in ["aep","duke","dominion","ppl","pseg","nextera","southern","vistra","talen","brookfield","nrg"])
    if is_public_co and deal_linked: mnpi="Yes"
    elif public_org: mnpi="No"
    else: mnpi="Unknown"

    nda_h=(merged.get("nda_hint") or "")+" "+(merged.get("agreement_type_hints") or "")+" "+(merged.get("notes") or "")
    nl=nda_h.lower()
    if "nda complete" in nl or "nda signed" in nl or "nda done" in nl: nda="Signed"
    elif "nda" in nl and ("pending" in nl or "in progress" in nl or "then" in nl): nda="In Progress"
    elif "nda" in nl: nda="In Progress"
    else: nda="Unknown"

    rel_owner = "Fluidstack-Direct" if (merged.get("internal_fs_owner") or src_disp in ("Kaiser",)) else "Unknown"
    intro=merged.get("introduced_by") or ""
    if intro and rel_owner=="Unknown": rel_owner="Intermediated"

    row={
      "record_id": (email if email else slug(recs[0]))+"|"+site,
      "contact_name": cn,"contact_first_name":fn,"contact_last_name":ln,
      "contact_title":title,"department":merged.get("department") or "",
      "seniority_level":seniority(title),"decision_role":decision_role(title),
      "org_name":merged.get("org_name") or "","org_type":ot,
      "parent_company":merged.get("parent_company") or "","org_ownership_model":own,
      "stakeholder_class":sc,"value_chain_segment":vc,"commodity_focus":cf,
      "org_domain":(merged.get("org_domain") or "").lower(),"org_stock_ticker":merged.get("org_stock_ticker") or "",
      "geographic_region":region,"market_iso":miso,"nerc_region":nerc,
      "balancing_authority":merged.get("balancing_authority") or "","service_territory":merged.get("service_territory") or "",
      "state":st,"country":"US" if st else (merged.get("country") or ""),
      "regulatory_jurisdiction":merged.get("regulatory_jurisdiction") or "","timezone":tz,
      "email":email,"email_secondary":(merged.get("email_secondary") or "").lower(),
      "office_phone":clean_phone(merged.get("office_phone")),"mobile_phone":clean_phone(merged.get("mobile_phone")),
      "preferred_contact_method": "Email" if email else "Unknown",
      "assistant_name":merged.get("assistant_name") or "","assistant_email":(merged.get("assistant_email") or "").lower(),
      "linkedin_url":merged.get("linkedin_url") or "","office_location":merged.get("office_location") or "",
      "first_contacted_date":first_c,"last_contacted_date":last_c,"last_inbound_date":last_in,"last_meeting_date":last_m,
      "last_contact_channel":lcc,"contact_cadence":cadence(recs),
      "interaction_count_estimate":maxint("interaction_count_estimate"),"meeting_count_estimate":maxint("meeting_count_estimate"),
      "last_contact_summary":(merged.get("last_contact_summary") or "").replace("\n"," ").strip(),
      "relationship_summary":(merged.get("relationship_summary") or "").replace("\n"," ").strip(),
      "sentiment":sentiment(recs),"relationship_strength":strength(recs),
      "engagement_score":"","relationship_status":"","responsiveness":"",
      "introduced_by":intro,"relationship_owner":rel_owner,"relationship_owner_detail":merged.get("relationship_owner_detail") or "",
      "internal_fs_owner":merged.get("internal_fs_owner") or "","internal_fs_backup":"",
      "relationship_sensitivity":sens,"nda_status":nda,"mnpi_flag":mnpi,"do_not_contact":"No",
      "project_name":proj,"site_code":site,"slack_channel":merged.get("slack_channel") or "",
      "deal_priority":"Unknown","associated_site_mw":merged.get("associated_site_mw") or "",
      "lifecycle_stage": "Executed/IA Signed" if (merged.get("lifecycle_stage_hint","").lower().startswith("commit")) else ("Unknown" if deal_linked else "N/A"),
      "engagement_type":map_engagement(merged),"agreement_type":map_agreement(merged),
      "contract_status":map_contract_status(merged),"pricing_structure":"",
      "rate_schedule":merged.get("rate_schedule") or "","portfolio_position":"",
      "equipment_or_service":merged.get("equipment_or_service") or (merged.get("equipment_or_service") or ""),
      "docket_or_filing":merged.get("docket_or_filing") or "",
      "current_blocker":(merged.get("current_blocker") or "").replace("\n"," ").strip(),
      "risk_flags":merged.get("risk_flags") or "",
      "next_milestone":(merged.get("next_milestone") or "").replace("\n"," ").strip(),
      "next_milestone_date":merged.get("next_milestone_date") or "",
      "queue_position":merged.get("queue_position") or "","poi_substation":merged.get("poi_substation") or "",
      "interconnection_voltage":merged.get("interconnection_voltage") or "",
      "power_commitment_status": "" ,"study_status":"","target_energization_date":merged.get("target_energization_date") or "",
      "contact_source":src_disp,
      "source_artifacts":"; ".join(sorted({(r.get("source_artifacts") or "").replace("\n"," ").strip() for r in recs if r.get("source_artifacts")}))[:500],
      "source_links":"; ".join(sorted({(r.get("source_links") or "").strip() for r in recs if r.get("source_links")}))[:600],
      "in_kaiser":in_k,"verification_status":verif,"last_verified_date":merged.get("last_verified_date") or "",
      "confidence":conf,"data_quality_flags":dqf,"possible_duplicate_of":"",
      "next_action":"","tags":"",
      "notes":(merged.get("notes") or "").replace("\n"," ").strip()+ (" | engagement_type/agreement derived from hints." if False else ""),
      "schema_version":"boil-the-ocean-v3","run_id":RUN_ID,"extracted_by":EXTRACTED_BY,"extracted_date":EXTRACTED_DATE,
      "email_integration_used":"Gmail",
    }
    # equipment_or_service for vendors/consultants
    if ot in ("Equipment Supplier","Engineering/EPC","Energy Consultant/Advisor","Power Systems Modeling Firm","Outside Counsel"):
        es=merged.get("equipment_or_service") or merged.get("engagement_type_hints") or ""
        row["equipment_or_service"]=str(es).replace("\n"," ").strip()
    # power commitment / study status from hints
    pch=(merged.get("power_commitment_status_hint") or "").lower()
    if "firm" in pch: row["power_commitment_status"]="Firm"
    elif "conditional" in pch: row["power_commitment_status"]="Conditional"
    elif "indicative" in pch: row["power_commitment_status"]="Indicative"
    ssh=(merged.get("study_status_hint") or "").lower()
    if "facilities" in ssh: row["study_status"]="Facilities Study"
    elif "system impact" in ssh or "sis" in ssh: row["study_status"]="System Impact Study"
    elif "feasibility" in ssh: row["study_status"]="Feasibility"
    elif "complete" in ssh: row["study_status"]="Complete"
    elif "study" in ssh: row["study_status"]="System Impact Study"

    rows.append(row)
    if email: email_to_keys[email].append(row["record_id"])

# possible duplicates: same email, different record_id
for email,ids in email_to_keys.items():
    if len(set(ids))>1:
        uniq=sorted(set(ids))
        for r in rows:
            if r["email"]==email and r["record_id"]==uniq[0]:
                continue
            if r["email"]==email:
                r["possible_duplicate_of"]=uniq[0]

# sort: confidence then source
order={"High":0,"Medium":1,"Low":2}
rows.sort(key=lambda r:(order.get(r["confidence"],3), r["org_name"].lower(), r["contact_last_name"].lower()))

# write
with open(OUT,"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f,quoting=csv.QUOTE_MINIMAL)
    w.writerow(HEADER)
    for r in rows:
        w.writerow([r.get(h,"") for h in HEADER])

print("WROTE",OUT,"rows:",len(rows))

# stats
from collections import Counter
def cnt(field): return Counter(r[field] for r in rows)
print("\nBy stakeholder_class:", dict(cnt("stakeholder_class")))
print("By market_iso:", dict(cnt("market_iso")))
print("By lifecycle_stage:", dict(cnt("lifecycle_stage")))
print("By confidence:", dict(cnt("confidence")))
print("By contact_source:", dict(cnt("contact_source")))
print("net-new (in_kaiser=No):", sum(1 for r in rows if r["in_kaiser"]=="No"))
print("in_kaiser=Yes:", sum(1 for r in rows if r["in_kaiser"]=="Yes"))
print("with email:", sum(1 for r in rows if r["email"]))
print("Needs Review:", sum(1 for r in rows if r["verification_status"]=="Needs Review"))
print("possible dups flagged:", sum(1 for r in rows if r["possible_duplicate_of"]))
