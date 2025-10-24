"""PDF handling with robust content stream text replacement."""
import fitz  # PyMuPDF
import re
from pathlib import Path
from typing import Dict, List


class PDFHandler:
    """Handle PDF with direct content manipulation."""
    
    def __init__(self, template_path: str):
        self.template_path = template_path
    
    def generate_pdf(self, data: Dict[str, str], output_path: str) -> str:
        """Generate filled PDF using redaction and text insertion.
        
        Uses PyMuPDF's redaction API which is more reliable than overlay.
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        print(f"\n🔄 Generating PDF with redaction method...")
        print(f"📋 Data fields: {len(data)}\n")
        
        # Open template
        doc = fitz.open(self.template_path)
        replacements_made = 0
        
        # Process each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Collect all redactions for this page first
            redaction_list = []
            
            # For each data field
            for key, value in data.items():
                if not value:
                    value = ""
                
                # Try multiple placeholder formats
                placeholders = [
                    f"{{{key}}}",
                    f"{{{key.replace('fi', 'ﬁ')}}}",
                    f"{{{key.replace('fl', 'ﬂ')}}}",
                ]
                
                for placeholder in placeholders:
                    # Find all instances
                    instances = page.search_for(placeholder)
                    
                    for inst in instances:
                        # Add redaction annotation
                        redaction_list.append({
                            'rect': inst,
                            'placeholder': placeholder,
                            'value': str(value),
                            'key': key
                        })
            
            # Apply all redactions on this page
            for item in redaction_list:
                rect = item['rect']
                value = item['value']
                placeholder = item['placeholder']
                
                # Method 1: Use add_redact_annot + apply_redactions
                # This completely removes the old text
                page.add_redact_annot(rect, fill=(1, 1, 1))  # White fill
                
            # Apply all redactions at once
            page.apply_redactions()
            
            # Now insert new text at same positions using insert_text (simpler, more reliable)
            for item in redaction_list:
                rect = item['rect']
                value = item['value']
                placeholder = item['placeholder']
                
                # Calculate good font size based on rect height
                rect_height = rect.height
                fontsize = min(rect_height * 0.7, 10)  # Max 10pt, slightly smaller
                
                # Use insert_text at the baseline position (bottom-left of rect)
                # Position text at left edge and slightly above bottom
                point = fitz.Point(rect.x0, rect.y1 - 2)  # 2 points above bottom
                
                # Insert text directly (no text box constraints)
                page.insert_text(
                    point,
                    value,
                    fontsize=fontsize,
                    fontname="helv",
                    color=(0, 0, 0)
                )
                
                replacements_made += 1
                if len(value) > 30:
                    print(f"✅ Page {page_num + 1}: '{placeholder}' → '{value[:30]}...'")
                else:
                    print(f"✅ Page {page_num + 1}: '{placeholder}' → '{value}'")
        
        # Save with incremental=False to ensure changes are applied
        doc.save(output_path, garbage=4, deflate=True)
        doc.close()
        
        print(f"\n📄 PDF generated: {replacements_made} replacements")
        print(f"💾 Saved to: {output_path}\n")
        
        return output_path
    
    @staticmethod
    def get_placeholders_from_pdf(pdf_path: str) -> List[str]:
        """Extract all placeholders from PDF."""
        placeholders = set()
        
        try:
            doc = fitz.open(pdf_path)
            for page in doc.pages():
                text = page.get_text()
                # Find placeholders
                found = re.findall(r'\{([^}]+)\}', text)
                # Normalize ligatures
                for f in found:
                    normalized = f.replace('ﬁ', 'fi').replace('ﬂ', 'fl')
                    placeholders.add(normalized)
            doc.close()
        except Exception as e:
            print(f"Error reading PDF: {e}")
        
        return sorted(list(placeholders))
