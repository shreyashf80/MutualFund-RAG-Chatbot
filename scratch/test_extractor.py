import re
import json
from bs4 import BeautifulSoup
from pathlib import Path

def parse_html_to_facts(html_content: str) -> dict:
    soup = BeautifulSoup(html_content, "html.parser")
    facts = {}
    
    # 1. Scheme Name
    h1 = soup.find("h1")
    facts["scheme_name"] = h1.get_text(strip=True) if h1 else "Unknown Scheme"
    
    # 2. Pills (Category, Sub-Category, Risk)
    pills_container = soup.find(class_=lambda c: c and "pills_container" in "".join(c))
    if pills_container:
        pills = [p.get_text(strip=True) for p in pills_container.find_all(class_=lambda c: c and "pill12Pill" in "".join(c))]
        facts["category"] = pills[0] if len(pills) > 0 else None
        facts["sub_category"] = pills[1] if len(pills) > 1 else None
        facts["risk_level"] = pills[2] if len(pills) > 2 else None
    else:
        pills = [p.get_text(strip=True) for p in soup.find_all(class_=lambda c: c and "pill12Pill" in "".join(c))]
        facts["category"] = pills[0] if len(pills) > 0 else None
        facts["sub_category"] = pills[1] if len(pills) > 1 else None
        risk_level = None
        for pill in pills:
            if "risk" in pill.lower():
                risk_level = pill
                break
        facts["risk_level"] = risk_level

    # 3. Details Container (NAV, Min SIP, AUM, Expense Ratio, Rating)
    details_container = soup.find(class_=lambda c: c and "fundDetailsContainer" in "".join(c))
    if details_container:
        for block in details_container.find_all(recursive=False):
            divs = block.find_all(recursive=False) # Get all children, not just divs
            if len(divs) >= 2:
                key = divs[0].get_text(strip=True)
                val = divs[1].get_text(strip=True)
                if "NAV" in key:
                    facts["nav"] = val
                elif "Min. for SIP" in key or "Min SIP" in key:
                    facts["min_sip"] = val
                elif "Fund size" in key or "AUM" in key:
                    facts["aum"] = val
                elif "Expense ratio" in key:
                    facts["expense_ratio"] = val
                elif "Rating" in key:
                    facts["rating"] = val
                    
    # 4. Investment Objective & Benchmark
    obj_container = soup.find(class_=lambda c: c and "investmentObjective_contentSection" in "".join(c))
    if obj_container:
        text = obj_container.get_text(separator=" ", strip=True)
        # Find benchmark row
        bench_row = obj_container.find(class_=lambda c: c and "investmentObjective_benchmarkRow" in "".join(c))
        if bench_row:
            bench_val = bench_row.find_all(recursive=False) # Get all direct children (spans, divs)
            if len(bench_val) >= 1:
                facts["benchmark"] = bench_val[-1].get_text(strip=True)
                bench_text = bench_row.get_text(separator=" ", strip=True)
                text = text.replace(bench_text, "")
        else:
            facts["benchmark"] = None
        
        # Clean objective text
        text = text.replace("Investment Objective", "").replace("Scheme Information Document(SID)", "").strip()
        # Remove multiple spaces/newlines
        text = re.sub(r'\s+', ' ', text)
        facts["investment_objective"] = text
    else:
        facts["benchmark"] = None
        facts["investment_objective"] = None
        
    # 5. Exit Load, Stamp Duty and Tax
    tax_container = soup.find(class_=lambda c: c and "exitLoadStampDutyTax_container" in "".join(c))
    if tax_container:
        sections = tax_container.find_all(class_=lambda c: c and "exitLoadStampDutyTax_section" in "".join(c))
        for sec in sections:
            divs = sec.find_all(recursive=False) # Get direct children (could be divs, spans, etc.)
            if len(divs) >= 2:
                key = divs[0].get_text(strip=True)
                val = divs[1].get_text(separator=" ", strip=True)
                # Clean up value text
                val = re.sub(r'\s+', ' ', val).strip()
                if "Exit load" in key:
                    facts["exit_load"] = val
                elif "Stamp duty" in key:
                    facts["stamp_duty"] = val
                elif "Tax implication" in key:
                    facts["tax_implication"] = val
    else:
        facts["exit_load"] = None
        facts["stamp_duty"] = None
        facts["tax_implication"] = None

    # 6. Fund Managers
    managers = []
    # Query only accordion containers, avoiding header and icon matches
    accordions = soup.find_all(class_=lambda c: c and any(x.startswith("fundManagement_accordion__") for x in c))
    for acc in accordions:
        mgr = {}
        # Name
        name_tag = acc.find(class_=lambda c: c and "fundManagement_personName" in "".join(c))
        if name_tag:
            mgr["name"] = name_tag.get_text(strip=True)
        else:
            continue
            
        # Tenure
        # In groww, tenure is inside the name card next to the name
        card_text_div = name_tag.parent
        if card_text_div:
            tenure_div = card_text_div.find(class_=lambda c: c and "bodyLarge" in "".join(c))
            if tenure_div:
                mgr["tenure"] = tenure_div.get_text(strip=True)
                
        # Expanded Details (Education, Experience, Other schemes)
        body = acc.find(class_=lambda c: c and "ac11Hidden" in "".join(c))
        if body:
            exp_content = body.find(class_=lambda c: c and "fundManagement_expandedContent" in "".join(c))
            if exp_content:
                for block in exp_content.find_all(recursive=False):
                    title_div = block.find(class_=lambda c: c and "fundManagement_detailTitle" in "".join(c))
                    if title_div:
                        title = title_div.get_text(strip=True).lower()
                        content_div = title_div.find_next_sibling()
                        if content_div:
                            content_val = content_div.get_text(separator=", ", strip=True)
                            # Remove multiple spaces/newlines
                            content_val = re.sub(r'\s+', ' ', content_val).strip()
                            if "education" in title:
                                mgr["education"] = content_val
                            elif "experience" in title:
                                mgr["experience"] = content_val
                            elif "manages" in title:
                                mgr["other_schemes"] = content_val
                                
        managers.append(mgr)
        
    facts["fund_managers"] = managers
    return facts

