import requests, os, sys
from docx import Document

txtfile = sys.argv[1]
def chunkify_text(text, chunk_size=2735):
    chunks = []
    for word in text.split(" "):
        word = word.strip()
        if chunks and len(chunks[-1]) + len(word) > chunk_size:
            chunks.append("")
        if chunks:
            chunks[-1] += f" {word} "
        else:
            chunks.append(f"{word} ")
    return chunks                                             
with open(txtfile, "r") as file:
    input_text = file.read()
    url = 'http://www.7koko.com/api/tashkil/index.php'  # اضف هنا عنوان الموقع المحدد
       
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Origin': 'http://www.7koko.com',
    'Referer': 'http://www.7koko.com/apps/tashkil/index.php',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ar-EG,ar;q=0.9,en-us;q=0.8,en;q=0.7'
}

chunks = chunkify_text(input_text)
output_text = ""

for chunk in chunks:
    data = {
        'textArabic': chunk
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        output_text += response.text.strip()
        output_text = output_text.replace("\u064E", "").replace("\u064F", "").replace("\u0650", "").replace("\u0651", "").replace("\u0652", "").replace("?", "؟").replace(".", "")
        filename = os.path.splitext(file.name)[0]
        doc = Document()
        doc.add_paragraph(output_text)
        doc.save(f"{filename}.docx")


