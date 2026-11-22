# -*- coding: utf-8 -*-
"""Build the S13 extra deliverable as a .docx using only the standard library."""
from html import escape
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

OUT = Path(r"C:\Users\user\Downloads\evidencia-s13\Entregable-S13-Extra-Carrito-Revisado.docx")


def e(text):
    return escape(str(text), quote=False)


def runs(text, bold=False, code=False):
    if code:
        rpr = ('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
               '<w:sz w:val="17"/><w:color w:val="1F3864"/>')
    elif bold:
        rpr = '<w:b/><w:sz w:val="20"/>'
    else:
        rpr = '<w:sz w:val="20"/>'
    parts = []
    for i, line in enumerate(str(text).split("\n")):
        if i:
            parts.append("<w:br/>")
        parts.append(f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{e(line)}</w:t></w:r>')
    return "".join(parts)


def p(text="", style=None, bold=False, code=False):
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{ppr}{runs(text, bold, code)}</w:p>"


def cell(text, bold=False, code=False, shade=None):
    shd = f'<w:shd w:fill="{shade}"/>' if shade else ""
    tcpr = f"<w:tcPr>{shd}<w:vAlign w:val=\"center\"/></w:tcPr>"
    return f"<w:tc>{tcpr}<w:p>{runs(text, bold, code)}</w:p></w:tc>"


def table(headers, rows, code_cols=()):
    out = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
           '<w:tblW w:w="9360" w:type="dxa"/>'
           '<w:tblLayout w:type="autofit"/></w:tblPr>']
    out.append("<w:tr>" + "".join(cell(h, bold=True, shade="D9E2F3") for h in headers) + "</w:tr>")
    for row in rows:
        out.append("<w:tr>" + "".join(
            cell(v, code=(i in code_cols)) for i, v in enumerate(row)) + "</w:tr>")
    out.append("</w:tbl>")
    out.append(p(""))
    return "".join(out)


def bullets(items):
    return "".join(p("•  " + item) for item in items)


B = []
add = B.append

add(p("Entrega del laboratorio extra de la semana 13", "Title"))
add(p("El carrito revisado por pruebas: dinero exacto, existencias, cupones y auditoría sin pantalla", "Heading2"))
add(p("Michael Montgomery Rosell  |  Desarrollo de Aplicaciones Empresariales  |  4-C24-A", ))
add(p("Periodo 2026-2  |  Semana 13  |  Sección A  |  Fecha: 21 de noviembre de 2026"))
add(p("Nombre del alumno: ______________________________    Integrantes: ______________________________"))
add(p(""))

add(p("1. Entregable y estado final", "Heading1"))
add(p("Trabajo realizado bajo AGENTS.md: solo se editaron shop/cart_team.py y shop/cart_ai.py; un método por "
      "turno, con su prueba y su commit. No se tocaron pruebas, reglas, auditoría, compuerta, carritos ni "
      "configuración; no se ejecutó migrate, seed_shop ni pagos contra la base."))
add(table(
    ["Concepto", "Resultado"],
    [
        ["Carrito del equipo", "67/67 pruebas; compuerta ACEPTAR, código de salida 0"],
        ["Carrito de la IA (arreglado)", "67/67 pruebas; compuerta ACEPTAR, código de salida 0"],
        ["Commit base (estado original de la IA)", "85ec222 baseline: plantilla original con carrito IA sin arreglar"],
        ["Commits del trabajo", "27 commits posteriores (11 del equipo y 16 de la IA), uno por método"],
        ["Autor de los commits", "Los 28 commits tienen como autor y committer a scarita-dev "
                                 "<sofia.carita@tecsup.edu.pe>, la identidad real de Git del alumno."],
        ["Repositorio", "https://github.com/scarita-dev/dae-s13-carrito-con-ia-main.git (rama main)"],
    ]))
add(p("La compuerta en verde es condición necesaria, no suficiente: las cuatro preguntas de revisión las responde "
      "una persona con la línea de código que lo demuestra (sección 5)."))

