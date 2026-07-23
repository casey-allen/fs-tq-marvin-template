import openpyxl, csv, io
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Alignment

SRC='.tmp/beacon-qlog/Diligence-Tracker.xlsx'   # pristine original template
wb=openpyxl.load_workbook(SRC)

CATS=[
 "Transaction & PSA",
 "Title, Easements & Survey",
 "Building Quality & Warranties",
 "Power - Interconnection & Transfer",
 "Power - Substation Build & Schedule",
 "Power - Commercial, Collateral & O&M",
 "Regulatory & Moratorium",
 "Permitting & Construction",
 "Environmental & Aquifer",
 "Incentives / IDA / Tax",
]
ov=wb['Overview']
for i,c in enumerate(CATS):
    ov[f'B{37+i}']=c

DATE="2026-06-12"
# (Category, Question, VDR, Priority, Status, Seller Response so far, How-this-differs-from-Atlas / Follow-up)
rows=[
 ("Transaction & PSA",
  "We have the auction mechanics already - what we need now is the deal paper: the expected form of PSA and risk allocation. Deposit/escrow size, as-is vs. survival of reps & warranties, indemnity caps/baskets, and is R&W insurance available on this asset?",
  "Not in VDR - request PSA form","Highest","Open",
  "",
  "Distinct from Atlas (who asked process/timeline): this is the acquirer's PSA-terms ask, not the auction calendar."),

 ("Transaction & PSA",
  "Walk us through closing-cost leakage: NY State and Suffolk County transfer-tax treatment, any prepayment/defeasance or mortgage-recording-tax exposure on the Bank OZK payoff, broker-fee responsibility, and whether unwinding the IDA leaseback at closing creates added transfer or recording tax.",
  "3.1","High","Open",
  "",
  "Net-new vs Atlas - Atlas asked who owns the entity; we need the transaction-cost stack a buyer absorbs."),

 ("Title, Easements & Survey",
  "Please overlay the recorded easements on the site plan and confirm the 3.5-ac transformer yard, the 1-ac PSEG switching station, and the generator yards all sit clear of the LILCO/LIPA utility easements, the LIE access-restriction takings, and the Central Pine Barrens conservation easement - any encroachment or relocation needed?",
  "3.1, 3.2","High","Open",
  "",
  "Net-new - Atlas confirmed title is clean; nobody has checked whether the buildable footprint physically clears the recorded easements."),

 ("Title, Easements & Survey",
  "Confirm the curb-cut and ingress/egress rights off the LIE North Service Road given the State access-restriction easements, and whether a DOT-coordinated oversize/heavy-haul route for the 66 MVA transformers has been identified.",
  "3.2","High","Open",
  "",
  "Net-new - heavy-haul/access wasn't in Atlas's set and is a buyer construction-logistics item."),

 ("Building Quality & Warranties",
  "These shells are newly built, so a buyer inherits them - please list the assignable warranties (roof, Fabcon precast, McCombs structural steel, slab, base-building MEP) with remaining terms, and confirm each transfers to a buyer.",
  "4.1 - request warranty package","High","Open",
  "",
  "Net-new - Atlas treated the buildings as a given; we're buying them and need the warranty chain."),

 ("Building Quality & Warranties",
  "Share the FFFL inspection findings and confirm there's no open punch list, latent-defect claim, or unresolved final-CO condition - and no outstanding contractor liens beyond the Sunbelt item.",
  "4.1","Medium","Open",
  "",
  "Net-new - construction-quality/punch diligence on the as-built campus; ties to the title's mechanics-lien exception."),

 ("Power - Interconnection & Transfer",
  "Atlas confirmed the FSA is binding on assigns - what we need is the mechanical assignment package: exactly what PSEG-LI/NYISO require to move Q#1721 and the FSA to a buyer (consent, creditworthiness test, fresh deposits), and whether the $90K FSA deposit (and any queue deposit) is already paid and credited to the buyer.",
  "2.2, 2.3","Highest","Partial",
  "FSA is binding on successors and assigns; $90K FSA deposit; biweekly PSEG-LI meetings, on schedule.",
  "Differs from Atlas's 'does it transfer?' - we need the assignment checklist and whether paid deposits convey to us."),

 ("Power - Substation Build & Schedule",
  "Rather than re-ask the timeline, please give us the schedule build-up: the LIPA-approved design basis and an integrated schedule showing what concretely separates the ~12-month buyer self-build from LIPA's 39-month estimate - design-approval gates, tie-in/outage windows, and PSEG construction slots.",
  "2.2, 2.3, 4.3","Highest","Partial",
  "LIPA non-binding 39 months from IA; buyer/3rd-party self-build ~12 months with LIPA-approved design; design finalizes after facility study ~Aug 2026.",
  "Deeper than Atlas (who logged the two numbers) - we need the activity-level schedule that reconciles 12 vs 39."),

 ("Power - Substation Build & Schedule",
  "Can transformer and switchgear orders be placed now against the current design - are there existing factory slots, quotes, or reservation deposits - and would those POs assign to a buyer at closing?",
  "4.3","High","Open",
  "",
  "Differs from Atlas's 'procurement status' - we're asking about pre-ordering against lead time and PO assignability."),

 ("Power - Commercial, Collateral & O&M",
  "Atlas has the Rate 285 / $0.15 figure - what we need is the credit support: the form (LC, guarantee, prepayment), magnitude, and timing of the collateral LIPA will require under the ESA, and any read the seller has on the dollar amount.",
  "2.3 - request ESA draft","Highest","Partial",
  "177 MW under Rate 285; ~$0.15/kWh subject to the executed ESA (expected Q4 2026).",
  "Distinct from Atlas's rate question - collateral sizing drives the buyer's capital plan."),

 ("Power - Commercial, Collateral & O&M",
  "Since PSEG-LI will own the substation we fund and build, what are the ongoing O&M, station-service, metering, and standby/demand-ratchet charges, and the cost-recovery/true-up mechanism - i.e., what do we pay PSEG to operate the asset we paid for?",
  "Not in VDR - request","High","Open",
  "",
  "Net-new - Atlas never addressed post-energization O&M economics of the PSEG-owned substation."),

 ("Regulatory & Moratorium",
  "We're aligning to the customer's S10642 legal workstream rather than re-running it - so just confirm the seller will paper a regulatory CP / outside-date relief / price adjustment tied to enactment, and will share its own 'commencing construction' grandfathering opinion when ready.",
  "1.1","High","Partial",
  "Seller expects a Hochul veto; she has until 12/31/26; seller is open to a regulatory closing condition.",
  "Consolidated to the commercial ask only - the detailed permit-inventory/grandfathering analysis lives in Atlas's set, so we don't duplicate it."),

 ("Permitting & Construction",
  "Are the Clune GC relationship and the Syska / Gensler / Commonwealth design contracts assignable to a buyer, and can you share the Minor Site Plan submission set plus the Town's review timeline so we can sequence groundbreaking?",
  "3.3, 4.3 - request submission set","High","Open",
  "",
  "Net-new vs Atlas's zoning/by-right question - this is contractor continuity and the actual submission package for our build schedule."),

 ("Environmental & Aquifer",
  "Beyond identifying the zone, what does the Central Pine Barrens Commission require to approve substation and generator-yard ground disturbance or any added clearing, is there a mitigation/credit obligation, and please provide the recorded conservation easement and its amendment.",
  "3.1 - request CPB instrument","High","Partial",
  "Sewage-density limit (added floor area needs credits); seller 'not aware' of diesel-storage or stormwater limits.",
  "Deeper than Atlas's 'identify the designation' - we need the CPB approval process and instrument for our specific build."),

 ("Environmental & Aquifer",
  "Is environmental insurance (a PLL policy) contemplated for the transaction, and does the closed Liere Farm spill on the adjacent up-gradient parcel carry any monitoring obligation that runs with this site?",
  "5.1","Medium","Open",
  "",
  "Net-new - Atlas asked for the report inventory; we flag the specific adjacent spill and the insurance structure."),

 ("Incentives / IDA / Tax",
  "Beyond consent/recapture, what's the seller's read on a renegotiated data-center PILOT versus the recapture cost, the exposure from the 170 FT / 21 PT job commitment a data center won't meet, and any transfer- or mortgage-recording-tax leakage from unwinding the leaseback?",
  "Not in VDR - request IDA docs","High","Partial",
  "IDA defines the project as warehouse; consent required for change of use; sale without consent can trigger recapture; in discussions with TOBIDA.",
  "Atlas requested the IDA documents; we need the go-forward PILOT economics and tax leakage a buyer underwrites."),
]

