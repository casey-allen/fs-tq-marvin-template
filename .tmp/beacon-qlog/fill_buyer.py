import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Alignment

PATH='.tmp/beacon-qlog/Diligence-Tracker.xlsx'
wb=openpyxl.load_workbook(PATH)

CATS=[
 "Transaction & Process",
 "Title, Seller & IDA",
 "Power - Interconnection",
 "Power - Substation & Schedule",
 "Power - Commercial / ESA",
 "Regulatory - NY Moratorium",
 "Zoning & Permitting",
 "Environmental & Aquifer",
 "Design & Conversion",
 "Utilities - Water & Fiber",
]
ov=wb['Overview']
for i,c in enumerate(CATS):
    ov[f'B{37+i}']=c

DATE="2026-06-12"
# (Category, Question, VDR Ref, Priority, Status, Seller Response so far, Buyer Follow-Up)
rows=[
 ("Transaction & Process",
  "Can you confirm the process mechanics - bid date, number of rounds, diligence window, and the target sign/close - and whether a lead bidder can get exclusivity? Is there any flexibility beyond a 100% cash asset sale (e.g., seller note, phased takedown)?",
  "1.1","Highest","Partial",
  "Two-stage auction; initial bids targeted ~mid-July; CIM/VDR provided post-NDA in round one; sellers' preference is a 100% cash asset sale.",
  "Need the bid deadline and diligence window in writing, and whether exclusivity opens up after round one."),

 ("Title, Seller & IDA",
  "Please load the full title commitment with Schedule B exceptions and confirm the closing mechanics to deliver clean title - payoff/discharge of the Bank OZK loan (~$52.6M) and release of the Sunbelt Rentals mechanics lien (~$30.5K).",
  "3.1","High","Partial",
  "WF Industrial XII LLC is fee owner with good & marketable title; existing indebtedness expected to be paid off at closing from sale proceeds.",
  "Confirm the OZK discharge and Sunbelt lien release will be in hand at closing."),

 ("Title, Seller & IDA",
  "Can you share the IDA documents (Company Lease, Lease & Project Agreement, PILOT schedule) and walk us through the consent path for a change of use and change of control - including any recapture exposure if we convert to data center use?",
  "Not in VDR - please add","High","Partial",
  "Property subject to a Town of Brookhaven IDA lease/leaseback (WF remains fee owner); IDA defines the project as warehouse/distribution; IDA consent required for change of use; a sale without consent can trigger recapture; seller in discussions with TOBIDA.",
  "Need the executed IDA instruments and TOBIDA's written position on consent/recapture."),

 ("Power - Interconnection",
  "Please provide queue-position evidence for NYISO Q#1721 and the draft Interconnection Agreement when available, and confirm the IA and queue position transfer on a change of control without a restudy or timeline reset.",
  "2.2, 2.3","Highest","Partial",
  "IA application submitted 10/30/2024 under Q#1721; IA expected to execute Q3 2026 for 177 MW; Facilities Study Agreement is binding on successors and assigns; seller holds biweekly PSEG-LI meetings and is on schedule; cited as the only DC in the LI queue per NYISO's public queue.",
  "Want written confirmation a buyer inherits the position cleanly, plus the public NYISO queue cite."),

 ("Power - Interconnection",
  "Help us reconcile the load basis - the CIM cites 177 MW but the SIS studies 176.6 MW. Which figure carries into the IA and ESA, and would any increase trigger a NYISO restudy?",
  "2.2, 1.1","High","Partial",
  "Final SIS supports a 176.6 MW studied load with no significant adverse reliability impacts; any load revision requires NYISO review and may require a limited restudy.",
  "Confirm the contracted MW figure that will sit in the IA/ESA."),

 ("Power - Substation & Schedule",
  "This is our biggest open item: please reconcile the energization timeline. LIPA's SIS estimates ~39 months from IA execution for the substation and system upgrades, but the CIM markets first power in 2027 and your note suggests a ~12-month buyer self-build. What's the realistic in-service date, and what specifically drives the 39 months - the system upgrades (SUF/CTOAF/SASUF) or the substation itself?",
  "2.2, 2.3","Highest","Partial",
  "LIPA gave a non-binding estimate of 39 months from IA completion for the substation and relevant upgrades; alternatively the buyer (or LIPA-approved 3rd party) can build the substation in ~12 months with LIPA-approved design; SIS says PSEG-LI makes power available upon substation completion; the 90 MW (2027)/86 MW (2028) ramp is indicative, not contractual.",
  "Need the upgrade scope and sequence behind the 39 months, and a realistic energization date we can underwrite."),

 ("Power - Substation & Schedule",
  "Clarify the substation ownership and build split: materials indicate PSEG-LI owns the switching station/substation while the buyer funds and builds it. Who actually constructs what, and how does that interact with the 12- vs 39-month paths?",
  "2.1, 4.3","High","Partial",
  "On-site 138 kV 2N design: ~3.5-ac transformer/switchgear yard + ~1-ac PSEG-LI switching substation, 4 x 66 MVA; PSEG-LI will own the substation, customer owns downstream equipment; procurement/construction is the buyer's responsibility; design can't finalize until the facility study completes (~Aug 2026).",
  "Need the ownership/build boundary in writing and how it gates the timeline."),

 ("Power - Substation & Schedule",
  "Which substation budget is the basis - Clune (~$69.4M) or Hunter Roberts (~$84.0M)? And please share long-lead procurement status, quotes, and lead times for the 4 x 66 MVA transformers, HV breakers, and switchgear.",
  "4.3","High","Partial",
  "Seller cited a Clune ROM of ~$70M (~$50M electrical, ~$10M GC, ~$5M site & building, ~$5M contingency) and ~1-year construction.",
  "Hunter Roberts (~$84M) is also in the room - which governs? Transformer lead time is the critical path; has anything been ordered or quoted?"),

 ("Power - Commercial / ESA",
  "Please provide the draft Electric Service Agreement and confirm the all-in rate, term, escalation, and any credit/security. The CIM cites ~$0.15/kWh under Rate 285 'subject to the executed ESA' - what collateral sizing and CIAC/transmission security are payable?",
  "2.3, 1.1","Highest","Partial",
  "A 177 MW load falls under Rate 285 (large commercial); the ~$0.15/kWh delivery rate is subject to confirmation under the executed ESA (expected Q4 2026).",
  "Need the ESA draft, collateral sizing, and the CIAC figure."),

 ("Power - Commercial / ESA",
  "Can you confirm the SIS's ~$25.34M (+/-50%) LIPA upgrade cost estimate and how it's allocated between LIPA and the customer, and share the Facilities Study cost/schedule output when it lands?",
  "2.2, 2.3","Medium","Partial",
  "Facilities Study Agreement required a $90K deposit; study runs ~150 days to draft and ~180 days to final; cost allocation not yet bound.",
  "Need the bound upgrade cost and allocation once the Facilities Study completes (~Aug 2026)."),

 ("Regulatory - NY Moratorium",
  "Given S10642 passed both houses on 6/4-6/5/26, what's your read on signing vs. veto timing, and would you accept a regulatory closing condition / outside-date relief / price adjustment tied to the outcome?",
  "1.1","Highest","Partial",
  "Seller's advisors expect Senate passage but anticipate a Hochul veto; she has until 12/31/26 and is viewed as unlikely to act before the November midterms; seller is open to entertaining a regulatory closing condition.",
  "We'll want this reflected in the PSA - confirm the seller will paper a regulatory CP."),

 ("Regulatory - NY Moratorium",
  "Please share your counsel's grandfathering analysis: does the completed warehouse construction satisfy 'commencing construction,' and which existing campus permits can be modified (rather than newly issued) under the DEC moratorium's exceptions?",
  "3.3 (+ permit set - please add)","High","Open",
  "Site already holds local/county/utility approvals (SCWA Aug'22, Pine Barrens Nov'22, SCDHS Nov'22, Planning Board Dec'22, NYSDOT Dec'22, tree-clearing/site-work/building permits, temp CO Apr'24, final CO Jun'24); substation/fitout still need Town permits; a Minor Site Plan is under review.",
  "Need the written grandfathering opinion and the modify-vs-new permit list."),

 ("Regulatory - NY Moratorium",
  "How do you see the permanent S10642 obligations applying here - host-community-benefit funding via the LIPA program, prevailing wage/PLA and domestic steel for the retrofit, and the renewable-supply standard (>=1/3 by 2030 rising to 90% by 2040)? What's the compliance plan?",
  "1.1","High","Open",
  "Town to hold a public hearing July 16 on an 18-month data center moratorium; seller reports supportive local officials and a planned PR/legal/technical response; fuel-cell and geothermal generation concepts and a capture-and-use system for cooling water are being evaluated.",
  "Need a quantified view of the host-community/renewable/labor obligations and the generation architecture assumed."),

 ("Zoning & Permitting",
  "Confirm the remaining Town conversion path: what site-plan amendment scope (substation, generator yard, cooling plant), building permits, and SEQRA determination does the data-center use still require, and where does the Minor Site Plan application stand?",
  "3.3","High","Partial",
  "Land-use counsel memo confirms data center qualifies as R&D, a permitted use in the L-1 district; a Minor Site Plan application is under review; Town hearing July 16.",
  "Need the remaining-approvals matrix with a timeline and any SEQRA trigger."),

 ("Environmental & Aquifer",
  "Please identify the exact aquifer designation (Central Pine Barrens CGA / Special Groundwater Protection Area / Suffolk Art. 6) and provide the recorded Central Pine Barrens conservation easement and amendment, so we can overlay the protected/non-buildable area and any diesel/chemical-storage and stormwater-recharge limits onto the substation and generator yards.",
  "3.1 (+ designation memo - please add)","High","Partial",
  "Seller notes a sewage-density limit (added floor area requires density credits) and is 'not aware' of diesel-storage or stormwater limits.",
  "Need the recorded easement instrument and the formal designation; the 'not aware' answer needs to be backed by the actual restrictions."),

 ("Environmental & Aquifer",
  "Can you refresh the environmental record for the as-built campus - an updated Phase I ESA (the 2022 report predates construction) and the wetlands delineation and T&E species report that are referenced but not in the room?",
  "5.1 (+ wetlands/species - please add)","High","Partial",
  "Seller points to VDR folders 3/4/5; reports no RECs, open violations, or unresolved conditions; site was wooded forest before the warehouse development.",
  "2022 Phase I is stale and pre-construction; wetlands delineation and species clearance aren't actually in the VDR."),

 ("Design & Conversion",
  "Beyond the substation, what's the remaining conversion capex to a powered shell, and has the geotech (designed for warehouse loads) been validated for data-center equipment - transformer/UPS/generator pads and liquid-cooling slab loads against the 7-inch / 800 PSF slab and 2 tsf bearing?",
  "2.1, 5.2, 4.3","High","Partial",
  "Basis of Design (Syska-Gensler) in 2.1: 7-inch steel-fiber slab (800 PSF, FF45/FL35), 36' clear, 300 W/SF air + 600 W/SF direct-to-chip closed-loop, PUE 1.5, 117 IT MW total (A 44 / B 38 / C 35).",
  "Need a remaining-capex estimate and a geotech check for DC equipment loads vs. the warehouse-designed report."),

 ("Design & Conversion",
  "Confirm the backup-generation architecture assumed in the Basis of Design (diesel vs. fuel cell vs. BESS) and the resulting NYSDEC air-permit applicability in this severe-ozone-nonattainment area - that choice drives both moratorium exposure and the air-permit path.",
  "2.1","Medium","Partial",
  "Title V air permit would be required if the chosen emergency generators trigger it; low-emission designs can avoid it; seller has a fuel-cell concept that should avoid NYSDEC air permits; a NYSDEC stormwater permit applies if >1 acre is disturbed.",
  "Need the emissions/applicability analysis and the architecture actually carried in the BoD."),

 ("Utilities - Water & Fiber",
  "Please provide the SCWA will-serve letter and confirmed capacity on the 14-inch main, and - if a water-cooled configuration is ever contemplated - the cost/timeline for the sewer extension or on-site WWTP under the aquifer constraints.",
  "1.1, 2.1","Medium","Partial",
  "Base design is closed-loop with no external water supply or discharge; SCWA provides general water; a water-cooled option would need three 8-inch taps off the 14-inch mains and possibly a private WWTP/other upgrades.",
  "Need the SCWA will-serve letter and capacity confirmation."),

 ("Utilities - Water & Fiber",
  "Can you share the carrier will-serve letters (AT&T, Cogent, Extenet, Lightpath, OCG, Verizon, Zayo), physically diverse route maps, and latency to the key NYC-metro interconnect points (60 Hudson, 111 8th Ave, NJ campuses)?",
  "2.1 (Feasibility, Appx E)","Medium","Partial",
  "Seven carriers within ~0.5 mi; carrier will-serve represented as provided; fiber appendix referenced in the Feasibility Study.",
  "Need the actual will-serve letters and route-diversity maps, not just the representation."),

 ("Transaction & Process",
  "Confirm there's no relationship, shared infrastructure, or queue competition with the separate ~228-acre 'Brookhaven Logistics Center' rezoning south of the LIE, and whether any expansion option or ROFO is available to a buyer.",
  "n/a","Low","Closed",
  "Seller states there is no relationship - it's a separate project and ownership entity on the south side of the Long Island Expressway; this site is on the north side.",
  "Confirmed separate; closed unless an expansion option becomes relevant."),
]