add(p("2. Reglas de la tienda y arquitectura (pasos 1-2)", "Heading1"))
add(table(
    ["Regla", "En mis palabras", "Dónde se aplica"],
    [
        ["Dinero", "Decimal de principio a fin; al céntimo, mitad hacia arriba (0,005 → 0,01).", "money() en domain.py; money()/fmt() en los carritos"],
        ["Precio", "Lo fija el catálogo; la petición nunca trae precio.", "lines() y add_from_payload()"],
        ["Cantidad", "Entero ≥ 1. Quitar de más borra la línea; jamás cantidad negativa.", "_check_qty / add / remove"],
        ["Existencias", "Lo ya agregado + lo nuevo ≤ stock; se vuelve a comprobar al pagar; stock ≥ 0.", "add() y checkout()"],
        ["Cupón", "Uno solo; BIENVENIDA10 = 10 %, MENOS20 = S/20 tope; aplicar otro reemplaza.", "apply_coupon() y discount()"],
        ["Totales", "subtotal; descuento; IGV = 18 % de (subtotal − descuento); total = base + IGV, cada parte redondeada.", "subtotal()/discount()/igv()/total()"],
    ]))
add(bullets([
    "El carrito trabaja con un catálogo de datos puros (Product es un dataclass) para que la lógica sea "
    "determinista y no dependa de la base: las pruebas usan catalog_data() y la auditoría usa --catalogo-fijo.",
    "_qty guarda solo la cantidad por SKU en orden de inserción; el precio no se guarda porque el catálogo "
    "es la única fuente y un precio en sesión podría ser manipulado o quedar obsoleto.",
    "shop/impl.py elige el módulo con SHOP_MODE: team → cart_team, ai → cart_ai, solutions → solución del "
    "docente (no disponible en esta copia). Así las mismas pruebas y la API juzgan implementaciones distintas.",
    "Al inicio, 7 de 67 pruebas pasaban: las de la auditoría pura (test_audit sin replay), que no dependen "
    "del carrito, sino de audit.py y del catálogo fijo. Las dos de replay fallaban con REPLAY_UNAVAILABLE.",
]))

add(p("3. Carrito del equipo (pasos 3-9)", "Heading1"))
add(table(
    ["Método", "Cambio", "Prueba"],
    [
        ["add", "Valida entero ≥ 1, SKU del catálogo y stock = ya agregado + nuevo; sin mutar si falla.", "test_lines, test_stock"],
        ["remove", "Quita la línea o unidades; llega a cero → borra; nunca negativo.", "test_lines"],
        ["lines", "Line(sku, name, catalog price, qty) en orden de inserción.", "test_lines"],
        ["apply_coupon", "Normaliza y reemplaza: un cupón por carrito.", "test_coupons"],
        ["subtotal / discount / igv / total", "Decimal + money(): mitad hacia arriba; total = suma de partes redondeadas.", "test_totals"],
        ["summary", "Cadenas de dos decimales vía fmt().", "test_totals"],
        ["checkout", "Rechequea todas las líneas, descuenta stock, vacía carrito y cupón.", "test_stock"],
        ["add_from_payload", "Exige dict con sku de texto; ignora price/unit_price del cliente.", "test_api"],
    ]))
add(p("Resultado: python manage.py test → Ran 67 tests, OK (exit 0). Cada archivo de prueba se corrió tras su "
      "método (evidencia 10-20 en la carpeta de evidencias)."))