bw=wb['Buyer']
start=5; wrap=Alignment(wrap_text=True, vertical='top')
for i,(cat,q,vdr,prio,status,resp,follow) in enumerate(rows):
    r=start+i
    for col,val in zip('CDEFGHIJK',[DATE,cat,q,vdr,prio,status,DATE,resp,follow]):
        bw[f'{col}{r}']=val; bw[f'{col}{r}'].alignment=wrap

bw.data_validations.dataValidation=[]
dv_cat=DataValidation(type="list", formula1='Overview!$B$37:$B$46', allow_blank=True)
dv_pri=DataValidation(type="list", formula1='"Highest,High,Medium,Low"', allow_blank=True)
dv_sta=DataValidation(type="list", formula1='"Open,Partial,Closed,N/A"', allow_blank=True)
for dv,rng in [(dv_cat,'D5:D104'),(dv_pri,'G5:G104'),(dv_sta,'H5:H104')]:
    bw.add_data_validation(dv); dv.add(rng)

out='.tmp/beacon-qlog/Project-Beacon-Diligence-Tracker-BUYER-filled.xlsx'
wb.save(out)

# CSV for the native Sheet
hdr=['#','Date Requested','Category','Request / Question','VDR Reference','Priority','Status','Last Update',"Seller's Response","Buyer's Follow-Up / How this differs from Atlas"]
o=io.StringIO(); w=csv.writer(o,quoting=csv.QUOTE_ALL); w.writerow(hdr)
for i,(cat,q,vdr,prio,status,resp,follow) in enumerate(rows):
    w.writerow([i+1,DATE,cat,q,vdr,prio,status,DATE,resp,follow])
open('.tmp/beacon-qlog/buyer_log_v2.csv','w').write(o.getvalue())
print('WROTE xlsx + csv with', len(rows), 'developer-angled questions')
