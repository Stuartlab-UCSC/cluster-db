
# TSV database utilites.

def from_rows(rows):
    # Convert sqlite rows to TSV lines.
    if len(rows) < 1:
        return ''
    tsv = '\t'.join(rows[0].keys()) # the header
    for row in rows:
        lines = []
        for l in list(row.values()):
            lines.append(str(l))
        tsv += '\n' + '\t'.join(lines)
    return tsv