add(bullets([
    "remove borra la línea al llegar a cero porque una línea con qty=0 no es una línea; si quedara qty negativo, "
    "line.total sería negativo y el subtotal, el descuento y el total saldrían mal (precio × negativo).",
    "checkout vuelve a comprobar existencias porque entre add y pagar otro cliente puede comprar las mismas "
    "unidades. Si dos clientes pagan las últimas unidades a la vez, el rechequeo y la transacción atómica de "
    "views.py hacen que el segundo reciba 409 y conserve su carrito; la restricción CHECK de la BD es la última defensa.",
]))
add(p("Experimento de dinero (evidencia 36-decimal-experimento.txt):"))
add(p("0.1 + 0.2      = 0.30000000000000004\n"
      "Decimal suma   = 0.3\n"
      "round(0.845,2) = 0.84\n"
      "quantize half  = 0.85\n"
      "repr float     = 0.845", code=True))
add(p("Un float no puede guardar 0,845: es binario y 0,845 no es exacto; además round() usa half-even, por eso "
      "da 0,84. La tienda usa ROUND_HALF_UP con Decimal, por eso 0,845 → 0,85."))
add(p("Cálculo a mano del mousepad con BIENVENIDA10: subtotal 8,45; descuento = money(8,45×10/100) = money(0,845) "
      "= 0,85; IGV = money((8,45−0,85)×0,18) = money(1,368) = 1,37; total = 7,60 + 1,37 = 8,97. Coincide con "
      "test_the_discount_rounds_half_up."))

add(p("4. Duelo y clasificación de los cinco fallos de la IA (pasos 10-11)", "Heading1"))
add(p("Antes de los arreglos: python manage.py duelo →"))
add(p("team       tu carrito                 pasan   7   fallan  60\n"
      "ai         el carrito de la IA        pasan  49   fallan  18", code=True))
add(p("El detalle de duelo --modo ai agrupa los 18 fallos: API 6, auditoría 1, cupones 2, líneas 1, "
      "existencias 4, totales 4. Tras los arreglos, ambos carritos dan 67/67."))
add(table(
    ["#", "Fallo y líneas del original", "Prueba que lo detecta y mensaje", "Causa", "¿Se ve a mano?", "Tipo"],
    [
        ["1", "Redondeo con flotantes: cart_ai.py:14 IGV=0.18; :17-18 _money con round(); :84 float(l.unit_price); "
              ":88-94 acumulador 0.0 y float(amount); :104 IGV float; :107-108 total con descuento crudo.",
         "test_igv_rounds_half_up: Decimal('452.2') != Decimal('452.21'); test_the_discount_rounds_half_up: "
         "0.84 != 0.85; test_a_discount_of_one_and_a_half_cents: 0.1 != 0.11; "
         "test_total_is_the_sum_of_its_rounded_parts: 71.63 != 71.64; replay de 06: REPLAY_MISMATCH.",
         "Float binario + round() half-even + total calculado con descuento sin redondear.",
         "Sí, en importes con 0,005 (0,84 en vez de 0,85); discreto pero cobra de menos.", "Dinero"],
        ["2", "Precio tomado del cliente: cart_ai.py:45 add(price=None); :53 guarda Decimal(str(price)) en "
              "_prices; :73 usa _prices[sku]; :136-139 add_from_payload reenvía payload.get('price').",
         "test_the_price_comes_from_the_catalog_not_from_the_client: '0.01' != '2499.90'; "
         "test_a_negative_price_from_the_client_changes_nothing_either: '-100.00' != '2499.90'.",
         "El carrito confía en un campo no fiable del cuerpo HTTP y lo persiste en sesión (:30,:34,:41).",
         "NO se ve a mano: solo con la API (o auditando el carrito 02).", "SEGURIDAD / solo API"],
        ["3", "Existencias que no cuentan lo ya agregado: cart_ai.py:50 'if qty > product.stock'; "
              "checkout :128-129 descuenta sin rechequear.",
         "test_the_stock_counts_what_is_already_in_the_cart y test_two_adds_cannot_get_around_the_stock: "
         "OutOfStock not raised; test_the_stock_is_never_negative_after_any_sequence: -2; "
         "test_checkout_checks_the_stock_again: OutOfStock not raised; API 201 != 409; "
         "API stock cambiado → IntegrityError CHECK constraint failed: stock.",
         "Compara solo la cantidad nueva contra el stock y checkout confía en add.",
         "Sí: dos add seguidos o dos clientes pagando las últimas unidades.", "Stock"],
        ["4", "Cantidad negativa al quitar: cart_ai.py:63-66, '-=' y borra solo si es exactamente 0.",
         "test_remove_more_than_there_is_never_leaves_a_negative_quantity: -3 != 0; API "
         "test_remove_more_than_there_is_leaves_no_negative_line: queda qty -3 y line_total -119.70.",
         "Quitar más de lo que hay deja qty negativo; el total se vuelve negativo.",
         "Sí: quitar de más o doble clic en quitar.", "Cantidad"],
        ["5", "Descuento acumulado dos veces: cart_ai.py:81 _coupons.append(code); :89-94 suma todos los cupones.",
         "test_applying_the_same_coupon_twice_discounts_once: 37.8 != 18.90; "
         "test_a_second_coupon_replaces_the_first: 38.9 != 20.00; API "
         "test_the_coupon_is_applied_once_even_if_the_client_repeats_it: '37.80' != '18.90'.",
         "La lista acumula cupones y el descuento suma todos en vez de reemplazar.",
         "Sí: doble clic en «Aplicar cupón» o reintento de red.", "Idempotencia"],
    ],
    code_cols=()))

