"""PDF handling - Find and replace text with white rectangle overlay method."""
import fitz  # PyMuPDF
import re
from pathlib import Path
from typing import Dict, List


class PDFHandler:
    """Handle PDF extraction and generation preserving original formatting."""
    
    def __init__(self, template_path: str):
        self.template_path = template_path
    
    def generate_pdf(self, data: Dict[str, str], output_path: str) -> str:
        """Generate filled PDF by finding placeholders and overlaying replacements.
        
        This method:
        1. Opens the template PDF (keeps original formatting!)
        2. Finds each placeholder text location
        3. Draws white rectangle over placeholder
        4. Writes replacement text at same location
        5. Saves the modified PDF
        """
        # Create output directory
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        print(f"\n🔄 Generating PDF with overlay method...")
        print(f"📋 Data fields: {len(data)}\n")
        
        # Open the template
        doc = fitz.open(self.template_path)
        
        replacements_made = 0
        
        # Process each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # For each data field
            for key, value in data.items():
                # Handle empty values
                if not value:
                    value = ""
                
                # Try multiple placeholder formats (with ligatures)
                placeholders = [
                    f"{{{key}}}",
                    f"{{{key.replace('fi', 'ﬁ')}}}",  # fi ligature
                    f"{{{key.replace('fl', 'ﬂ')}}}",  # fl ligature
                ]
                
                for placeholder in placeholders:
                    # Search for this placeholder on the page
                    text_instances = page.search_for(placeholder)
                    
                    if not text_instances:
                        continue
                    
                    # Found placeholder(s)
                    for rect in text_instances:
                        # Expand rect significantly for long text
                        expanded_rect = fitz.Rect(
                            rect.x0 - 2,
                            rect.y0 - 2,
                            rect.x0 + 500,  # Very wide for long addresses
                            rect.y1 + 2
                        )
                        
                        # Draw white rectangle to cover placeholder
                        page.draw_rect(expanded_rect, color=(1, 1, 1), fill=(1, 1, 1))
                        
                        # Insert replacement text with dynamic font sizing
                        text_rect = fitz.Rect(
                            rect.x0,
                            rect.y0 - 2,
                            rect.x0 + 500,
                            rect.y1 + 2
                        )
                        
                        # Try decreasing font sizes until text fits
                        success = False
                        for fontsize in [11, 10, 9, 8, 7, 6]:
                            rc = page.insert_textbox(
                                text_rect,
                                str(value),
                                fontname="helv",
                                fontsize=fontsize,
                                color=(0, 0, 0),  # Black
                                align=fitz.TEXT_ALIGN_LEFT
                            )
                            
                            if rc >= 0:  # 0 = OK, >0 = text fits
                                success = True
                                replacements_made += 1
                                if fontsize < 10:
                                    print(f"✅ Page {page_num + 1}: '{placeholder}' → '{value}' (font {fontsize})")
                                else:
                                    print(f"✅ Page {page_num + 1}: '{placeholder}' → '{value}'")
                                break
                        
                        if not success:
                            print(f"⚠️  Page {page_num + 1}: Could not fit '{value}'")
        
        # Save the modified PDF
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()
        
        print(f"\n📄 PDF generated: {replacements_made} replacements made")
        print(f"💾 Output: {output_path}\n")
        
        return output_path
    
    @staticmethod
    def get_placeholders_from_pdf(pdf_path: str) -> List[str]:
        """Extract placeholders from PDF."""
        placeholders = set()
        
        try:
            doc = fitz.open(pdf_path)
            for page in doc.pages:
                text = page.get_text()
                # Find all placeholders
                found = re.findall(r'\{([^}]+)\}', text)
                placeholders.update(found)
            doc.close()
        except Exception as e:
            print(f"Error reading PDF: {e}")
        
        return sorted(list(placeholders))
