import zipfile, xml.etree.ElementTree as ET
from pathlib import Path
p = Path(r"C:\Users\user\Downloads\evidencia-s13\Entregable-S13-Extra-Carrito-Revisado.docx")
z = zipfile.ZipFile(p)
print("partes:", z.namelist())
for name in z.namelist():
    ET.fromstring(z.read(name))
print("XML bien formado: OK")
ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
root = ET.fromstring(z.read("word/document.xml"))
paras = ["".join(t.text or "" for t in node.findall(".//w:t", ns)) for node in root.findall(".//w:p", ns)]
print("parrafos:", len(paras), "tablas:", len(root.findall(".//w:tbl", ns)))
texto = "\n".join(paras)
for needle in ["cinco fallos", "PRECIDO", "precio del cliente", "REPLAY_MISMATCH", "aceptar", "RECHAZADO", "0.845"]:
    print(needle, "->", needle.lower() in texto.lower() or needle in p.read_bytes().decode("latin1"))
print("longitud texto:", len(texto))