add(p("5. Cuatro preguntas de revisión aplicadas al carrito de la IA ya arreglado", "Heading1"))
add(table(
    ["Pregunta", "Respuesta con la línea que lo demuestra"],
    [
        ["1. ¿Todo el dinero es Decimal de principio a fin, con redondeo hacia arriba en la mitad?",
         "SÍ. cart_ai.py:17-18 '_money → money(value)'; :81 suma con Decimal('0'); :88 'money(subtotal * amount / 100)'; "
         ":100 'money((self.subtotal() - self.discount()) * IGV_RATE)'; :103 'money(self.subtotal() - self.discount()) + self.igv()'. "
         "No queda ningún float: IGV_RATE y los importes de COUPONS vienen de domain.py."],
        ["2. ¿El servidor es la única fuente del precio?",
         "SÍ. cart_ai.py:42 'def add(self, sku, qty=1)' ya no acepta price; :70 'Line(..., self._catalog[sku].price, qty)'; "
         ":133-136 add_from_payload solo pasa sku y qty; :33 y :39 el estado no guarda ni carga precios. "
         "No hay ninguna línea que lea price ni unit_price de la petición."],
        ["3. ¿Cada regla de cantidad y existencias se cumple con cualquier secuencia?",
         "SÍ. cart_ai.py:47-50 'in_cart + qty > product.stock' con mutación después del chequeo; :58-63 remove usa "
         "'remaining <= 0' y borra la línea; :122-127 checkout rechequea todas las líneas antes de descontar y "
         "solo luego limpia el carrito. Pruebas: dos add seguidos, quitar de más y stock cambiado antes de pagar."],
        ["4. ¿Repetir una acción da el mismo resultado?",
         "SÍ. cart_ai.py:78 'self._coupons = [normalized]' reemplaza; :85 'for code in self._coupons[:1]' aplica solo "
         "el primero aunque vengan varios del estado; :112 summary muestra el último cupón guardado. "
         "Doble clic en aplicar cupón o reintento de red dejan un descuento, no dos."],
    ]))

add(p("6. Arreglo del carrito de la IA, fallo por fallo (paso 13)", "Heading1"))
add(p("Estado original guardado en 85ec222. Tras cada método se corrió $env:SHOP_MODE='ai'; python manage.py test. "
      "La compuerta se revisó en tres hitos: antes 18 fallos / RECHAZAR (1); tras el redondeo 16 / RECHAZAR (1); "
      "al terminar 0 / ACEPTAR (0). En la bitácora de la sección 10, 'fallos' cuenta los tests con FAIL o ERROR "
      "de la suite completa; cuando se indica 'archivo', cuenta solo el archivo de prueba corrido en ese turno."))
