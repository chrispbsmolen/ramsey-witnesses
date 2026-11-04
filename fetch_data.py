"""Download the third-party witness files that are not redistributed here into data/ (not committed),
from the original URLs in sources/manifest.csv, and check every file against the SHA-256 recorded there.

  python3 fetch_data.py                 # everything (about 63 MB, most of it McKay's graph6 sets)
  python3 fetch_data.py mckay exoo_site # only these sources (source column of the manifest)

Special cases:
  exoo_tatarevic2015  one zip from the Electronic Journal of Combinatorics, unpacked into data/exoo_tatarevic/
  kuznetsov_table2    the circulants are printed in Table 2 of arXiv:1505.07186v5; the PDF is downloaded to
                      data/kuznetsov/, converted with pdftotext -layout (poppler) and Table 2 is written to
                      data/kuznetsov/table2_circulants.csv; each circulant is then checked against the hash of
                      its canonical text n:d1,d2,... recorded in the manifest
Writes results/fetch_log.txt with the date and one line per witness: OK, MISMATCH or MISSING.
"""
import os, re, sys, csv, zipfile, subprocess, urllib.request, hashlib
import verify_ramsey as V
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
KUZ_PDF_SHA = '46d374e26acef7e83f67587262fd37910268f58a9e500887685a56c3811c6ee3'
EXT_ZIP = 'https://www.combinatorics.org/ojs/index.php/eljc/article/view/v22i3p11/data'
EXT_ZIP_SHA = '5b05a7ff47f2d9af543a16f786ad895ef8a3322c0e7ff9278072c8651a0dfc6e'


def get(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path): return
    req = urllib.request.Request(url, headers={'User-Agent': 'ramsey-witnesses fetch_data.py'})
    with urllib.request.urlopen(req, timeout=120) as r, open(path + '.part', 'wb') as f:
        while True:
            b = r.read(1 << 20)
            if not b: break
            f.write(b)
    os.replace(path + '.part', path)


def kuznetsov_table2(pdf, out):
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True, check=True).stdout
    i = txt.index('Table 2. Largest cyclic colorings'); j = txt.index('Table 3. Largest cyclic coloring orders')
    seg = re.sub(r'\n\s*\n+\s*\d+\s*\n', '\n', txt[i:j])          # page numbers
    seg = seg.replace('\n               ', ' ').replace('\n                   ', ' ')
    ents = re.findall(r'\n\s*(\(\d+,\s*\d+\)(?:\(isolated\))?)\s+CirculantGraph\[(\d+),\s*\{([^}]*)\}\]', seg)
    with open(out, 'w', newline='') as fo:
        w = csv.writer(fo); w.writerow(['label', 'n', 'distances'])
        for lab, n, s in ents: w.writerow([lab.replace(' ', ''), n, ' '.join(re.findall(r'\d+', s))])


def main():
    rows = [r for r in csv.DictReader(open('sources/manifest.csv')) if r['committed'] == 'no']
    want = set(sys.argv[1:])
    if want: rows = [r for r in rows if r['source'] in want]
    log = []
    for r in rows:
        try:
            if r['source'] == 'exoo_tatarevic2015':
                z = 'data/exoo_tatarevic/ExT_data.zip'; get(EXT_ZIP, z)
                if V.sha256_file(z) != EXT_ZIP_SHA: raise ValueError('zip hash differs')
                if not os.path.exists(r['path']): zipfile.ZipFile(z).extract(os.path.basename(r['path']), 'data/exoo_tatarevic')
                got = V.sha256_file(r['path'])
            elif r['source'] == 'kuznetsov_table2':
                pdf = 'data/kuznetsov/1505.07186v5.pdf'; get(r['url'], pdf)
                if V.sha256_file(pdf) != KUZ_PDF_SHA: raise ValueError('PDF hash differs')
                if not os.path.exists(r['path']): kuznetsov_table2(pdf, r['path'])
                n, D = V.circcsv_entry(r['path'], r['entry'])
                got = V.sha256_text(V.circulant_key(n, D))
            else:
                get(r['url'], r['path']); got = V.sha256_file(r['path'])
            st = 'OK' if got == r['sha256'] else 'MISMATCH'
        except Exception as e:
            st = 'MISSING (%s)' % repr(e)[:120]
        log.append('%s %s' % (st, r['id'])); print(log[-1], flush=True)
    import datetime
    size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk('data') for f in fs)
    open('results/fetch_log.txt', 'w').write('fetch_data.py %s, sources: %s, data/ bytes %d\n' % (datetime.date.today().isoformat(), ' '.join(sorted(want)) or 'all', size) + '\n'.join(log) + '\n')
    bad = [l for l in log if not l.startswith('OK')]
    print('%d witnesses, %d OK, %d not OK' % (len(log), len(log) - len(bad), len(bad)))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
