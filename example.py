import os
from pathlib import Path
from pipeline import PDFProcessingPipeline
from credit_card_parser import CreditCardStatementParser
import json

def print_separator():
    print("\n" + "="*80 + "\n")

def parse_credit_card_statement(file_path):
    """Parse credit card statement and extract key data points"""
    print_separator()
    print("💳 CREDIT CARD STATEMENT PARSER")
    print_separator()
    
    print("⏳ Parsing your credit card statement...\n")
    
    # Initialize credit card parser
    cc_parser = CreditCardStatementParser()
    
    # Parse the statement
    result = cc_parser.parse_statement(file_path)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    # Display the 5 key data points
    print_separator()
    print("✅ EXTRACTED KEY DATA POINTS")
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
        print(f"💰 RECENT TRANSACTIONS: {len(transactions)} found\n")
        for i, txn in enumerate(transactions, 1):
            print(f"  Transaction {i}:")
            print(f"    Date:        {txn['date']}")
            print(f"    Description: {txn['description']}")
            print(f"    Amount:      {txn['amount']}")
            print()
    else:
        print("💰 No transactions extracted")
        print("   (Patterns may need adjustment for your specific statement format)")
    
    print_separator()
    
    # Display metadata
    print("📋 DOCUMENT INFO")
    print_separator()
    metadata = result.get('raw_metadata', {})
    print(f"File Name:       {metadata.get('file_name', 'N/A')}")
    print(f"File Size:       {metadata.get('file_size', 'N/A')} bytes")
    print(f"Extraction Time: {result.get('extraction_timestamp', 'N/A')}")
    
    print_separator()
    
    # Ask if user wants to save results
    save_choice = input("💾 Save results to JSON file? (y/n): ").strip().lower()
    if save_choice == 'y':
        output_file = "credit_card_parsed_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        print(f"✅ Results saved to: {output_file}")
    
    print_separator()

def main():
    print("👋 Welcome to the Custom PDF Parser!")
    print("\nWhat would you like to do?")
    print("\n📄 GENERAL PDF PARSING:")
    print("  1. View full parsed raw data")
    print("  2. Extract full plain text")
    print("  3. Get LangChain documents (no chunking)")
    print("  4. Get LangChain documents (with chunking)")
    print("  5. Show document metadata")
    print("  6. Show per-page metadata")
    print("  7. Show cleaned page text (header/footer removed)")
    print("  8. Show extracted image metadata")
    print("\n💳 CREDIT CARD STATEMENT PARSING:")
    print("  9. Parse Credit Card Statement (Extract 5 key data points)")
    
    choice = input("\nEnter the number of your choice: ").strip()
    
    if choice not in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
        print("❌ Invalid option.")
        return
    
    file_path = input("Enter the path to your PDF file: ").strip()
    
    # Remove quotes if present
    file_path = file_path.strip('"').strip("'")
    
    if not Path(file_path).exists():
        print("❌ File not found.")
        return
    
    # Option 9: Credit Card Statement Parsing
    if choice == '9':
        parse_credit_card_statement(file_path)
        return
    
    # Initialize pipeline for general PDF parsing (options 1-8)
    pipeline = PDFProcessingPipeline({
        "preserve_layout": False,
        "remove_headers_footers": True,
        "extract_images": True,
        "min_text_length": 20
    })
    
    # Raw data is needed for most options
    parsed = pipeline.process_single_pdf(file_path, output_format="raw")
    
    if choice == '1':
        print("\n" + "="*80)
        print("Full Raw Parsed Output:")
        print("="*80 + "\n")
        for k, v in parsed.items():
            print(f"{k}: {str(v)[:300]}...")
    
    elif choice == '2':
        print("\n" + "="*80)
        print("Full Cleaned Text (truncated preview):")
        print("="*80 + "\n")
        print("Previewing the first 1000 characters:\n")
        print(parsed["full_text"][:1000], "...")
    
    elif choice == '3':
        docs = pipeline.process_single_pdf(file_path, output_format="langchain", chunk_documents=False)
        print("\n" + "="*80)
        print(f"LangChain Documents: {len(docs)}")
        print("="*80 + "\n")
        print("Previewing the first 500 characters:\n", docs[0].page_content[:500], "...")
    
    elif choice == '4':
        docs = pipeline.process_single_pdf(file_path, output_format="langchain", chunk_documents=True)
        print("\n" + "="*80)
        print(f"LangChain Chunks: {len(docs)}")
        print("="*80 + "\n")
        print("Sample chunk content (first 500 chars):")
        print(docs[0].page_content[:500], "...")
    
    elif choice == '5':
        print("\n" + "="*80)
        print("Document Metadata:")
        print("="*80 + "\n")
        for key, value in parsed["document_metadata"].items():
            print(f"{key}: {value}")
    
    elif choice == '6':
        print("\n" + "="*80)
        print("Per-page Metadata:")
        print("="*80 + "\n")
        for i, page in enumerate(parsed["pages"]):
            print(f"Page {i+1}: {page['metadata']}")
    
    elif choice == '7':
        print("\n" + "="*80)
        print("Cleaned Text After Header/Footer Removal")
        print("="*80 + "\n")
        print("Showing the first 3 pages and first 500 characters of text from each page.\n")
        for i, page in enumerate(parsed["pages"][:3]):  # First 3 pages
            print(f"\n--- Page {i+1} ---")
            print(page["text"][:500], "...")
    
    elif choice == '8':
        print("\n" + "="*80)
        print("Extracted Image Metadata (if available):")
        print("="*80 + "\n")
        found = False
        for i, page in enumerate(parsed["pages"]):
            images = page["metadata"].get("images", [])
            if images:
                found = True
                print(f"\n--- Page {i+1} ---")
                for img in images:
                    print(img)
        if not found:
            print("No image metadata found.")

if __name__ == "__main__":
    main()