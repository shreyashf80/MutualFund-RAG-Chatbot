from src.ingestion.cleaner import clean_text

def test_clean_text_removes_scripts():
    html = """
    <html>
        <body>
            <h1>Fund Name</h1>
            <script>console.log('test');</script>
            <style>.hidden { display: none; }</style>
            <p>This is a test mutual fund.</p>
        </body>
    </html>
    """
    text, facts = clean_text(html)
    assert "Fund Name" in text
    assert "This is a test mutual fund." in text
    assert "console.log" not in text
    assert "display: none" not in text

def test_clean_text_extracts_facts():
    html = """
    <html>
        <body>
            <table>
                <tr><td>Expense Ratio</td><td>0.5%</td></tr>
                <tr><td>Exit Load</td><td>1% within 1 year</td></tr>
            </table>
        </body>
    </html>
    """
    text, facts = clean_text(html)
    assert "Expense Ratio" in text
    assert "0.5%" in text
