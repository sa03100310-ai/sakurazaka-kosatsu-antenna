"""Portable source bundle; excludes hosting identity, Git internals and itself."""
import pathlib,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
out=ROOT/'dist/downloads/sakura-essay-antenna.zip';out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(ROOT.rglob('*')):
  rel=p.relative_to(ROOT)
  if not p.is_file() or any(x in ('.git','.openai','__pycache__','.venv','downloads') for x in rel.parts) or p.suffix in ('.pyc','.zip','.gz'):continue
  z.write(p,pathlib.Path('sakura-essay-antenna')/rel)
print(out)
