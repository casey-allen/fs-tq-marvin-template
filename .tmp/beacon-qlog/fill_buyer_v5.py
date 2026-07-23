import openpyxl, csv, io
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Alignment

SRC='.tmp/beacon-qlog/Diligence-Tracker.xlsx'
wb=openpyxl.load_workbook(SRC)

CATS=[
 "Regulatory & Moratorium","Power - Interconnection & Studies","Power - Substation & Equipment",
 "Power - Commercial / ESA","Title, Liens & Encumbrances","IDA / PILOT / Incentives",
 "Land, Easements & Access","Environmental & Aquifer","Geotech & Conversion","Zoning, Permitting & Air",
]
ov=wb['Overview']
for i,c in enumerate(CATS): ov[f'B{37+i}']=c

DATE="2026-06-12"
# (Category, Question, VDR, Priority, Basis) -- questions 2-19 are Casey's curated wording verbatim
rows=[
 ("Regulatory & Moratorium",
  "Where does S10642 stand right now, and how does the project plan to navigate it? We'd want your read on the grandfathering case - whether the completed construction counts as \"commencing construction\" and which existing permits can be modified rather than newly issued - plus whether you'd support a regulatory closing condition or outside-date if the bill is signed.",
  "1.1","Highest","S10642 passed both houses 6/4-6/5/26, awaiting Hochul; at 177 MW Beacon is a covered 'large data center.'"),
 ("Power - Interconnection & Studies",
  "Where does the Interconnection Agreement stand, and can you share the current draft or redline?",
  "2.2, 2.3","Highest","CIM projects IA execution Q3 2026; no executed IA in the room."),
 ("Power - Interconnection & Studies",
  "The SIS estimates roughly 39 months from IA execution for the system upgrades, but the CIM markets first power in 2027. What's the realistic energization date, and what specifically drives the 39 months - the SUF/CTOAF/SASUF upgrades or the substation build itself?",
  "2.2","Highest","Direct conflict in the docs: SIS 39-mo-from-IA vs CIM 2027 ramp. Biggest open item from the review."),
 ("Power - Interconnection & Studies",
  "The Facilities Study Agreement was executed in Feb 2026 with the $90K deposit, but the Facilities Study itself isn't in the room. When does it complete, and can you share the cost and schedule output? That's what binds the SIS's preliminary estimate.",
  "2.3","High","FSA present; FS output absent. FSA references a ~150/180-day study and a high-level estimate."),
 ("Power - Interconnection & Studies",
  "Confirm the two incoming 138 kV feeds deliver true N-1/firm service, and clarify the point of interconnection - the SIS shows an original POI on Line 138-873 and an updated POI on Line 138-872. Which is the basis?",
  "2.2","Medium","CIM claims 2N/redundant feeds (N-1 unconfirmed); SIS notes a POI change mid-study."),
 ("Power - Substation & Equipment",
  "Please clarify the substation build and ownership boundary - the materials indicate PSEG-LI owns the switching station/substation while the buyer funds and builds it. Who constructs what, when does design reach IFC, and does that depend on the Facilities Study (~Aug 2026)?",
  "2.1, 4.3","High","PSEG-owns / buyer-builds split is ambiguous; design appears conceptual (ROMs only)."),
 ("Power - Substation & Equipment",
  "The room has two substation ROMs - Clune (~$69.4M) and Hunter Roberts (~$84.0M). Which is the basis of design, and what accounts for the ~$15M gap?",
  "4.3","High","Two divergent ROMs reviewed (Clune 3/2/26; Hunter Roberts 3/5/26)."),
 ("Power - Substation & Equipment",
  "What's the procurement status, lead time, and any quotes or factory slots for the 4 x 66 MVA transformers, HV breakers, and switchgear? At ~2-year lead these gate first power - has anything been ordered or reserved?",
  "4.3","High","Hunter Roberts shows ~40-52 wk furnish + ~48-52 wk install; nothing ordered per the room."),
 ("Power - Commercial / ESA",
  "Can you provide the draft Electric Service Agreement and confirm the rate, term, escalation, and credit/security? The CIM's ~$0.15/kWh is indicative and explicitly 'subject to the executed ESA.'",
  "1.1","Highest","No ESA in the room; CIM flags 177 MW as subject to the executed ESA (projected Q4 2026)."),
 ("Title, Liens & Encumbrances",
  "Confirm the payoff/discharge of the Bank OZK building loan (~$52.62M) and release of the Sunbelt Rentals mechanics lien (~$30,539) so clean title is delivered at closing.",
  "3.1","High","Schedule B (Title No. 917082): OZK building loan + open Sunbelt mechanics lien."),
 ("Title, Liens & Encumbrances",
  "Please walk the Schedule B exceptions on Title No. 917082 - in particular the multiple LILCO/LIPA utility easements and the LIE access-restriction takings - and flag which burden the developable area or the planned substation site.",
  "3.1, 3.2","High","Numerous recorded LILCO/LIPA and Long Island Expressway easements in Schedule B."),
 ("IDA / PILOT / Incentives",
  "The title shows a Town of Brookhaven IDA lease/leaseback (recorded 3/1/2023), but the IDA documents aren't in the room. Please add the Company Lease, Lease & Project Agreement, and PILOT schedule, and explain the consent path for change of use/control, recapture exposure, and whether the PILOT can transfer or be renegotiated for data-center use.",
  "Not in VDR - request","High","IDA appears only as a Schedule B exception; VDR has no IDA folder."),
 ("Land, Easements & Access",
  "Provide the recorded Central Pine Barrens conservation easement (12/6/2022) and its 4/19/2023 amendment, the resulting protected/non-buildable area, and what the Central Pine Barrens Commission requires to approve ground disturbance for the substation and generator yards.",
  "3.1 - request instrument","High","Conservation easement in Schedule B; net buildable acreage never quantified in the CIM."),
 ("Land, Easements & Access",
  "Confirm curb-cut and ingress/egress rights off the LIE North Service Road given the State access-restriction easements, and whether an oversize/heavy-haul route for the transformers has been coordinated with NYSDOT.",
  "3.2","Medium","LIE access-restriction takings in Schedule B; transformers are oversize loads."),
 ("Environmental & Aquifer",
  "The Phase I (VERTEX, 7/29/2022) predates construction and is ~4 years old, and the CIM states no wetlands delineation was completed. Please refresh the Phase I for the as-built campus and provide the wetlands delineation and threatened & endangered species report.",
  "5.1 - request wetlands/species","High","Phase I is stale/pre-construction; CIM says wetlands delineation not done; species 'clearance' asserted with no standalone report."),
 ("Environmental & Aquifer",
  "Identify the exact groundwater designation (Central Pine Barrens CGA / Special Groundwater Protection Area / Suffolk County Article 6) and any limits on diesel/chemical storage and stormwater recharge over the sole-source aquifer - relevant to a large backup-generator fleet.",
  "1.1, 3.1","Medium","CIM flags a 'hydrogeologic sensitive zone'; designation and constraints unconfirmed."),
 ("Geotech & Conversion",
  "The Tectonic geotech (12/6/2021) gives 2 tsf net allowable bearing but was designed for warehouse loads. Has it been validated for data-center equipment - transformer/UPS/generator pads and liquid-cooling slab loads - against the 7-inch / 800 PSF slab?",
  "5.2","High","Geotech reviewed: Class D, no liquefaction, 2 tsf - sized for warehouses, not DC equipment."),
 ("Zoning, Permitting & Air",
  "Data center is a permitted R&D use, but the change-of-use as a data center hasn't been filed. Please share the remaining-approvals matrix (Town change-of-use, CPBJPPC, SCDHS), the Minor Site Plan status, and whether SEQRA is triggered.",
  "3.3","High","Zoning memo (Certilman Balin) confirms the use but the DC change-of-use isn't yet filed."),
]

