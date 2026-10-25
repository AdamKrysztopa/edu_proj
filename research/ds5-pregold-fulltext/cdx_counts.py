"""DS5 Wayback CDX counts: captures before each gold's cut-off, metadata only.

For each candidate site or page, asks the CDX server for capture lines up to
the cut-off and counts captures and distinct URLs. Never fetches an archived
page. Writes cdx_counts.json next to this file.
    python3 -I cdx_counts.py
"""
import http.client
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

CDX = "https://web.archive.org/cdx/search/cdx"
CAP = 20000

# gold, cut-off (yyyymmdd), [(target, matchType)]
SITES = [
    ("sullivan2014", "20140324", [("en.wikipedia.org/wiki/Cricothyrotomy", "exact"),
                                  ("emedicine.medscape.com", "domain"), ("www.trauma.org", "domain")]),
    ("okoli2020", "20200820", [("en.wikipedia.org/wiki/Incident_Command_System", "exact"),
                               ("www.firehouse.com", "domain"), ("www.fireengineering.com", "domain"),
                               ("www.usfa.fema.gov", "domain")]),
    ("madani2015", "20150805", [("en.wikipedia.org/wiki/Cholecystectomy", "exact"),
                                ("www.sages.org", "domain"), ("www.websurg.com", "domain")]),
    ("logishetty2019", "20190919", [("en.wikipedia.org/wiki/Hip_replacement", "exact"),
                                    ("www.orthobullets.com", "domain"), ("orthoinfo.aaos.org", "domain")]),
    ("grover2022_tar", "20221116", [("en.wikipedia.org/wiki/Incisional_hernia", "exact"),
                                    ("www.americasherniasociety.org", "domain"), ("www.websurg.com", "domain")]),
    ("grover2023_rygb", "20230912", [("en.wikipedia.org/wiki/Gastric_bypass_surgery", "exact"),
                                     ("asmbs.org", "domain"), ("www.websurg.com", "domain")]),
    ("smink2012", "20120209", [("en.wikipedia.org/wiki/Appendectomy", "exact"),
                               ("www.sages.org", "domain"), ("www.websurg.com", "domain")]),
    ("sullivan2007", "20071212", [("en.wikipedia.org/wiki/Colonoscopy", "exact"),
                                  ("www.asge.org", "domain"), ("gi.org", "domain")]),
    ("dias2019", "20190723", [("en.wikipedia.org/wiki/Cardiac_surgery", "exact"),
                              ("www.sts.org", "domain"), ("www.ctsnet.org", "domain")]),
    ("karamchandani2021", "20210623", [("en.wikipedia.org/wiki/Tear_of_meniscus", "exact"),
                                       ("www.orthobullets.com", "domain"), ("www.sportsmed.org", "domain")]),
    ("russjara2023", "20231130", [("en.wikipedia.org/wiki/Drug_interaction", "exact"),
                                  ("www.drugs.com/drug_interactions", "prefix")]),
    ("ede2023", "20231208", [("en.wikipedia.org/wiki/Early_warning_score", "exact"),
                             ("www.nice.org.uk", "domain"), ("www.rcplondon.ac.uk", "domain")]),
    ("canopy2015", "20150629", [("en.wikipedia.org/wiki/Endoscopic_retrograde_cholangiopancreatography", "exact"),
                                ("www.asge.org", "domain")]),
    ("plumptre2017", "20170711", [("en.wikipedia.org/wiki/Pelvic_examination", "exact"),
                                  ("www.acog.org", "domain")]),
    ("phillips1998", "19971231", [("en.wikipedia.org/wiki/Urban_warfare", "exact"),
                                  ("www.fas.org", "domain"), ("www.army.mil", "domain"),
                                  ("www.globalsecurity.org", "domain")]),
    ("phillips2001", "20010731", [("en.wikipedia.org/wiki/Urban_warfare", "exact"),
                                  ("www.fas.org", "domain"), ("www.army.mil", "domain"),
                                  ("www.globalsecurity.org", "domain")]),
]


def cdx(target, match, to):
    params = {"url": target, "matchType": match, "to": to, "fl": "timestamp,urlkey,statuscode",
              "filter": "statuscode:200", "limit": CAP}
    url = CDX + "?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            time.sleep(2)
            with urllib.request.urlopen(url, timeout=300) as r:
                lines = r.read().decode("utf8", "ignore").splitlines()
            break
        except (urllib.error.URLError, TimeoutError, http.client.HTTPException, ConnectionError) as e:
            if attempt == 3:
                return {"error": str(e)}
            time.sleep(20 * (attempt + 1))
    stamps = [ln.split(" ")[0] for ln in lines if ln]
    return {"captures_200": len(stamps), "capped": len(stamps) >= CAP,
            "distinct_urls": len({ln.split(" ")[1] for ln in lines if ln}),
            "first": min(stamps) if stamps else None, "last": max(stamps) if stamps else None}


def main():
    rows = []
    for gold, to, targets in SITES:
        for target, match in targets:
            res = cdx(target, match, to)
            rows.append({"gold": gold, "cutoff": to, "target": target, "matchType": match, **res})
            print(gold, target, res, flush=True)
    doc = {"retrieved": date.today().isoformat(), "api": CDX, "cap_per_query": CAP,
           "method": "statuscode:200 captures with timestamp <= cutoff; counts only, no page fetched",
           "rows": rows}
    Path(__file__).with_name("cdx_counts.json").write_text(json.dumps(doc, indent=1) + "\n")


if __name__ == "__main__":
    main()
