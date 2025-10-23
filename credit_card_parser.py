import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from parser import CustomPDFParser
import logging
import time

logger = logging.getLogger(__name__)

class CreditCardStatementParser:
    """
    Parser for extracting key data points from credit card statements.
    Supports multiple credit card issuers with pattern-based extraction.
    """
    
    def __init__(self):
        self.pdf_parser = CustomPDFParser(
            extract_images=False,
            preserve_layout=True,
            remove_headers_footers=False,
            min_text_length=5
        )
        
    def parse_statement(self, pdf_path: str) -> Dict[str, Any]:
        """
        Parse a credit card statement and extract key data points.
        
        Args:
            pdf_path: Path to the PDF statement file
            
        Returns:
            Dictionary containing extracted data points and metadata
        """
        try:
            # Parse the PDF
            parsed_data = self.pdf_parser.parse_pdf(pdf_path)
            full_text = parsed_data["full_text"]
            
            # Detect credit card issuer
            issuer = self._detect_issuer(full_text)
            
            # Extract 5 key data points
            extracted_data = {
                "issuer": issuer,
                "card_last_4_digits": self._extract_card_last_4(full_text),
                "statement_period": self._extract_statement_period(full_text),
                "total_amount_due": self._extract_total_amount_due(full_text),
                "payment_due_date": self._extract_payment_due_date(full_text),
                "transactions": self._extract_transactions(full_text),
                "raw_metadata": parsed_data["document_metadata"],
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"Error parsing statement: {e}")
            return {
                "error": str(e),
                "issuer": "Unknown",
                "extraction_timestamp": time.now().isoformat()
            }
    
    def _detect_issuer(self, text: str) -> str:
        """Detect credit card issuer from statement text."""
        text_lower = text.lower()
        
        issuers = {
            "American Express": ["american express", "amex"],
            "Chase": ["chase", "jpmorgan chase"],
            "Citibank": ["citibank", "citi card"],
            "Capital One": ["capital one"],
            "Bank of America": ["bank of america", "bankamericard"]
        }
        
        for issuer, keywords in issuers.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return issuer
        
        return "Unknown"
    
    def _extract_card_last_4(self, text: str) -> Optional[str]:
        """Extract last 4 digits of credit card number."""
        patterns = [
            r"(?:card|account)\s*(?:number|ending|#)?\s*[:\s]*(?:x+|\*+)?(\d{4})",
            r"(\d{4})\s*$",  # Often at end of line
            r"x{4,}\s*(\d{4})",
            r"\*{4,}\s*(\d{4})"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_statement_period(self, text: str) -> Optional[str]:
        """Extract billing/statement period."""
        patterns = [
            r"(?:statement|billing)\s+(?:period|cycle|date)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+(?:to|through|-)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
            r"(?:from|period)[:\s]+(\w+\s+\d{1,2},?\s+\d{4})\s+(?:to|through)\s+(\w+\s+\d{1,2},?\s+\d{4})"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)} to {match.group(2)}"
        
        return None
    
    def _extract_total_amount_due(self, text: str) -> Optional[str]:
        """Extract total amount due or new balance."""
        patterns = [
            r"(?:total|new)\s+(?:amount\s+)?(?:due|balance)[:\s]+\$?([\d,]+\.\d{2})",
            r"(?:payment\s+due)[:\s]+\$?([\d,]+\.\d{2})",
            r"(?:balance)[:\s]+\$?([\d,]+\.\d{2})"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"${match.group(1)}"
        
        return None
    
    def _extract_payment_due_date(self, text: str) -> Optional[str]:
        """Extract payment due date."""
        patterns = [
            r"(?:payment\s+)?due\s+(?:date|by)[:\s]+(\w+\s+\d{1,2},?\s+\d{4})",
            r"(?:payment\s+)?due\s+(?:date|by)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
            r"(?:pay\s+by)[:\s]+(\w+\s+\d{1,2},?\s+\d{4})"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_transactions(self, text: str) -> List[Dict[str, str]]:
        """Extract transaction details (sample extraction - first 5 transactions)."""
        transactions = []
        
        # Pattern for date, description, amount
        pattern = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+([A-Za-z0-9\s\*\-]+?)\s+(\$?[\d,]+\.\d{2})"
        
        matches = re.findall(pattern, text, re.MULTILINE)
        
        for match in matches[:5]:  # Limit to first 5 transactions
            transactions.append({
                "date": match[0],
                "description": match[1].strip(),
                "amount": match[2] if match[2].startswith('$') else f"${match[2]}"
            })
        
        return transactions if transactions else []