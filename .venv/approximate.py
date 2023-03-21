import string
from boyer_moore import boyer_moore
from preprocessing import BoyerMoore

def approximate_match(p, t, n, missed):
    segment_length = int(round(len(p) / (n+1)))
    all_matches = set()
    for i in range(n+1):
        start = i*segment_length
        end = min((i+1)*segment_length, len(p))
        p_bm = BoyerMoore(p[start:end], alphabet='abcdefghijklmnopqrstuvwxyz ')
        matches = boyer_moore(p[start:end], p_bm, t)
        # Extend matching segments to see if whole p matches
        for m in matches:
            missed[m-start] = []
            if m < start or m-start+len(p) > len(t):
                continue
            mismatches = 0
            for j in range(0, start):
                if not p[j] == t[m-start+j]:
                    mismatches += 1
                    missed[m-start].append(j)
                    if mismatches > n:
                        break
            for j in range(end, len(p)):
                if not p[j] == t[m-start+j]:
                    mismatches += 1
                    missed[m-start].append(j)
                    if mismatches > n:
                        break
            if mismatches <= n:
                all_matches.add(m - start)
            else:
              del missed[m-start]
    return list(all_matches)
