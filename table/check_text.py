"""Text checks run before every push: line endings, American spelling, no em dash and no home-folder path in this
repository's own prose.

Copies keep their original text and are not checked for spelling: the public editions of the registrations, logs,
scripts as run, and third-party files. Paths, file names, code and quoted titles are skipped by rule.
Run from anywhere: python3 table/check_text.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CRLF = ['phase2/coverage.csv', 'phase2/witnesses/manifest.csv', 'phase2/checks/logs/INDEX.csv',
        'phase2/scripts_as_run/INDEX.csv', 'phase2/above_survey.csv', 'sources/manifest.csv', 'survey/search_notes.csv',
        'results/coverage.csv', 'table/register.csv', 'table/cells.csv', 'table/claims.csv', 'table/intake.csv',
        'table/closed_inputs.csv', 'table/phase2_entered.csv']
PROSE = ['README.md', 'CORRECTIONS.md', 'CITATION.cff', 'phase2/README.md', 'phase2/NOTES.md', 'phase2/COVERAGE.md',
         'phase2/CHECKS.md', 'table/COLUMNS.md', 'table/CURRENT.md', 'registration/EDITS.md',
         'registration/REGISTRATION_intake.md', 'intake/witnesses/NOTICE.md', '.github/ISSUE_TEMPLATE/offer_a_witness.md']
BRITISH = re.compile(r'colour|licence|neighbour|labelled|labelling|afterwards|behaviour|favour|honour|centre|'
                     r'organis|recognis|summaris|minimis|maximis|optimis|analyse|stabilis|catalogue|modelling|'
                     r'travelled|whilst|amongst|programme|artefact', re.I)
TITLES = ['Neighbourhood counting and new bounds for small three-colour Ramsey numbers']

EDITIONS = ['registration/REGISTRATION_phase1.md', 'registration/REGISTRATION_phase2.md']
PRIVATE = re.compile(r'~/')

bad = []
for f in CRLF:
    b = open(f, 'rb').read()
    if b.count(b'\n') != b.count(b'\r\n'):
        bad.append('%s: not CRLF' % f)

for f in PROSE + EDITIONS:
    for m in PRIVATE.finditer(open(f, encoding='utf-8').read()):
        bad.append('%s: home-folder path "%s"' % (f, m.group(0)))

for f in PROSE:
    t = open(f, encoding='utf-8').read()
    if '\u2014' in t:
        bad.append('%s: em dash' % f)
    t = re.sub(r'```.*?```', '', t, flags=re.S)
    t = re.sub(r'`[^`]*`', '', t)
    t = re.sub(r'https?://\S+', '', t)
    for title in TITLES:
        t = t.replace(title, '')
    for m in BRITISH.finditer(t):
        a, b = m.start(), m.end()
        while a > 0 and not t[a - 1].isspace() and t[a - 1] not in '(|,;':
            a -= 1
        while b < len(t) and not t[b].isspace() and t[b] not in ')|,;':
            b += 1
        word = t[a:b].strip('.:*"\'')
        if re.search(r'[/_]|\.(py|txt|csv|json|md|c|gz)$', word):
            continue
        bad.append('%s: "%s"' % (f, word))

if bad:
    print('\n'.join(bad))
    sys.exit('TEXT CHECK FAILED: %d problems' % len(bad))
print('text check passed: %d CRLF files, %d prose files' % (len(CRLF), len(PROSE)))
