"""Generate reproducible, error-free paired reads from the toy genome."""

import argparse
import csv
import gzip
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
READ_LENGTH = 100
PAIRS = 10_000
COMPLEMENT = str.maketrans("ACGT", "TGCA")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, default=ROOT / "project_A/samples.tsv",
                        help="Sample sheet; r1/r2 paths are relative to its directory")
    args = parser.parse_args()
    sheet = args.samples.resolve()
    with sheet.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if not {"sample", "r1", "r2"}.issubset(reader.fieldnames or []):
            raise ValueError("Sample sheet requires sample, r1, and r2 columns")
        rows = list(reader)
    if not rows or any(not row.get(k) for row in rows for k in ("sample", "r1", "r2")):
        raise ValueError("Sample sheet is empty or contains missing values")
    if len({row["sample"] for row in rows}) != len(rows):
        raise ValueError("Sample IDs must be unique")
    destinations = [(sheet.parent / row[k]).resolve() for row in rows for k in ("r1", "r2")]
    if len(set(destinations)) != len(destinations):
        raise ValueError("FASTQ output paths must be unique")
    if any(not str(path).endswith(".fastq.gz") for path in destinations):
        raise ValueError("FASTQ output paths must end with .fastq.gz")
    fasta = (ROOT / "reference/star_index/toy.fa").read_text().splitlines()
    assert sum(line.startswith(">") for line in fasta) == 1
    genome = "".join(line.strip() for line in fasta if not line.startswith(">")).upper()
    assert set(genome) <= set("ACGT") and len(genome) >= 500
    for index, row in enumerate(rows):
        sample, seed = row["sample"], 42 + index
        rng = random.Random(seed)
        paths = [(sheet.parent / row[k]).resolve() for k in ("r1", "r2")]
        for path in paths:
            path.parent.mkdir(parents=True, exist_ok=True)
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