add(table(
    ["Turnos (método tocado)", "Fallos antes → después", "Commit"],
    [
        ["_subtotal, _discount, IGV→IGV_RATE, _money (redondeo base)", "18 → 16", "645a8d9, 18389b5, fb96ca7, 2002d28"],
        ["add, add_from_payload, lines, to_state, from_state (precio del cliente)", "16 → 13", "0964e51, 59c52dd, 4e09278, 2adb0e5, 154d631"],
        ["remove (cantidad negativa)", "13 → 8", "3be2f6d"],
        ["add (existencias), checkout (rechequeo)", "8 → 6", "0964e51, e2d45de"],
        ["igv y total con partes redondeadas", "6 → 3", "8fd65e6, 04cd072"],
        ["apply_coupon y _discount (cupón único)", "3 → 0", "e29c9bd, 4c8f387"],
        ["__init__ (limpieza de _prices)", "0 → 0", "f5bd3f8"],
    ]))
add(p("Nota: algunos turnos intermedios elevaron temporalmente los errores (por ejemplo, al quitar el parámetro "
      "price antes de cambiar add_from_payload). Eso es esperado en un cambio incremental: cada commit es pequeño "
      "y se mide, y el estado final de cada grupo deja menos fallos que el anterior. Ningún arreglo quedó pendiente."))

add(p("7. Auditoría de los seis carritos (pasos 14-15)", "Heading1"))
add(p("Comandos: $env:SHOP_MODE='ai'; python manage.py audit_cart carts/*.json --catalogo-fijo  (y con --replay; "
      "en PowerShell se pasa la lista de rutas desde Get-ChildItem). Resultado con la IA ya arreglada:"))
add(table(
    ["Carrito", "Hallazgo declarado", "REPLAY antes", "REPLAY después", "Fallo relacionado"],
    [
        ["01-correcto", "sin hallazgos (OK)", "sin REPLAY_*", "sin REPLAY_*; totalles correctos", "ninguno"],
        ["02-precio-del-cliente", "PRICE_MISMATCH LAP-01 0.01 vs 2499.90 + 3 TOTAL_MISMATCH", "sin REPLAY_*", "sin REPLAY_*; la implementación ignora 0.01", "#2 precio del cliente"],
        ["03-stock", "OVER_STOCK PAD-01: 4 > 2", "REPLAY_REJECTED", "REPLAY_REJECTED: 'pides 4, ya hay 0 y quedan 2'", "#3 existencias"],
        ["04-cantidad-negativa", "BAD_QTY MOU-01 -3 + 3 TOTAL_MISMATCH", "REPLAY_REJECTED", "REPLAY_REJECTED: 'Cantidad no válida: -3'", "#4 cantidad negativa"],
        ["05-cupon-doble", "MULTIPLE_COUPONS + 3 TOTAL_MISMATCH (37.80 vs 18.90)", "REPLAY_MISMATCH en discount, igv y total", "sin REPLAY_*; descuento 18.90", "#5 cupón doble"],
        ["06-redondeo", "TOTAL_MISMATCH discount 0.84 vs 0.85", "REPLAY_MISMATCH discount 0.84 vs 0.85", "sin REPLAY_*; descuento 0.85", "#1 redondeo float"],
    ]))
add(bullets([
    "TOTAL_MISMATCH compara lo que el carrito DECLARA contra reference_totals(): el carrito mintió o calculó mal "
    "al generar el JSON. REPLAY_MISMATCH compara lo que la IMPLEMENTACIÓN ACTIVA calcula al reconstruir el mismo "
    "carrito contra esa misma fórmula: el carrito declarado puede estar bien y aun así el código estar mal.",
    "Con --json --strict la auditoría devuelve un objeto {mode, carts:[{file, ok, findings:[{code, detail}]}]} y "
    "termina con código 1 porque 5 carritos tienen hallazgos declarados; sin --strict termina con 0. Un agente "
    "leería carts[].ok y findings[].code para decidir, y el código de salida para saber si debe parar.",
    "La auditoría NO sustituye las reglas del servidor: avisa DESPUÉS de que el cobro ocurrió (o al revisar un "
    "carrito ajeno). La regla en add()/checkout() impide el cobro ANTES; por eso ambas se complementan.",
]))

