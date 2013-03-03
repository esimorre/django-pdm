
version_seq = []
len_version = 3
version_schema = "001-099"

for n in range(1, 10): version_seq.append("00%d" % n)
for n in range(10, 100): version_seq.append("0%d" % n)

def get_next_reference(reference):
    v = reference[-1*len_version:]
    found = False
    for vv in version_seq:
        if found: break
        if v == vv: found = True
    if not found:
        raise Exception("Versioned reference %s does not comply schema %s" % (reference, version_schema))
    return reference[:-1*len_version] + vv