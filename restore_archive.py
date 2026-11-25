#!/usr/bin/env python3
"""Verify and losslessly restore the original ZIP from ordered Git LFS parts."""
from pathlib import Path
import argparse,hashlib,json,os
ROOT=Path(__file__).resolve().parent
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--verify-only',action='store_true')
 ap.add_argument('--output',type=Path)
 a=ap.parse_args();m=json.loads((ROOT/'archive_manifest.json').read_text(encoding='utf-8'))
 output=(a.output or ROOT/m['archive']['name']).resolve()
 partial=output.with_name(output.name+'.partial')
 if not a.verify_only and (output.exists() or partial.exists()):
  raise SystemExit('Output or partial file already exists; nothing overwritten.')
 target=None;created=False;whole=hashlib.sha256();total=0
 try:
  if not a.verify_only:target=partial.open('xb');created=True
  for row in m['parts']:
   p=ROOT/row['path']
   if not p.is_file() or p.stat().st_size!=row['bytes']:
    raise RuntimeError('Missing/truncated part or LFS pointer: '+row['path']+'. Run git lfs pull.')
   digest=hashlib.sha256();n=0
   with p.open('rb') as f:
    for b in iter(lambda:f.read(8*1024*1024),b''):
     digest.update(b);whole.update(b);n+=len(b);total+=len(b)
     if target:target.write(b)
   if n!=row['bytes'] or digest.hexdigest()!=row['sha256']:
    raise RuntimeError('Part SHA-256 mismatch: '+row['path'])
   print('VERIFIED',row['path'],n,flush=True)
  if total!=m['archive']['bytes'] or whole.hexdigest()!=m['archive']['sha256']:
   raise RuntimeError('Original archive SHA-256 mismatch')
  if target:
   target.flush();os.fsync(target.fileno());target.close();target=None
   os.link(partial,output);partial.unlink();created=False
  print('ORIGINAL ZIP SHA-256',whole.hexdigest(),flush=True)
  print('VERIFY ONLY: no ZIP created' if a.verify_only else 'RESTORED '+str(output),flush=True)
 finally:
  if target:target.close()
  if created and partial.exists():partial.unlink()
if __name__=='__main__':main()