bw=wb['Buyer']; start=5; wrap=Alignment(wrap_text=True, vertical='top')
for i,(cat,q,vdr,prio,basis) in enumerate(rows):
    r=start+i
    for col,val in zip('CDEFGHIJK',[DATE,cat,q,vdr,prio,"Open",DATE,"",basis]):
        bw[f'{col}{r}']=val; bw[f'{col}{r}'].alignment=wrap
bw['K4']="Basis (from our VDR review)"
bw.data_validations.dataValidation=[]
for f1,rng in [('Overview!$B$37:$B$46','D5:D104'),('"Highest,High,Medium,Low"','G5:G104'),('"Open,Partial,Closed,N/A"','H5:H104')]:
    dv=DataValidation(type="list",formula1=f1,allow_blank=True); bw.add_data_validation(dv); dv.add(rng)
wb.save('.tmp/beacon-qlog/Project-Beacon-Diligence-Tracker-BUYER-filled.xlsx')

hdr=['#','Date Requested','Category','Request / Question','VDR Reference','Priority','Status','Last Update',"Seller's Response","Basis (from our VDR review)"]
o=io.StringIO(); w=csv.writer(o,quoting=csv.QUOTE_ALL); w.writerow(hdr)
for i,(cat,q,vdr,prio,basis) in enumerate(rows):
    w.writerow([i+1,DATE,cat,q,vdr,prio,"Open",DATE,"",basis])
open('.tmp/beacon-qlog/buyer_log_v5.csv','w').write(o.getvalue())
print('done -', len(rows), 'questions')
