from parser import CustomPDFParser
from pathlib import Path

def debug_pdf_text(pdf_path):
    """Extract and display raw text from PDF for debugging"""
    
    print("\n" + "="*80)
    print("🔍 PDF TEXT EXTRACTION DEBUG")
    print("="*80 + "\n")
    
    if not Path(pdf_path).exists():
        print(f"❌ Error: File not found at {pdf_path}")
        return
    
    print(f"📄 Processing: {pdf_path}\n")
    
    # Initialize parser
    parser = CustomPDFParser(
        extract_images=False,
        preserve_layout=True,
        remove_headers_footers=False,
        min_text_length=5
    )
    
    # Parse PDF
    try:
        parsed = parser.parse_pdf(pdf_path)
        
        print("="*80)
        print("📊 EXTRACTION SUMMARY")
        print("="*80)
        print(f"Total Pages: {parsed['total_pages']}")
        print(f"Processed Pages: {parsed['processed_pages']}")
        print(f"Total Words: {parsed['total_words']}")
        print(f"Total Characters: {len(parsed['full_text'])}")
        
        print("\n" + "="*80)
        print("📝 FULL TEXT (First 2000 characters)")
        print("="*80 + "\n")
        
        # Show first 2000 characters
        print(parsed['full_text'][:2000])
        
        if len(parsed['full_text']) > 2000:
            print(f"\n... [Text truncated - {len(parsed['full_text']) - 2000} more characters]")
        
        print("\n" + "="*80)
        print("📄 PAGE-BY-PAGE BREAKDOWN")
        print("="*80 + "\n")
        
        # Show first 3 pages in detail
        for i, page in enumerate(parsed['pages'][:3]):
            print(f"--- PAGE {i+1} ---")
            print(f"Word Count: {page['word_count']}")
            print(f"First 500 characters:")
            print(page['text'][:500])
            print(f"\n{'-'*40}\n")
        
        if len(parsed['pages']) > 3:
            print(f"... [{len(parsed['pages']) - 3} more pages not shown]")
        
        # Save full text to file
        output_file = "extracted_text.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(parsed['full_text'])
        
        print("\n" + "="*80)
        print(f"💾 Full text saved to: {output_file}")
        print("="*80 + "\n")
        
        print("💡 TIP: Open 'extracted_text.txt' to see the complete extracted text")
        print("💡 Use this to identify patterns for your credit card issuer")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("\n🔍 PDF Debug Tool - Extract Raw Text\n")
    pdf_path = input("Enter path to your PDF: ").strip().strip('"').strip("'")
    debug_pdf_text(pdf_path)

if __name__ == "__main__":
    main()