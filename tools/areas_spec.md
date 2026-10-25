# Areas-extraction spec — strategic areas per evaluation (both regimes)

You turn the Portuguese strategic-area block of an NT into one structured, anonymized English record per evaluation.
Input: your batch JSON. Each item has `id`, `regime`, `header_ae`, `header_total`, hints from a regex parser
(`areas_total`, `parsed_areas` / `parsed_criteria`, may be empty or wrong) and `segment_pt` (the raw NT slice).
Output: one file per item `<out_dir>/<id>.json` (use the Write tool; `out_dir` is given in the batch file).

## Anonymization (checked by a validator; violations invalidate the record)
Never write entity/proponent names, state or municipality names, river/park/program/institution names or acronyms, people,
SEI/PFE/CC/NT numbers, meeting numbers, calendar dates, currency amounts, or counts/sizes of physical assets or people
(km, ha, hospitals, schools, families, households, inhabitants…). Percent shares of cost rounded to 10% are allowed.
Paraphrase in English, never copy sentences. Area labels come from the tables below, not from the NT.

## Record schema
```json
{
  "id": "A1B2C3D", "regime": "NR1_2024", "status": "ok",
  "areas_total": [4.0, 10.0],
  "areas": [
    {"code": "111", "label": "Sustainable cities", "points": 3.0, "max": 5.0, "level": "B", "scored": true,
     "reason": "Mobility objective directly tied to the area; indicators measurable; large resource share -> high impact."},
    {"code": "211", "label": "Trade", "points": 0.0, "max": 5.0, "level": "", "scored": false,
     "reason": "Declared by proponent; indicators measure cross-border freight only, no export diversification evidence."}
  ],
  "bonus": [
    {"article": "15 par.3 PPA priority", "requested": false, "points": 0.0, "max": 1.0, "accepted": false,
     "justification": "Proponent did not state the programme is exclusively aimed at federal PPA priorities."},
    {"article": "15 par.4 regional integration", "requested": true, "points": 1.0, "max": 1.0, "accepted": true,
     "justification": "Border-location rationale plus indicators on cross-border flows."}
  ],
  "technical": {"design": [1.027, 1.8], "management": [0.9, 1.0], "risk": [0.9, 1.2], "total": [2.847, 4.0]},
  "notes": "optional, <=30 words"
}
```
- `status`: `ok`, or `no_area_scoring_in_nt` when `segment_pt` is empty or has no area scoring (then `areas` = []).
- `scored` = points > 0. Zero-point entries are areas the proponent declared/ the NT assessed but did not accept;
  `reason` says why in one short sentence (≤35 words). For R17 list all 15 criteria; a zero entry means "not accepted/not applicable".
- NR1_2024: one entry per Annex II objective the NT evaluates (code 101–307, max usually 5.0, `level` A–E when printed).
  `areas_total` = the NT's area total (max 10). `bonus` = the two additional points of Res. 1/2024 art. 15:
  §3 PPA priority (resources entirely aimed at federal PPA priorities) and §4 regional integration (frontier).
  `requested` = whether the proponent declared it (read the NT's description of what the proponent indicated; null if unclear);
  `accepted` = points > 0; `justification` = the NT's reasoning in one or two sentences.
- R17_2021: criteria code `1.1`…`1.15`, `max` 0.133 each except 1.15 whose `max` is 0.138 (14 x 0.133 + 0.138 = 2.0); `areas_total` max 2.0. `technical` = the 4.0 technical analysis
  split (design / management / risk); omit a part you cannot read. Res. 17/2021 has no additional-points mechanism:
  `bonus` = [] unless the text clearly shows one (then describe it and say so in `notes`).
- If the NT's numbers are inconsistent (e.g. body says level E, conclusion says D; sub-scores do not add up), record the
  values as printed and add the inconsistency to `notes`.
- Check: sum of `points` equals `areas_total[0]` (±0.002). If not, re-read; if it truly differs, say so in `notes`.

## Label tables
NR1_2024 (PPA 2024-2027 Annex II objectives): 101 Poverty · 102 Health (SUS) · 103 Early childhood and education · 104 Secondary/technical education ·
105 Creative economy · 106 Human rights · 107 Women · 108 Indigenous and quilombola peoples · 109 Anti-racism · 110 Social security ·
111 Sustainable cities · 112 Public safety · 113 Sport · 201 Environment · 202 Disaster resilience and climate adaptation ·
203 Family farming · 204 Decarbonization · 205 Competitiveness · 206 Science, technology and innovation · 207 Labor ·
208 Clean energy · 209 Digital inclusion and connectivity · 210 Logistics and transport · 211 Trade · 212 Water security ·
213 Tourism · 214 Regional equity · 215 Mining · 301 Transparency and participation · 302 State capacity ·
303 Digital government · 304 Defense · 305 International cooperation and regional development · 306 Fiscal sustainability · 307 Justice.

R17_2021 criteria: 1.1 Environmental sustainability, adaptation and mitigation · 1.2 Energy efficiency and renewable energy ·
1.3 Basic sanitation · 1.4 Integrated water-resources management and water security · 1.5 Biodiversity and forest resources ·
1.6 Business environment and opportunities · 1.7 Individual entrepreneurs and micro/small firms ·
1.8 Jobs and income for low-income and vulnerable groups · 1.9 Infrastructure and social facilities for low-income and vulnerable groups ·
1.10 Inclusion of social minorities · 1.11 Youth, gender and race policies · 1.12 Public-service delivery, management and citizen participation ·
1.13 Education and health conditions · 1.14 Technological development, innovation and modernization ·
1.15 Financing arrangements encouraging private participation.

## Mechanics
Work only from your batch (the segment text is inside it; do not read other files except this spec). One Write per item.
Final message: one line per id (`done`, or `skipped:<reason>`) and a short `UNCERTAIN:` list. Do not paste the records.