def generate_facts_text(facts: dict) -> str:
    lines = []
    lines.append(f"Scheme Name: {facts.get('scheme_name')}")
    lines.append(f"Category: {facts.get('category')}")
    lines.append(f"Sub-Category: {facts.get('sub_category')}")
    lines.append(f"Risk Level: {facts.get('risk_level')}")
    lines.append(f"Latest NAV: {facts.get('nav')}")
    lines.append(f"Minimum SIP Amount: {facts.get('min_sip')}")
    lines.append(f"Fund Size (AUM): {facts.get('aum')}")
    lines.append(f"Expense Ratio: {facts.get('expense_ratio')}")
    lines.append(f"Rating: {facts.get('rating')}")
    lines.append(f"Fund Benchmark: {facts.get('benchmark')}")
    lines.append("")
    lines.append(f"Investment Objective:\n{facts.get('investment_objective')}")
    lines.append("")
    lines.append("Exit Load & Tax Implications:")
    lines.append(f"- Exit Load: {facts.get('exit_load')}")
    lines.append(f"- Stamp Duty: {facts.get('stamp_duty')}")
    lines.append(f"- Tax Implication: {facts.get('tax_implication')}")
    lines.append("")
    lines.append("Fund Managers:")
    for i, mgr in enumerate(facts.get("fund_managers", []), 1):
        tenure = f" (Tenure: {mgr.get('tenure')})" if mgr.get('tenure') else ""
        lines.append(f"{i}. {mgr.get('name')}{tenure}")
        if "education" in mgr:
            lines.append(f"   - Education: {mgr.get('education')}")
        if "experience" in mgr:
            lines.append(f"   - Experience: {mgr.get('experience')}")
        if "other_schemes" in mgr:
            lines.append(f"   - Other Schemes Managed: {mgr.get('other_schemes')}")
            
    return "\n".join(lines)

# Run test
raw_html_path = Path("/Users/shreyash/NextLeap/Groww_Milestone/data/raw/hdfc-mid-cap-fund-direct-growth.html")
with open(raw_html_path, "r", encoding="utf-8") as f:
    html = f.read()

facts = parse_html_to_facts(html)
print(json.dumps(facts, indent=2))
print("\n--- GENERATED TEXT PROFILE ---")
print(generate_facts_text(facts))
