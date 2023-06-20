import io
import re
from UnitextPython.pullenti.unitext.UnitextImage import UnitextImage
from UnitextPython.pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from UnitextPython.pullenti.unitext.UnitextService import UnitextService

doc = UnitextService.create_document("pres.docx")

buffer = io.StringIO()
doc.get_html(res=buffer)

with open(f"image.html", "w") as f:
    f.write(buffer.getvalue())
num_img = 0
for i in doc.content_items:
    print(type(i))
    # print(i.get_plaintext_string())
    tags_name = str(i.get_styled_fragment())
    # print(i.get_styled_fragment())
    if type(i) == UnitextPlaintext:
        print(i.get_plaintext_string())
    if "bold" in tags_name:
        pattern = r'\".*\"'
        match = re.search(pattern, tags_name)
        # if match:
        #     print(match.group()[1:-1])
        #     print(i.get_plaintext_string())

    if type(i) is UnitextImage:
        with open(f"image_{num_img}.jpg", "wb") as f:
            f.write(i.content)
        num_img = num_img + 1
