

from credit_card_parser import CreditCardStatementParser
import json
from pathlib import Path

def print_separator(char="=", length=80):
    print("\n" + char*length + "\n")

def test_credit_card_parser(pdf_path):
    """Test the credit card parser with a PDF file"""
    
    print_separator()
    print("🔍 CREDIT CARD STATEMENT PARSER - STANDALONE TEST")
    print_separator()
    
    # Check if file exists
    if not Path(pdf_path).exists():
        print(f"❌ Error: File not found at {pdf_path}")
        return
    
    print(f"📄 Processing file: {Path(pdf_path).name}")
    print(f"📁 Full path: {pdf_path}")
    print("\n⏳ Parsing in progress...")
    
    # Initialize parser
    parser = CreditCardStatementParser()
    
    try:
        # Parse the statement
        result = parser.parse_statement(pdf_path)
        
        # Check for errors
        if "error" in result and result.get('issuer') == 'Unknown':
            print_separator()
            print(f"❌ PARSING ERROR: {result['error']}")
            print_separator()
            return
        
        # Display results
        print_separator()
        print("✅ EXTRACTION COMPLETE - 5 KEY DATA POINTS")
        print_separator()
        
        print(f"1️⃣  Card Issuer:          {result.get('issuer', 'Not detected')}")
        print(f"2️⃣  Card Last 4 Digits:   {result.get('card_last_4_digits', 'Not found')}")
        print(f"3️⃣  Statement Period:     {result.get('statement_period', 'Not found')}")
        print(f"4️⃣  Total Amount Due:     {result.get('total_amount_due', 'Not found')}")
        print(f"5️⃣  Payment Due Date:     {result.get('payment_due_date', 'Not found')}")
        
        print_separator()
        
        # Display transactions if found
        transactions = result.get('transactions', [])
        if transactions:
            print(f"💳 TRANSACTIONS FOUND: {len(transactions)} transaction(s)\n")
            for i, txn in enumerate(transactions, 1):
                print(f"  Transaction {i}:")
                print(f"    Date:        {txn['date']}")
                print(f"    Description: {txn['description']}")
                print(f"    Amount:      {txn['amount']}")
                print()
        else:
            print("💳 TRANSACTIONS: None extracted")
            print("   Note: Transaction patterns may need adjustment for your specific statement\n")
        
        print_separator()
        
        # Display metadata
        print("📋 DOCUMENT INFORMATION\n")
        metadata = result.get('raw_metadata', {})
        print(f"  File Name:       {metadata.get('file_name', 'N/A')}")
        print(f"  File Size:       {metadata.get('file_size', 'N/A')} bytes")
        print(f"  Total Pages:     {metadata.get('total_pages', 'N/A')}")
        print(f"  Extraction Time: {result.get('extraction_timestamp', 'N/A')}")
        
        print_separator()
        
        # Save full results to JSON
        output_file = "cc_statement_parsed.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Full results saved to: {output_file}")
        print("   You can open this file to see all extracted data in JSON format")
        
        print_separator()
        
        # Summary
        found_count = sum([
            1 if result.get('issuer') and result.get('issuer') != 'Unknown' else 0,
            1 if result.get('card_last_4_digits') else 0,
            1 if result.get('statement_period') else 0,
            1 if result.get('total_amount_due') else 0,
            1 if result.get('payment_due_date') else 0
        ])
        
        print("📊 EXTRACTION SUMMARY\n")
        print(f"   ✅ Successfully extracted: {found_count}/5 data points")
        print(f"   💳 Transactions extracted: {len(transactions)}")
        
        if found_count < 5:
            print("\n💡 TIP: If some data points are missing:")
            print("   1. Run 'python debug_parser.py' to see raw extracted text")
            print("   2. Check extracted_text.txt to identify the exact patterns")
            print("   3. Adjust regex patterns in credit_card_parser.py accordingly")
        
        print_separator()
        
    except Exception as e:
        print_separator()
        print(f"❌ UNEXPECTED ERROR: {e}")
        print_separator()
        import traceback
        traceback.print_exc()

def main():
    """Main function to run the test"""
    
    print("\n🚀 Credit Card Statement Parser - Standalone Test\n")
    
    # Get PDF path from user
    pdf_path = input("📄 Enter the path to your credit card statement PDF: ").strip()
    
    # Remove quotes if user wrapped path in quotes
    pdf_path = pdf_path.strip('"').strip("'")
    
    # Test the parser
    test_credit_card_parser(pdf_path)
    
    print("\n✨ Test complete!\n")

if __name__ == "__main__":
    main()