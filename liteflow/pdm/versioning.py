
version_seq = []
len_version = 3
for n in range(1, 10): version_seq.append("00%d" % n)
for n in range(10, 100): version_seq.append("0%d" % n)

def get_next_reference(reference):
    v = reference[-1*len_version:0]
    found = False
    for vv in version_seq:
        if found: break
        if v == vv: found = True
    return reference[:-1*len_version] + vv