add(p("8. Compuerta antes y después (paso 16)", "Heading1"))
add(table(
    ["Momento", "Modo", "Pruebas", "Carritos", "verdict", "exit"],
    [
        ["Antes", "team", "7 pasan / 60 fallan", "6 sin_implementar", "rechazar", "1"],
        ["Antes", "ai", "49 pasan / 18 fallan", "4 ok, 05 y 06 calcula_distinto", "rechazar", "1"],
        ["Después", "team", "67 pasan / 0 fallan", "6 ok", "aceptar", "0"],
        ["Después", "ai", "67 pasan / 0 fallan", "6 ok", "aceptar", "0"],
    ]))
add(p("Salida de python manage.py gate --modo ai --json (después):"))
add(p('{\n  "mode": "ai",\n  "tests": {"total": 67, "passed": 67, "failed": 0, "failing": []},\n'
      '  "carts": [\n    {"file": "01-correcto.json", "expected": "totales", "result": "ok"},\n'
      '    {"file": "02-precio-del-cliente.json", "expected": "totales", "result": "ok"},\n'
      '    {"file": "03-stock.json", "expected": "rechazar", "result": "ok"},\n'
      '    {"file": "04-cantidad-negativa.json", "expected": "rechazar", "result": "ok"},\n'
      '    {"file": "05-cupon-doble.json", "expected": "totales", "result": "ok"},\n'
      '    {"file": "06-redondeo.json", "expected": "totales", "result": "ok"}\n  ],\n'
      '  "verdict": "aceptar",\n  "exit_code": 0\n}', code=True))
add(bullets([
    "Un agente leería verdict y exit_code para decidir; tests.failed y tests.failing para localizar el problema; "
    "y carts[].expected frente a carts[].result para ver si rechaza lo que debe y calcula lo que debe.",
    "Los carritos 03 y 04 DEBEN ser rechazados: tienen OVER_STOCK y BAD_QTY, que están en MUST_REJECT. Una "
    "implementación correcta lanza OutOfStock / InvalidQuantity en el replay; si los aceptara, la compuerta "
    "diría 'acepta_lo_que_debia_rechazar' y daría código 1, aunque las pruebas pasaran.",
    "El replay NO detecta el fallo del precio del cliente: audit.py reconstruye con cart.add(sku, qty), sin "
    "enviar price. Por eso el carrito 02 daba 'ok' en la compuerta de la IA original. Lo detectan las pruebas "
    "test_the_price_comes_from_the_catalog_not_from_the_client y test_a_negative_price...; la compuerta lo "
    "convierte en rechazo a través de tests.failed → verdict. La auditoría declarada sí muestra PRICE_MISMATCH, "
    "pero eso habla del JSON del carrito, no del código.",
]))

add(p("9. Uso de IA y diff de un rechazo (pasos 17-18)", "Heading1"))
add(p("Todo el trabajo se originó en un único pedido del usuario en este turno; se desglosa por pedido/acción "
      "para que la tabla cumpla con la guía."))
