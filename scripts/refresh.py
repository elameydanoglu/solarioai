import json, re, sys, datetime
page, data = sys.argv[1], sys.argv[2]
html = open(page, encoding="utf-8").read()
m = re.search(r'(<script type="application/json" id="model">)(.*?)(</script>)', html, re.S)
M = json.loads(m.group(2))
d = json.load(open(data))["daily"]
keys = ["temperature_2m_mean", "relative_humidity_2m_mean", "precipitation_sum", "cloud_cover_mean", "shortwave_radiation_sum"]
rows = [[d["time"][i]] + [d[k][i] for k in keys] for i in range(len(d["time"])) if all(d[k][i] is not None for k in keys)]
last = rows[-4:]
dates = [datetime.date.fromisoformat(r[0]) for r in last]
assert len(last) == 4 and all((dates[i+1] - dates[i]).days == 1 for i in range(3)), "need 4 consecutive complete days"
if last[-1][0] <= M["issued"]:
    print("NO_NEW_DATA", M["issued"]); sys.exit(0)
M["recent"] = [[r[0], r[1], int(r[2]), r[3], int(r[4]), r[5] / 3.6] for r in last]
M["issued"] = last[-1][0]
html = html[:m.start(2)] + json.dumps(M, separators=(",", ":")) + html[m.end(2):]
open(page, "w", encoding="utf-8").write(html)
print("UPDATED", M["issued"], [round(r[5], 3) for r in M["recent"]])
