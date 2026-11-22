import zipfile
p = r"C:\Users\user\Downloads\evidencia-s13\Entregable-S13-Extra-Carrito-Revisado.docx"
t = zipfile.ZipFile(p).read("word/document.xml").decode("utf-8")
for needle in ["85ec222", "scarita-dev", "sofia.carita@tecsup.edu.pe", "github.com/scarita-dev", "PENDIENTE DE PUBLICAR", "a853adc"]:
    print(needle, "->", needle in t)