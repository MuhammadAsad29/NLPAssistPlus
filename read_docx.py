import zipfile
import xml.etree.ElementTree as ET
import sys
import os

def read_docx(file_path):
    try:
        # Try to use python-docx if available (though unlikely in standard env)
        import docx
        doc = docx.Document(file_path)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    except ImportError:
        # Fallback to manual XML parsing
        try:
            with zipfile.ZipFile(file_path) as document:
                xml_content = document.read('word/document.xml')
            
            tree = ET.fromstring(xml_content)
            
            # XML namespaces in word/document.xml
            namespaces = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            }
            
            text_content = []
            for p in tree.findall('.//w:p', namespaces):
                texts = [node.text for node in p.findall('.//w:t', namespaces) if node.text]
                if texts:
                    text_content.append(''.join(texts))
            
            return '\n'.join(text_content)
        except Exception as e:
            return f"Error reading docx manually: {str(e)}"

if __name__ == "__main__":
    file_path = "CCP NLP.docx"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
    else:
        content = read_docx(file_path)
        with open("doc_content.txt", "w", encoding="utf-8") as f:
            f.write(content)
        print("Done writing to doc_content.txt")
