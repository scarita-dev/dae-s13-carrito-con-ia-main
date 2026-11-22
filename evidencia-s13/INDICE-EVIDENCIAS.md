# Índice de evidencias — Laboratorio extra S13

Repositorio local: `C:\Users\user\Downloads\dae-s13-carrito-con-ia-main`
Repositorio remoto: `https://github.com/scarita-dev/dae-s13-carrito-con-ia-main.git` (rama `main`)
Entregable: `Entregable-S13-Extra-Carrito-Revisado.docx`

Los 28 commits tienen como autor **y** committer a `scarita-dev <sofia.carita@tecsup.edu.pe>`, la identidad real
de Git del alumno. Se reescribió el metadato de autoría (sin cambiar el contenido de los archivos) porque la
configuración local inicial tenía un nombre y un email ficticios. Como cambiaron los hashes, hay que hacer
`git push --force-with-lease` para que GitHub muestre la historia corregida.

Nota de entorno: en PowerShell hay que fijar `$env:PYTHONIOENCODING = 'utf-8'` antes de `gate`/`duelo`, porque esos
comandos leen la salida de subprocesos como UTF-8 y la consola de Windows usa otra página de códigos.

| Archivo | Comando que lo produjo | Resultado |
|---|---|---|
| `00-test-inicial.txt` | `python manage.py test` | 67 tests, 2 failures, 67 errors (exit 1) |
| `01-gate-team-antes.json.txt` | `python manage.py gate --json` | rechazar, 60 fallos, exit 1 |
| `02-gate-ai-antes.json.txt` | `python manage.py gate --modo ai --json` | rechazar, 18 fallos, exit 1 |
| `03-duelo-antes.txt` | `python manage.py duelo` | team 7/60, ai 49/18 |
| `04-duelo-ai-detalle-antes.txt` | `python manage.py duelo --modo ai` | detalle de los 18 fallos |
| `10-20-team-*.txt` | `python manage.py test shop.tests.test_<archivo>` pruebas por método | una por turno del carrito del equipo |
| `21-test-team-final.txt` | `python manage.py test` | 67 OK, exit 0 |
| `22-gate-team-despues.json.txt` | `python manage.py gate --json` | aceptar, 0 fallos, exit 0 |
| `30-audit-ai-antes.txt` | `$env:SHOP_MODE='ai'; python manage.py audit_cart <6 rutas> --catalogo-fijo` | 1 de 6 sin hallazgos |
| `31-audit-ai-antes-replay.txt` | ídem con `--replay` | REPLAY_MISMATCH en 05 y 06 |
| `32-gate-ai-tras-redondeo.json.txt` | `python manage.py gate --modo ai --json` | rechazar, 16 fallos, exit 1 |
| `33-gate-ai-despues.json.txt` | `python manage.py gate --modo ai --json` | aceptar, 0 fallos, exit 0 |
| `34-audit-ai-despues-replay.txt` | auditoría IA con `--replay --catalogo-fijo` | ningún REPLAY_* |
| `35-audit-ai-despues-json-strict.txt` | auditoría IA con `--json --strict --catalogo-fijo` | exit 1 (5 carritos con hallazgos declarados) |
| `36-decimal-experimento.txt` | `python decimal_experimento.py` | 0.30000000000000004 / 0.3 / 0.84 / 0.85 |
| `40-gate-propuesta-rechazada.json.txt` | `python manage.py gate --json` con la propuesta de leer `price` | aceptar, exit 0 (por eso la rechazó la revisión) |
| `41-diff-rechazo.patch` | `git diff -- shop/cart_team.py` | diff de una línea añadida |
| `42-gate-tras-rechazo.json.txt` | `python manage.py gate --json` tras `git restore` | aceptar, exit 0 |

Commits: `85ec222` guarda el carrito original de la IA; 27 commits posteriores (11 del equipo y 16 de la IA), uno por método; 28 en total.
