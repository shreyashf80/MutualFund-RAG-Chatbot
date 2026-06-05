from bs4 import BeautifulSoup
from pathlib import Path

raw_html_path = Path("/Users/shreyash/NextLeap/Groww_Milestone/data/raw/hdfc-mid-cap-fund-direct-growth.html")

with open(raw_html_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("--- Testing class split for accordion ---")
accordions = soup.find_all(class_=lambda c: c and any(x.startswith("fundManagement_accordion__") for x in c.split()))
print(f"Found {len(accordions)} accordion containers.")
for i, acc in enumerate(accordions):
    name_tag = acc.find(class_=lambda c: c and "fundManagement_personName" in c)
    name = name_tag.get_text(strip=True) if name_tag else "Unknown"
    print(f"  Accordion {i}: manager={name}, class={acc.get('class')}")
    
    # Let's inspect if we can find expanded content inside this accordion
    body = acc.find(class_=lambda c: c and "ac11Hidden" in c)
    print(f"    Has body? {'Yes' if body else 'No'}")
    if body:
        exp = body.find(class_=lambda c: c and "fundManagement_expandedContent" in c)
        print(f"    Has expanded content? {'Yes' if exp else 'No'}")
        if exp:
            print(f"      Text: {exp.get_text(separator=' | ', strip=True)[:150]}")

print("\n--- Testing global benchmark search ---")
bench_row = soup.find(class_=lambda c: c and "investmentObjective_benchmarkRow" in c)
if bench_row:
    print(f"Found benchmark row. Text: {bench_row.get_text(separator=' | ', strip=True)}")
    # Find value (direct child spans/divs)
    children = bench_row.find_all(recursive=False)
    if children:
        print(f"  Benchmark value: {children[-1].get_text(strip=True)}")
else:
    print("Benchmark row not found globally.")
