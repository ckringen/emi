""" Collect verb-particle pairs from Syntactic N-grams """
#!/usr/bin/env python3
import sys

YEARS = range(1960, 2000 + 1)

def get_sum_counts(parts):
    def gen():
        for part in parts:
            try:
                year, count = part.split(",")
                if int(year) in YEARS:
                    yield int(count)
            except ValueError:
                pass
    return sum(gen())

def counts_from_lines(vps, get_code, lines):
    def extract_counts_from_line(line):
        parts = line.strip().split()
        first_part = parts[1]
        second_part = parts[2]
        try:
            first_word, first_pos, first_deptype, _ = first_part.split("/")
            second_word, second_pos, second_deptype, _ = second_part.split("/")
        except ValueError:
            return None
        # Try searching for everything matching this for a limited list of particles, and an unlimited list of verbs.
        relevant_words = tuple(
            (first_word, second_word)[i]
            for i in get_code
        )
        ok = (
            relevant_words in vps
            and (
                get_code == (0,) 
                or (
                    second_pos == 'RB'
                    and second_deptype == 'advmod'
                )
            )
            and (get_code == (1,) or first_pos.startswith("VB"))
        )
        if not ok:
            return None
        else:
            yearcounts = parts[4:]
            return (
                " ".join(relevant_words)
                + "\t" 
                + str(get_sum_counts(yearcounts))
            )

    return filter(None, map(extract_counts_from_line, lines))

def main(vps_filename, get_code):
    get_code = tuple(map(int, get_code))
    with open(vps_filename, 'rt') as infile:
        vps = [tuple(line.strip().split()) for line in infile]
    assert all(len(vp) == 2 for vp in vps)
    vps = {tuple(w[i] for i in get_code) for w in vps}
    for line in counts_from_lines(vps, get_code, sys.stdin):
        print(line)

if __name__ == '__main__':
    try:
        main(*sys.argv[1:])
    except IndexError as e:
        print(e, file=sys.stderr)
        print("Need a filename listing verb-particle combinations; ", end="", file=sys.stderr)
        print("N-gram counts come in through stdin.", file=sys.stderr)
        
