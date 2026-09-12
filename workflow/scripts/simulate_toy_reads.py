"""Generate reproducible, error-free paired reads from the toy genome."""

import gzip
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
READ_LENGTH = 100
PAIRS = 10_000
COMPLEMENT = str.maketrans("ACGT", "TGCA")


def main():
    fasta = (ROOT / "reference/star_index/toy.fa").read_text().splitlines()
    assert sum(line.startswith(">") for line in fasta) == 1
    genome = "".join(line.strip() for line in fasta if not line.startswith(">")).upper()
    assert set(genome) <= set("ACGT") and len(genome) >= 500
    for sample, seed in (("sample1", 42), ("sample2", 43)):
        rng = random.Random(seed)
        paths = [ROOT / "data" / f"{sample}_R{mate}.fastq.gz" for mate in (1, 2)]
        with paths[0].open("wb") as raw1, paths[1].open("wb") as raw2:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw1, mtime=0) as r1, gzip.GzipFile(
                filename="", mode="wb", fileobj=raw2, mtime=0
            ) as r2:
                for i in range(1, PAIRS + 1):
                    length = min(500, max(200, round(rng.gauss(300, 30))))
                    start = rng.randrange(len(genome) - length + 1)
                    fragment = genome[start : start + length]
                    if rng.randrange(2):
                        fragment = fragment.translate(COMPLEMENT)[::-1]
                    reads = (fragment[:READ_LENGTH], fragment[-READ_LENGTH:].translate(COMPLEMENT)[::-1])
                    for mate, (handle, sequence) in enumerate(zip((r1, r2), reads), 1):
                        handle.write(f"@{sample}_read{i:05d}/{mate}\n{sequence}\n+\n{'I' * READ_LENGTH}\n".encode())
        print(f"{sample}: {PAIRS:,} pairs, {READ_LENGTH} bp per mate")


if __name__ == "__main__":
    main()
