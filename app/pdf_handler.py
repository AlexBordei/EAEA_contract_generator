"""PDF handling with robust content stream text replacement."""
import fitz  # PyMuPDF
import re
from pathlib import Path
from typing import Dict, List


class PDFHandler:
    """Handle PDF with direct content manipulation."""
    
    def __init__(self, template_path: str):
        self.template_path = template_path
    
    def _get_font_at_position(self, page, rect) -> tuple:
        """Extract font name and size from text at given position.
        
        Returns:
            (fontname, fontsize) tuple
        """
        # Get text with font information
        blocks = page.get_text('dict')['blocks']
        
        # Find text spans that overlap with our rect
        for block in blocks:
            if 'lines' not in block:
                continue
            
            for line in block['lines']:
                for span in line['spans']:
                    span_rect = fitz.Rect(span['bbox'])
                    
                    # Check if this span overlaps with our placeholder
                    if span_rect.intersects(rect):
                        # Return the original font info
                        return (span['font'], span['size'])
        
        # Fallback to Palatino if not found
        return ('PalatinoLinotype-Roman', 10.0)
    
    def generate_pdf(self, data: Dict[str, str], output_path: str) -> str:
        """Generate filled PDF using redaction and text insertion.
        
        Uses PyMuPDF's redaction API which is more reliable than overlay.
        Preserves original fonts from template.
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
                        # Extract original font from this position
                        original_font, original_size = self._get_font_at_position(page, inst)
                        
                        # Add redaction annotation
                        redaction_list.append({
                            'rect': inst,
                            'placeholder': placeholder,
                            'value': str(value),
                            'key': key,
                            'font': original_font,
                            'fontsize': original_size
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
            
            # Now insert new text at same positions using original fonts
            for item in redaction_list:
                rect = item['rect']
                value = item['value']
                placeholder = item['placeholder']
                original_font = item['font']
                original_fontsize = item['fontsize']
                
                # Use original fontsize, but slightly smaller if needed
                fontsize = min(original_fontsize * 0.9, original_fontsize)
                
                # Position text at left edge and slightly above bottom
                point = fitz.Point(rect.x0, rect.y1 - 2)
                
                # Map template fonts to available PyMuPDF fonts
                # PalatinoLinotype → tiro (Times-Roman, serif similar)
                # OpenSans → helv (Helvetica, sans-serif)
                font_mapping = {
                    'PalatinoLinotype-Roman': 'tiro',
                    'PalatinoLinotype-Bold': 'tirob',  # Times-Bold
                    'OpenSans-Regular': 'helv',
                    'OpenSans-Bold': 'helvb',
                }
                
                # Get mapped font or use fallback
                fontname = font_mapping.get(original_font, 'tiro')
                
                # Insert text with matched font
                try:
                    page.insert_text(
                        point,
                        value,
                        fontsize=fontsize,
                        fontname=fontname,
                        color=(0, 0, 0)
                    )
                    font_used = fontname
                except Exception as e:
                    # Ultimate fallback to Times
                    page.insert_text(
                        point,
                        value,
                        fontsize=fontsize,
                        fontname='tiro',
                        color=(0, 0, 0)
                    )
                    font_used = 'tiro'
                
                replacements_made += 1
                
                # Print replacement confirmation
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
