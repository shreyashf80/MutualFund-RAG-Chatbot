import re
from bs4 import BeautifulSoup, Comment

from typing import Tuple

def clean_text(raw_html: str) -> Tuple[str, dict]:
    """
    Clean raw HTML by stripping tags, nav, footers, ads, and normalizing whitespace.
    Removes duplicate content blocks to keep the data concise.
    """
    if not raw_html:
        return "", {}
        
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # Check if this is a recognized Groww mutual fund page
    details_container = soup.find(class_=lambda c: c and "fundDetailsContainer" in c)
    h1 = soup.find("h1")
    
    if details_container and h1:
        # Structured cleaning: extract key facts and generate a clean text profile
        facts = {}
        
        # 1. Scheme Name
        facts["scheme_name"] = h1.get_text(strip=True)
        
        # 2. Category & Pills
        pills_container = soup.find(class_=lambda c: c and "pills_container" in c)
        if pills_container:
            pills = [p.get_text(strip=True) for p in pills_container.find_all(class_=lambda c: c and "pill12Pill" in c)]
            facts["category"] = pills[0] if len(pills) > 0 else "N/A"
            facts["sub_category"] = pills[1] if len(pills) > 1 else "N/A"
            facts["risk_level"] = pills[2] if len(pills) > 2 else "N/A"
        else:
            pills = [p.get_text(strip=True) for p in soup.find_all(class_=lambda c: c and "pill12Pill" in c)]
            facts["category"] = pills[0] if len(pills) > 0 else "N/A"
            facts["sub_category"] = pills[1] if len(pills) > 1 else "N/A"
            risk = "N/A"
            for p in pills:
                if "risk" in p.lower():
                    risk = p
                    break
            facts["risk_level"] = risk

        # 3. Details Container (NAV, Min SIP, AUM, Expense Ratio, Rating, Lock-in)
        for block in details_container.find_all(recursive=False):
            divs = block.find_all(recursive=False)
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
                elif "Lock-in" in key or "lock-in" in key:
                    facts["lock_in_period"] = val
                    
        # 4. Investment Objective & Benchmark
        objective_parts = []
        sections = soup.find_all(class_=lambda c: c and "investmentObjective_contentSection" in c)
        for sec in sections:
            # Look for the actual Investment Objective heading to avoid SEO boilerplate
            title = sec.find("h4", class_=lambda c: c and "investmentObjective_readMoreTitle" in c)
            if title and "Investment Objective" in title.get_text(strip=True):
                # The actual objective is usually the sibling div
                obj_div = title.find_next_sibling("div")
                if obj_div:
                    text = obj_div.get_text(separator=" ", strip=True)
                    text = re.sub(r'\s+', ' ', text)
                    if text:
                        objective_parts.append(text)
            else:
                # Fallback if the heading is not found
                import copy
                sec_copy = copy.copy(sec)
                bench_row = sec_copy.find(class_=lambda c: c and "investmentObjective_benchmarkRow" in c)
                if bench_row:
                    bench_row.decompose()
                text = sec_copy.get_text(separator=" ", strip=True)
                if "launched by HDFC Mutual Fund" not in text:  # Skip generic boilerplate
                    text = text.replace("Investment Objective", "").replace("Scheme Information Document(SID)", "").strip()
                    text = re.sub(r'\s+', ' ', text)
                    if text:
                        objective_parts.append(text)
                        
        facts["investment_objective"] = " ".join(objective_parts)
        
        bench_row = soup.find(class_=lambda c: c and "investmentObjective_benchmarkRow" in c)
        if bench_row:
            children = bench_row.find_all(recursive=False)
            facts["benchmark"] = children[-1].get_text(strip=True) if children else "N/A"
        else:
            facts["benchmark"] = "N/A"
            
        # 5. Exit Load, Stamp Duty and Tax
        tax_container = soup.find(class_=lambda c: c and "exitLoadStampDutyTax_container" in c)
        facts["exit_load"] = "N/A"
        facts["stamp_duty"] = "N/A"
        facts["tax_implication"] = "N/A"
        if tax_container:
            sections_elements = tax_container.find_all(class_=lambda c: c and "exitLoadStampDutyTax_section" in c)
            for sec in sections_elements:
                divs = sec.find_all(recursive=False)
                if len(divs) >= 2:
                    key = divs[0].get_text(strip=True)
                    val = divs[1].get_text(separator=" ", strip=True)
                    val = re.sub(r'\s+', ' ', val).strip()
                    if "Exit load" in key:
                        facts["exit_load"] = val
                    elif "Stamp duty" in key:
                        facts["stamp_duty"] = val
                    elif "Tax implication" in key:
                        facts["tax_implication"] = val

        # 6. Fund Managers
        managers = []
        accordions = soup.find_all(class_=lambda c: c and any(x.startswith("fundManagement_accordion__") for x in c.split()))
        for acc in accordions:
            mgr = {}
            name_tag = acc.find(class_=lambda c: c and "fundManagement_personName" in c)
            if name_tag:
                mgr["name"] = name_tag.get_text(strip=True)
            else:
                continue
            card_text_div = name_tag.parent
            if card_text_div:
                tenure_div = card_text_div.find(class_=lambda c: c and "bodyLarge" in c)
                if tenure_div:
                    mgr["tenure"] = tenure_div.get_text(strip=True)
            body = acc.find(class_=lambda c: c and "ac11Hidden" in c)
            if body:
                exp_content = body.find(class_=lambda c: c and "fundManagement_expandedContent" in c)
                if exp_content:
                    for block in exp_content.find_all(recursive=False):
                        title_div = block.find(class_=lambda c: c and "fundManagement_detailTitle" in c)
                        if title_div:
                            title = title_div.get_text(strip=True).lower()
                            content_div = title_div.find_next_sibling()
                            if content_div:
                                content_val = content_div.get_text(separator=", ", strip=True)
                                content_val = re.sub(r'\s+', ' ', content_val).strip()
                                if "education" in title:
                                    mgr["education"] = content_val
                                elif "experience" in title:
                                    mgr["experience"] = content_val
                                elif "manages" in title:
                                    mgr["other_schemes"] = content_val
            managers.append(mgr)
        facts["fund_managers"] = managers
        
        # 7. Generate clean formatted text profile
        lines = []
        lines.append(f"Scheme Name: {facts['scheme_name']}")
        lines.append(f"Category: {facts.get('category', 'N/A')}")
        lines.append(f"Sub-Category: {facts.get('sub_category', 'N/A')}")
        lines.append(f"Risk Level: {facts.get('risk_level', 'N/A')}")
        lines.append(f"Latest NAV: {facts.get('nav', 'N/A')}")
        lines.append(f"Minimum SIP Amount: {facts.get('min_sip', 'N/A')}")
        lines.append(f"Fund Size (AUM): {facts.get('aum', 'N/A')}")
        lines.append(f"Expense Ratio: {facts.get('expense_ratio', 'N/A')}")
        lines.append(f"Rating: {facts.get('rating', 'N/A')}")
        lines.append(f"Fund Benchmark: {facts.get('benchmark', 'N/A')}")
        if facts.get("lock_in_period"):
            lines.append(f"Lock-in Period: {facts['lock_in_period']}")
        lines.append("")
        lines.append(f"Investment Objective:\n{facts.get('investment_objective', 'N/A')}")
        lines.append("")
        lines.append("Exit Load & Tax Implications:")
        lines.append(f"- Exit Load: {facts.get('exit_load', 'N/A')}")
        lines.append(f"- Stamp Duty: {facts.get('stamp_duty', 'N/A')}")
        lines.append(f"- Tax Implication: {facts.get('tax_implication', 'N/A')}")
        lines.append("")
        lines.append("Fund Managers:")
        for i, mgr in enumerate(facts.get("fund_managers", []), 1):
            tenure = f" (Tenure: {mgr['tenure']})" if mgr.get('tenure') else ""
            lines.append(f"{i}. {mgr.get('name', 'Unknown')}{tenure}")
            if mgr.get("education"):
                lines.append(f"   - Education: {mgr['education']}")
            if mgr.get("experience"):
                lines.append(f"   - Experience: {mgr['experience']}")
            if mgr.get("other_schemes"):
                lines.append(f"   - Other Schemes Managed: {mgr['other_schemes']}")
                
                
        return "\n".join(lines), facts
        
    else:
        # Fallback to generic HTML cleaning if page structure is not recognized
        for element in soup(["script", "style", "noscript", "iframe", "svg", "img"]):
            element.decompose()
            
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
            
        for tag in soup(["nav", "footer", "header", "aside"]):
            tag.decompose()
            
        # Remove ad blocks
        to_decompose = []
        for tag in soup.find_all(True):
            if tag.attrs is None:
                continue
            classes = tag.get("class", [])
            tag_id = tag.get("id", "")
            if isinstance(classes, list):
                class_str = " ".join(classes).lower()
            else:
                class_str = str(classes).lower()
            id_str = str(tag_id).lower()
            if any(kw in class_str or kw in id_str for kw in ["ad-", "banner", "promo"]):
                to_decompose.append(tag)
        for tag in to_decompose:
            if tag.parent is not None:
                tag.decompose()
                
        text = soup.get_text(separator=" ")
        text = text.replace('\xa0', ' ')
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        text = text.strip()
        
        # Deduplication
        lines = text.split('\n')
        seen_lines = set()
        deduped_lines = []
        for line in lines:
            line_strip = line.strip()
            if not line_strip:
                deduped_lines.append(line)
                continue
            if line_strip not in seen_lines:
                seen_lines.add(line_strip)
                deduped_lines.append(line)
                
        return '\n'.join(deduped_lines), {}
