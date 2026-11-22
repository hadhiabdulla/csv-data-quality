#!/usr/bin/env python3
"""Profile a CSV file: shape, inferred types, missing values, duplicates and basic stats.

Standard library only. Usage: python3 profile_csv.py <file.csv>
"""
import csv
import statistics
import sys
from collections import Counter


def sniff_type(values):
    nums = []
    for v in values:
        try:
            nums.append(float(v))
        except ValueError:
            return 'text', None
    return 'numeric', nums


def profile(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.reader(f))
    if not rows:
        raise SystemExit('empty file')
    header, data = rows[0], rows[1:]
    width = len(header)
    ragged = sum(1 for r in data if len(r) != width)
    seen = set()
    dupes = 0
    for r in data:
        t = tuple(r)
        if t in seen:
            dupes += 1
        seen.add(t)
    cols = []
    for i, name in enumerate(header):
        raw = [r[i] if i < len(r) else '' for r in data]
        missing = sum(1 for v in raw if v.strip() == '')
        present = [v for v in raw if v.strip() != '']
        distinct = len(set(present))
        kind, nums = sniff_type(present)
        col = {'name': name, 'type': kind, 'missing': missing, 'distinct': distinct}
        if kind == 'numeric' and nums:
            col.update(min=min(nums), max=max(nums),
                       mean=round(statistics.fmean(nums), 3),
                       median=statistics.median(nums))
        elif present:
            col['top'] = Counter(present).most_common(3)
        cols.append(col)
    return {'path': path, 'rows': len(data), 'columns': width,
            'ragged_rows': ragged, 'duplicate_rows': dupes,
            'columns_detail': cols}


def render(p):
    lines = ['File: %s' % p['path'],
             'Rows: %d  Columns: %d' % (p['rows'], p['columns']),
             'Duplicate rows: %d  Ragged rows: %d' % (p['duplicate_rows'], p['ragged_rows']),
             '']
    for c in p['columns_detail']:
        lines.append('- %s [%s] missing=%d distinct=%d'
                     % (c['name'], c['type'], c['missing'], c['distinct']))
        if c['type'] == 'numeric':
            lines.append('    min=%s max=%s mean=%s median=%s'
                         % (c['min'], c['max'], c['mean'], c['median']))
        elif c.get('top'):
            tops = ', '.join('%s (%d)' % (v, n) for v, n in c['top'])
            lines.append('    top: %s' % tops)
    return '\n'.join(lines)


def main(argv):
    if len(argv) != 2:
        raise SystemExit('usage: python3 profile_csv.py <file.csv>')
    print(render(profile(argv[1])))


if __name__ == '__main__':
    main(sys.argv)
