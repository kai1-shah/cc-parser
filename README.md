# Credit Card Statement Parser

Extract 5 key data points from credit card statements across multiple issuers.

## 📋 Features

Extracts the following 5 key data points:
1. **Card Issuer** (American Express, Chase, Citibank, Capital One, Bank of America)
2. **Card Last 4 Digits**
3. **Statement Period**
4. **Total Amount Due**
5. **Payment Due Date**

**Bonus:** Also extracts recent transactions

## 🗂️ Project Structure

```
custom_pdf_parser/
├── parser.py                    # Base PDF parser (your existing file)
├── credit_card_parser.py        # NEW - Credit card extraction logic
├── langchain_loader.py          # LangChain integration (existing)
├── pipeline.py                  # Processing pipeline (existing)
├── example.py                   # UPDATED - Menu with CC parsing option
├── test_parser.py              # NEW - Standalone test script
├── debug_parser.py             # NEW - Debug raw text extraction
├── requirements.txt            # Updated dependencies
└── __init__.py                 # Optional
```

## 🚀 Setup

### 1. Install Dependencies

```bash
pip install pypdf
```

### 2. File Placement

Make sure all these files are in the same directory:
- `parser.py` (your existing file - NO changes needed)
- `credit_card_parser.py` (NEW - copy from artifacts)
- `example.py` (UPDATED - copy from artifacts)
- `test_parser.py` (NEW - copy from artifacts)
- `debug_parser.py` (NEW - copy from artifacts)

## 🎯 How to Run

### **Method 1: Using the Enhanced Menu (Recommended)**

Run the updated example.py with the new option:

```bash
python example.py
```

**What you'll see:**
```
👋 Welcome to the Custom PDF Parser!

What would you like to do?

📄 GENERAL PDF PARSING:
  1. View full parsed raw data
  2. Extract full plain text
  ... (your existing options)

💳 CREDIT CARD STATEMENT PARSING:
  9. Parse Credit Card Statement (Extract 5 key data points)

Enter the number of your choice: 9
```

Then enter your PDF path when prompted.

---

### **Method 2: Standalone Test (Quickest for Testing)**

```bash
python test_parser.py
```

This will:
- ✅ Parse the credit card statement
- ✅ Display the 5 key data points
- ✅ Show extracted transactions
- ✅ Save results to `cc_statement_parsed.json`

---

### **Method 3: Debug Mode (When Things Don't Work)**

If data points aren't being extracted correctly:

```bash
python debug_parser.py
```

This will:
- Show you the raw extracted text
- Save complete text to `extracted_text.txt`
- Help you identify what patterns to look for

## 📊 Expected Output

```
================================================================================

✅ EXTRACTION COMPLETE - 5 KEY DATA POINTS

================================================================================

1️⃣  Card Issuer:          Chase
2️⃣  Card Last 4 Digits:   1234
3️⃣  Statement Period:     01/01/2024 to 01/31/2024
4️⃣  Total Amount Due:     $1,234.56
5️⃣  Payment Due Date:     February 25, 2024

================================================================================

💳 TRANSACTIONS FOUND: 5 transaction(s)

  Transaction 1:
    Date:        01/05/2024
    Description: AMAZON.COM
    Amount:      $45.67

  ... (more transactions)

================================================================================

💾 Full results saved to: cc_statement_parsed.json
```

## 🔧 Customization

### Supported Credit Card Issuers

Currently supports:
- American Express
- Chase
- Citibank
- Capital One
- Bank of America

### Adding New Issuers

Edit `credit_card_parser.py`, find the `_detect_issuer()` method:

```python
issuers = {
    "Your Bank Name": ["keyword1", "keyword2"],
    # Add more issuers here
}
```

### Adjusting Extraction Patterns

If patterns don't match your statement format:

1. Run `debug_parser.py` to see raw text
2. Open `extracted_text.txt` to find exact format
3. Edit the regex patterns in `credit_card_parser.py`
4. Test again with `test_parser.py`

**Example:** Adjusting the amount pattern in `_extract_total_amount_due()`:

```python
patterns = [
    r"(?:total|new)\s+(?:amount\s+)?(?:due|balance)[:\s]+\$?([\d,]+\.\d{2})",
    # Add your custom pattern here
    r"your custom pattern here"
]
```

## 📝 Testing Workflow

```bash
# Step 1: Debug to see raw text
python debug_parser.py
# Enter: path/to/your/statement.pdf

# Step 2: Check what was extracted
cat extracted_text.txt

# Step 3: Test the parser
python test_parser.py
# Enter: path/to/your/statement.pdf

# Step 4: View results
cat cc_statement_parsed.json
```

## 🐛 Troubleshooting

### "File not found" error
- Make sure the PDF path is correct
- Remove quotes around the path if copy-pasting
- Use forward slashes (/) or double backslashes (\\\\) on Windows

### "Not found" for data points
- Run `debug_parser.py` to see raw text
- Check if the expected text exists in `extracted_text.txt`
- Adjust regex patterns in `credit_card_parser.py`

### "Unknown" issuer detected
- Add your bank to the `_detect_issuer()` method
- Check the debug output for bank name format

## 📦 Output Files

After running, you'll get:

1. **cc_statement_parsed.json** - Complete extraction results in JSON format
2. **extracted_text.txt** (if using debug mode) - Raw text from PDF

## 🎓 Next Steps

Once credit card parsing works well:
1. Create the web interface (Flask app)
2. Add export to CSV functionality
3. Support batch processing of multiple statements
4. Add data visualization

## 💡 Tips

- Always test with `debug_parser.py` first to see what text is extracted
- Different credit card issuers use different formats - patterns may need adjustment
- The parser works best with text-based PDFs (not scanned images)
- For scanned PDFs, you'll need OCR functionality

## 🤝 Support

If you need help adjusting patterns for your specific credit card issuer, share:
1. Output from `debug_parser.py`
2. The format of data points in your statement (with sensitive info redacted)
