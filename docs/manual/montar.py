"""Monta o manual de continuidade da land (HTML) a partir de conteudo.html + o prompt."""
import html, pathlib
aqui = pathlib.Path(__file__).parent
corpo = (aqui / 'conteudo.html').read_text()
corpo = corpo.replace('{{PROMPT}}', html.escape((aqui.parent / 'prompt-continuidade-land.md').read_text().rstrip()))
css = (aqui / 'estilo.css').read_text()
(aqui / 'manual.html').write_text(f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Land da Núcleo · manual de continuidade · 28/10/2026</title><style>{css}</style></head><body>{corpo}</body></html>''')
print('ok')