add(table(
    ["Se pidió", "Qué respondió el agente", "Aceptado / rechazado y por qué", "Evidencia"],
    [
        ["Entregar el laboratorio completo bajo AGENTS.md, sin tocar pruebas ni reglas.",
         "Implementó 11 métodos del carrito del equipo, clasificó 5 fallos de la IA, corrigió 16 métodos de la IA "
         "y capturó pruebas, auditoría y compuerta.",
         "ACEPTADO: compuerta team y ai en aceptar/código 0 y 67/67 pruebas; cuatro preguntas respondidas con línea.",
         "01, 02, 21, 22, 33; bitácora 10-20 y 32."],
        ["Arreglar la IA un fallo cada vez y medir antes/después.",
         "16 commits atómicos; fallos 18 → 16 → 13 → 9 → 8 → 0.",
         "ACEPTADO: ningún arreglo quedó pendiente; toda la suite en verde.",
         "32-gate-ai-tras-redondeo.json.txt y 33-gate-ai-despues.json.txt."],
        ["Proponer un cambio para revisar con el contrato (paso 17).",
         "Propuso añadir en add_from_payload: client_price = payload.get(\"price\") para 'validar' el cuerpo, "
         "sin usarlo en el cálculo.",
         "RECHAZADO: la compuerta lo aceptó (aceptar, 0) pero la pregunta 2 prohíbe toda línea que lea price de "
         "la petición. Se restauró el archivo; la compuerta sigue en 0.",
         "40-gate-propuesta-rechazada.json.txt, 41-diff-rechazo.patch, 42-gate-tras-rechazo.json.txt."],
    ]))
add(p("Diff del rechazo (evidencia 41-diff-rechazo.patch):"))
add(p("diff --git a/shop/cart_team.py b/shop/cart_team.py\n"
      "@@ -144,4 +144,5 @@ def add_from_payload(cart, payload):\n"
      '     """Translate an untrusted request body into a cart.add call; the catalog owns the price."""\n'
      '     if not isinstance(payload, dict) or not isinstance(payload.get("sku"), str):\n'
      '         raise CartError("El cuerpo debe ser un objeto con un «sku» de texto")\n'
      '+    client_price = payload.get("price")  # PROPUESTA RECHAZADA: se lee para "validar" el cuerpo\n'
      '     cart.add(payload["sku"], payload.get("qty", 1))', code=True))
add(p("Veredicto de la compuerta para esa propuesta: tests.failed = 0, verdict = 'aceptar', exit_code = 0. "
      "Decisión humana: RECHAZAR por la pregunta 2. Es el caso que la guía pide: la compuerta no sabe lo que "
      "las pruebas no preguntan (aquí el precio se lee pero se descarta, así que el total sigue bien)."))

add(p("10. Bitácora de turnos", "Heading1"))
add(table(
    ["Método tocado", "Prueba corrida", "Resultado de ese turno", "Compuerta"],
    [
        ["team.add", "test_lines + test_stock (25)", "19 errores; 6 pasan", "(inicio: rechazar 1)"],
        ["team.remove", "test_lines (15)", "9 errores; 6 pasan", "—"],
        ["team.lines", "test_lines (15)", "3 errores; 12 pasan", "—"],
        ["team.apply_coupon", "test_coupons (9)", "9 errores (dependen de subtotal)", "—"],
        ["team.subtotal", "test_totals (10)", "9 errores; 1 pasa", "—"],
        ["team.discount", "test_coupons (9)", "6 errores; 3 pasan", "—"],
        ["team.igv", "test_totals (10)", "8 errores; 2 pasan", "—"],
        ["team.total", "test_totals (10)", "2 errores; 8 pasan", "—"],
        ["team.summary", "test_totals + test_audit (19)", "OK", "—"],
        ["team.checkout", "test_stock (10)", "OK", "—"],
        ["team.add_from_payload", "test_api (14)", "OK", "aceptar (0)"],
        ["ai._subtotal", "suite ai (67)", "38 fallos (transitorio)", "—"],
        ["ai._discount", "suite ai (67)", "36 fallos (transitorio)", "—"],
        ["ai.igv + IGV_RATE", "suite ai (67)", "18 fallos", "—"],
        ["ai._money", "suite ai (67)", "16 fallos", "rechazar (1), hito redondeo"],
        ["ai.add (precio + stock)", "suite ai (67)", "44 fallos (transitorio)", "—"],
        ["ai.add_from_payload", "suite ai (67)", "41 fallos (transitorio)", "—"],
        ["ai.lines", "suite ai (67)", "13 fallos", "—"],
        ["ai.to_state", "suite ai (67)", "13 fallos", "—"],
        ["ai.from_state", "suite ai (67)", "13 fallos", "—"],
        ["ai.remove", "suite ai (67)", "8 fallos", "—"],
        ["ai.checkout", "suite ai (67)", "6 fallos", "—"],
        ["ai.igv", "suite ai (67)", "6 fallos", "—"],
        ["ai.total", "suite ai (67)", "3 fallos", "—"],
        ["ai.apply_coupon", "suite ai (67)", "0 fallos", "—"],
        ["ai._discount (primer cupón)", "suite ai (67)", "0 fallos", "—"],
        ["ai.__init__", "suite ai (67)", "OK", "aceptar (0)"],
    ]))
