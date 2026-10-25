"""DS5 metadata-only counts of pre-gold works per gold domain (OpenAlex).

Never fetches a gold paper or any work's full text: only aggregate counts
(`group_bys`) and, with --sample, five random titles per query for a
precision check. Usage:
    python3 -I openalex_counts.py --sample   # print titles, write nothing
    python3 -I openalex_counts.py            # write openalex_counts.json
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

API = "https://api.openalex.org/works"

# id, DS1 verdict, gold DOI, cut-off (day before the gold's OpenAlex date), domain query
GOLDS = [
    ("sullivan2014", "P", "10.1097/acm.0000000000000224", "2014-03-24",
     '(cricothyrotomy OR cricothyroidotomy OR "surgical airway")'),
    ("okoli2020", "P", "10.1108/ijdrbe-09-2020-086", "2020-08-20",
     '("incident command" OR "incident commander" OR "incident commanders" OR fireground OR "fire ground" OR ((firefighting OR firefighter OR firefighters OR "fire service") AND ("decision making" OR command OR tactics OR tactical)))'),
    ("madani2015", "P", "10.1016/j.jamcollsurg.2015.07.450", "2015-08-05",
     '"laparoscopic cholecystectomy"'),
    ("logishetty2019", "P", "10.2106/jbjs.19.00121", "2019-09-19",
     '("anterior approach" AND hip AND arthroplasty)'),
    ("grover2022_tar", "P", "10.1097/sla.0000000000005756", "2022-11-16",
     '"transversus abdominis release"'),
    ("grover2023_rygb", "P", "10.1007/s00464-023-10354-w", "2023-09-12",
     '"Roux-en-Y gastric bypass"'),
    ("smink2012", "P", "10.1016/j.amjsurg.2011.11.002", "2012-02-09",
     '"laparoscopic appendectomy"'),
    ("sullivan2007", "P", "10.1016/j.amjsurg.2007.08.051", "2007-12-12",
     'colonoscopy'),
    ("dias2019", "P", "10.1097/sla.0000000000003489", "2019-07-23",
     '(("cardiac surgery" OR "cardiac surgical" OR "cardiac operating room") AND (teamwork OR team OR teams OR "non-technical skills" OR communication))'),
    ("karamchandani2021", "P", "10.1177/03635465211021652", "2021-06-23",
     '("meniscal repair" OR "meniscus repair")'),
    ("russjara2023", "P", "10.1136/bmjopen-2023-075512", "2023-11-30",
     '(("drug-drug interaction" OR "drug-drug interactions") AND (management OR alert OR alerts OR prescribing OR prescriber OR prescribers OR "decision support"))'),
    ("ede2023", "P", "10.1016/j.ijnurstu.2023.104671", "2023-12-08",
     '(("deteriorating patient" OR "deteriorating patients" OR "clinical deterioration" OR "early warning score" OR "rapid response team") AND (nurse OR nurses OR nursing OR escalation))'),
    ("canopy2015", "P", "10.1016/j.amjsurg.2015.05.006", "2015-06-29",
     '("endoscopic retrograde cholangiopancreatography" OR ERCP)'),
    ("plumptre2017", "P", "10.1002/ijgo.12260", "2017-07-11",
     '("pelvic examination" OR "bimanual examination" OR "vaginal examination")'),
    ("phillips1998", "P", "10.1037/e444522005-001", "1997-12-31",
     '("urban operations" OR "urbanized terrain" OR "urban warfare" OR "urban combat")'),
    ("phillips2001", "P", "10.21236/ada395934", "2001-07-31",
     '("urban operations" OR "urbanized terrain" OR "urban warfare" OR "urban combat")'),
    ("seamster1993", "P", "10.1207/s15327108ijap0304_2", "1993-09-30",
     '("air traffic control" OR "air traffic controller" OR "air traffic controllers")'),
    ("crandall1993", "U", "10.1097/00012272-199309000-00006", "1993-08-31",
     '((neonatal OR neonate OR NICU) AND (sepsis OR infection) AND (nurse OR nurses OR nursing))'),
    ("chao1994", "U", "10.1080/10447319409526093", "1994-06-30",
     '((troubleshooting OR "fault diagnosis") AND (expert OR experts OR expertise OR knowledge))'),
]

GROUP_ALL = "oa_status,type,has_content.pdf,best_oa_location.license"
GROUP_CLOSED = "primary_location.source.host_organization"


def get(params):
    for attempt in range(5):
        time.sleep(1.5)
        try:
            with urllib.request.urlopen(API + "?" + urllib.parse.urlencode(params), timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 4:
                raise
            time.sleep(10 * (attempt + 1))


def groups(resp):
    return {g["group_by_key"]: {x["key_display_name"] or "unknown": x["count"] for x in g["groups"]}
            for g in resp["group_bys"]}


def filt(query, cutoff, extra=""):
    f = f"title_and_abstract.search:{query},to_publication_date:{cutoff}"
    return f + ("," + extra if extra else "")


def sample(only):
    for gid, _, _, cutoff, q in GOLDS:
        if only and gid not in only:
            continue
        r = get({"filter": filt(q, cutoff), "sample": 5, "seed": 5, "per_page": 5,
                 "select": "display_name,publication_year"})
        print(f"\n{gid} n={r['meta']['count']}")
        for w in r["results"]:
            print(f"  {w['publication_year']} {(w['display_name'] or '')[:110]}")


def main():
    out, cost = [], 0.0
    for gid, verdict, doi, cutoff, q in GOLDS:
        a = get({"filter": filt(q, cutoff), "group_bys": GROUP_ALL, "per_page": 200})
        c = get({"filter": filt(q, cutoff, "oa_status:closed"), "group_bys": GROUP_CLOSED, "per_page": 200})
        cost += (a["meta"].get("cost_usd") or 0) + (c["meta"].get("cost_usd") or 0)
        ga, gc = groups(a), groups(c)
        n = a["meta"]["count"]
        oa = ga["oa_status"]
        n_open = n - oa.get("closed", 0)
        lic = ga["best_oa_location.license"]
        n_licensed = sum(v for k, v in lic.items() if k.lower().startswith(("cc", "public")))
        out.append({
            "gold": gid, "ds1_verdict": verdict, "gold_doi": doi, "cutoff": cutoff, "query": q,
            "n_pregold": n,
            "n_free_to_read": n_open,
            "n_openalex_pdf": ga["has_content.pdf"].get("true", 0),
            "n_open_licence": n_licensed,
            "oa_status": oa,
            "type": ga["type"],
            "licence": lic,
            "closed_by_publisher": gc[GROUP_CLOSED],
        })
    doc = {"retrieved": date.today().isoformat(), "api": API,
           "method": "title_and_abstract.search, to_publication_date = cutoff, group_bys; counts only",
           "cost_usd": round(cost, 4), "golds": out}
    Path(__file__).with_suffix(".json").write_text(json.dumps(doc, indent=1) + "\n")
    print("wrote", Path(__file__).with_suffix(".json"), "cost", round(cost, 4))


if __name__ == "__main__":
    if "--sample" in sys.argv:
        sample(sys.argv[sys.argv.index("--sample") + 1:])
    else:
        main()
