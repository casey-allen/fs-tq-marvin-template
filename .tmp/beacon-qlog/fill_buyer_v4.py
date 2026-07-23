import openpyxl, io
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Alignment

SRC='.tmp/beacon-qlog/Diligence-Tracker.xlsx'
wb=openpyxl.load_workbook(SRC)

CATS=[
 "Power - Interconnection & Studies","Power - Substation & Equipment","Power - Commercial / ESA",
 "Title, Liens & Encumbrances","IDA / PILOT / Incentives","Land, Easements & Access",
 "Environmental & Aquifer","Geotech & Conversion","Zoning, Permitting & Air","Transaction & Process",
]
ov=wb['Overview']
for i,c in enumerate(CATS): ov[f'B{37+i}']=c

DATE="2026-06-12"
# (Category, Question[human], VDR, Priority, Basis)
rows=[
 ("Power - Interconnection & Studies",
  "Could you give us an update on where the Interconnection Agreement stands, and share the latest draft if there is one? Right now the 177 MW reads as an approved pathway rather than firm contracted capacity, so we'd like to see how close the IA really is.",
  "2.2, 2.3","Highest","CIM projects IA execution Q3 2026; no executed IA in the room."),
 ("Power - Interconnection & Studies",
  "We're trying to square the SIS with the CIM on timing. The SIS points to roughly 39 months of upgrade work after the IA is signed, but the marketing shows first power in 2027. What's the realistic energization date, and what's actually driving those 39 months - the utility system upgrades or building the substation?",
  "2.2","Highest","Direct conflict in the docs: SIS 39-mo-from-IA vs CIM 2027 ramp. Biggest open item from the review."),
 ("Power - Interconnection & Studies",
  "Small one: the CIM says 177 MW but the SIS studied 176.6 MW. Which number ends up in the IA and ESA, and would bumping it back up trigger a restudy at NYISO?",
  "2.2, 1.1","High","Load figure differs between CIM and SIS Rev 6."),
 ("Power - Interconnection & Studies",
  "We see the Facilities Study Agreement was signed in February and the $90K deposit is in - when do you expect the Facilities Study itself back, and can you share it when it lands? That's the piece that firms up the cost and schedule behind the SIS estimate.",
  "2.3","High","FSA present; FS output absent. FSA references a ~150/180-day study and a high-level estimate."),
 ("Power - Interconnection & Studies",
  "Can you confirm the two 138 kV feeds give us genuine N-1 redundancy? And which point of interconnection is the basis now - the SIS shows it moving from Line 138-873 to 138-872 partway through.",
  "2.2","Medium","CIM claims 2N/redundant feeds (N-1 unconfirmed); SIS notes a POI change mid-study."),

 ("Power - Substation & Equipment",
  "Help us understand who builds and owns what on the substation. The materials suggest PSEG-LI owns it but we fund and build it - can you spell out the split, when the design gets to IFC, and whether that waits on the Facilities Study in August?",
  "2.1, 4.3","High","PSEG-owns / buyer-builds split is ambiguous; design appears conceptual (ROMs only)."),
 ("Power - Substation & Equipment",
  "There are two substation estimates in the room - Clune around $69M and Hunter Roberts around $84M. Which one should we be underwriting to, and what's behind the ~$15M difference?",
  "4.3","High","Two divergent ROMs reviewed (Clune 3/2/26; Hunter Roberts 3/5/26)."),
 ("Power - Substation & Equipment",
  "Where are we on the long-lead gear - the four 66 MVA transformers, HV breakers, and switchgear? Those run about a two-year lead and drive first power, so it'd help to know if anything's been ordered or if there are quotes or factory slots in hand.",
  "4.3","High","Hunter Roberts shows ~40-52 wk furnish + ~48-52 wk install; nothing ordered per the room."),

 ("Power - Commercial / ESA",
  "Could you share the draft ESA, or at least the expected rate, term, escalation, and any security? The ~$0.15/kWh in the CIM is flagged as indicative and subject to the executed ESA, so we'd like to see where it actually lands.",
  "1.1","Highest","No ESA in the room; CIM flags 177 MW as subject to the executed ESA (projected Q4 2026)."),
 ("Power - Commercial / ESA",
  "The SIS puts the utility upgrades at $25.34M give or take 50%. Do you have a tighter number yet, how is that cost split between LIPA and us, and what collateral will the ESA require - form, size, and timing?",
  "2.2","High","Upgrade cost is a wide non-binding band; collateral undisclosed."),

 ("Title, Liens & Encumbrances",
  "Just confirming the cleanup at closing: the Bank OZK loan (~$52.6M) gets paid off and discharged, and the Sunbelt Rentals mechanics lien (~$30.5K) gets released, so we take clean title?",
  "3.1","High","Schedule B (Title No. 917082): OZK building loan + open Sunbelt mechanics lien."),
 ("Title, Liens & Encumbrances",
  "Could someone walk us through the Schedule B exceptions on title (No. 917082)? We're especially interested in the LIPA/LILCO utility easements and the Long Island Expressway access takings, and whether any of them eat into the developable area or the substation site.",
  "3.1, 3.2","High","Numerous recorded LILCO/LIPA and Long Island Expressway easements in Schedule B."),

 ("IDA / PILOT / Incentives",
  "The title shows the property sits in a Town of Brookhaven IDA lease/leaseback, but we don't see the IDA documents in the room - could you add the company lease, the lease & project agreement, and the PILOT schedule? And what does it take to get IDA consent for a change of use and a sale: any recapture risk, and can the PILOT carry over or be renegotiated for a data center?",
  "Not in VDR - request","High","IDA appears only as a Schedule B exception; VDR has no IDA folder."),

 ("Land, Easements & Access",
  "Can you provide the recorded Central Pine Barrens conservation easement and its 2023 amendment? We want to understand how much of the site it takes off the table and what the Pine Barrens Commission needs to approve before we disturb ground for the substation and generator yards.",
  "3.1 - request instrument","High","Conservation easement in Schedule B; net buildable acreage never quantified in the CIM."),
 ("Land, Easements & Access",
  "A couple of access questions: are the curb cuts and ingress/egress off the LIE service road locked in given the State access restrictions on the parcel, and has anyone worked out an oversize/heavy-haul route with NYSDOT for getting the transformers in?",
  "3.2","Medium","LIE access-restriction takings in Schedule B; transformers are oversize loads."),

 ("Environmental & Aquifer",
  "The Phase I is from 2022 and was done before the buildings went up, and the CIM mentions no wetlands delineation was ever completed. Could you refresh the Phase I for the site as it stands today and provide the wetlands delineation and the threatened & endangered species work?",
  "5.1 - request wetlands/species","High","Phase I is stale/pre-construction; CIM says wetlands delineation not done; species 'clearance' asserted with no standalone report."),
 ("Environmental & Aquifer",
  "The teaser calls this a hydrogeologic sensitive zone - can you pin down the exact designation (Central Pine Barrens, Special Groundwater Protection Area, Suffolk Article 6) and any limits on storing diesel or chemicals and on stormwater recharge? That matters for a large backup-generator fleet sitting over the aquifer.",
  "1.1, 3.1","Medium","CIM flags a 'hydrogeologic sensitive zone'; designation and constraints unconfirmed."),

 ("Geotech & Conversion",
  "The Tectonic geotech gives 2 tons/sf bearing, but it was done for warehouses. Has anyone checked it against data-center loads - the transformer, UPS, and generator pads, plus the liquid-cooling slab loads on the 800 PSF floor?",
  "5.2","High","Geotech reviewed: Class D, no liquefaction, 2 tsf - sized for warehouses, not DC equipment."),
 ("Geotech & Conversion",
  "Beyond the substation, what's your estimate for the remaining capex to reach a true powered shell - MEP upgrades, fit-out interfaces, and so on? We want to pressure-test the low-incremental-capex story against the basis of design.",
  "2.1","High","CIM markets 'low incremental capex' but only the substation is costed."),

 ("Zoning, Permitting & Air",
  "We understand data center reads as a permitted R&D use, but it doesn't look like the change of use has actually been filed yet. Could you share the full list of remaining approvals (Town change of use, Pine Barrens, County Health), where the Minor Site Plan stands, and whether SEQRA gets triggered?",
  "3.3","High","Zoning memo (Certilman Balin) confirms the use but the DC change-of-use isn't yet filed."),
 ("Zoning, Permitting & Air",
  "What's the air-permitting picture for the ~78 backup generators, given this is a severe ozone nonattainment area? And what backup architecture does the basis of design actually assume - diesel, fuel cells, or batteries?",
  "2.1","High","CIM implies ~78 gensets (29/25/24); NYC-metro ozone nonattainment; air pathway unscoped."),

 ("Transaction & Process",
  "Last one - could you confirm the process basics? The bid deadline, the diligence window, the target signing and closing, and any guidance on price and the structure you're looking for.",
  "1.1","High","Broad TD Securities sale; pre-LOI; no price or exclusivity disclosed."),
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

# single-column paste block: just the questions, in order
open('.tmp/beacon-qlog/questions_only.txt','w').write("\n".join(q for (_,q,_,_,_) in rows)+"\n")
print('done -', len(rows), 'questions')