add(p("Los números 'transitorios' son errores de tipo mientras el cambio estaba a medio aplicar (por ejemplo, "
      "recibir float donde ya se esperaba Decimal). Cada commit es reversible y el estado final se mide siempre "
      "con la suite completa y la compuerta."))

add(p("11. Evidencias y conclusión", "Heading1"))
add(p("Carpeta C:\\Users\\user\\Downloads\\evidencia-s13\\ (fuera del repositorio, para no tocar archivos "
      "prohibidos): 00-test-inicial, 01/02 compuertas antes, 03/04 duelo, 10-20 pruebas por método del equipo, "
      "21/22 team final, 30/31 auditoría IA antes, 32 compuerta tras redondeo, 33 compuerta IA final, "
      "34/35 auditoría IA después, 36 experimento Decimal, 40/41/42 propuesta rechazada."))
add(p("Conclusión: el carrito del equipo y el de la IA calculan con Decimal, toman el precio del catálogo, "
      "respetan existencias en cualquier secuencia y aplican un solo cupón. Las pruebas y la compuerta están en "
      "verde (código 0) y la revisión humana documenta por qué un cambio que la compuerta aceptaba fue rechazado. "
      "El repositorio quedó publicado en GitHub con los 28 commits a nombre del alumno."))
add(p("Autoevaluación según la rúbrica de 20 puntos: 5/5 líneas, existencias y pago; 5/5 Decimal, precio del "
      "servidor y API; 5/5 revisión de los cinco fallos de la IA; 5/5 auditoría, compuerta y uso de IA documentado. "
      "Acciones: puntualidad 1, cumplimiento de tiempos 1, ortografía y redacción 1."))

DOCUMENT = "".join(B)

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="20"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>
<w:rPr><w:b/><w:sz w:val="36"/><w:color w:val="1F3864"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
<w:rPr><w:b/><w:sz w:val="28"/><w:color w:val="1F3864"/></w:rPr><w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
<w:rPr><w:b/><w:sz w:val="24"/><w:color w:val="2E5496"/></w:rPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr>
<w:tblBorders>
<w:top w:val="single" w:sz="4" w:color="9FB3D9"/><w:left w:val="single" w:sz="4" w:color="9FB3D9"/>
<w:bottom w:val="single" w:sz="4" w:color="9FB3D9"/><w:right w:val="single" w:sz="4" w:color="9FB3D9"/>
<w:insideH w:val="single" w:sz="4" w:color="9FB3D9"/><w:insideV w:val="single" w:sz="4" w:color="9FB3D9"/>
</w:tblBorders></w:tblPr></w:style>
</w:styles>"""

DOCUMENT_XML = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>{DOCUMENT}
<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>
</w:body></w:document>"""

TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", TYPES)
    z.writestr("_rels/.rels", RELS)
    z.writestr("word/document.xml", DOCUMENT_XML)
    z.writestr("word/styles.xml", STYLES)
    z.writestr("word/_rels/document.xml.rels", DOC_RELS)

print(OUT)
print(OUT.stat().st_size, "bytes")
