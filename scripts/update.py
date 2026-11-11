import json, re, sys, urllib.request, datetime

# Cursul oficial BNM pentru EUR (lei MDL pentru 1 EUR)
for back in range(0, 5):
    d = datetime.date.today() - datetime.timedelta(days=back)
    url = "https://www.bnm.md/en/official_exchange_rates?get_xml=1&date=" + d.strftime("%d.%m.%Y")
    try:
        xml = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode("utf-8", "ignore")
    except Exception as e:
        print("eroare", url, e); continue
    m = re.search(r"<CharCode>EUR</CharCode>\s*<Nominal>(\d+)</Nominal>.*?<Value>([\d.,]+)</Value>", xml, re.S)
    if m:
        rate = float(m.group(2).replace(",", ".")) / float(m.group(1))
        json.dump({"EUR_MDL": round(rate, 4), "date": d.isoformat(), "source": "bnm.md"}, open("rate.json", "w"))
        print("OK", rate, d); sys.exit(0)
print("Nu am gasit cursul"); sys.exit(1)