bw=wb['Buyer']
start=5
wrap=Alignment(wrap_text=True, vertical='top')
for i,(cat,q,vdr,prio,status,resp,follow) in enumerate(rows):
    r=start+i
    bw[f'C{r}']=DATE
    bw[f'D{r}']=cat
    bw[f'E{r}']=q
    bw[f'F{r}']=vdr
    bw[f'G{r}']=prio
    bw[f'H{r}']=status
    bw[f'I{r}']=DATE
    bw[f'J{r}']=resp
    bw[f'K{r}']=follow
    for col in 'CDEFGHIJK':
        bw[f'{col}{r}'].alignment=wrap

# Guarantee working dropdowns on the Buyer tab (openpyxl drops the x14 list-from-range)
bw.data_validations.dataValidation=[]
dv_cat=DataValidation(type="list", formula1='Overview!$B$37:$B$46', allow_blank=True)
dv_pri=DataValidation(type="list", formula1='"Highest,High,Medium,Low"', allow_blank=True)
dv_sta=DataValidation(type="list", formula1='"Open,Partial,Closed,N/A"', allow_blank=True)
bw.add_data_validation(dv_cat); dv_cat.add('D5:D104')
bw.add_data_validation(dv_pri); dv_pri.add('G5:G104')
bw.add_data_validation(dv_sta); dv_sta.add('H5:H104')

out='.tmp/beacon-qlog/Project-Beacon-Diligence-Tracker-BUYER-filled.xlsx'
wb.save(out)
print('WROTE', out, 'with', len(rows), 'questions')
# quick verify
wb2=openpyxl.load_workbook(out)
b2=wb2['Buyer']
print('row5 D/E/G/H:', b2['D5'].value,'||', b2['E5'].value[:50],'||',b2['G5'].value,'||',b2['H5'].value)
print('last filled row', start+len(rows)-1)
