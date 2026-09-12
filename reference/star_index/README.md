# Toy STAR reference

Synthetic 10,000 bp chromosome `toy_chr1`, built with STAR 2.7.11b.
For workflow testing only; this is not a biological reference.

`toy.fa` uses Python random seed 42 and contains the four existing toy
read pairs at offsets 1000, 3000, 5000, and 7000 (zero-based). Each R2
reverse complement starts 180 bases after R1. `toy.gtf` annotates these
four fragments as single-exon transcripts.

Rebuilt using the Snakemake Conda environment created from
`workflow/envs/star.yaml` (STAR 2.7.11b), with `sjdbOverhang=99` for
the current 100 bp reads. Rebuild from the repository root:

```sh
source /Users/szhang32/miniforge3/bin/activate .snakemake/conda/e965c9f31d2391d31e4bd11d727a8590_
STAR \
  --runMode genomeGenerate --runThreadN 2 \
  --genomeDir reference/star_index \
  --genomeFastaFiles reference/star_index/toy.fa \
  --sjdbGTFfile reference/star_index/toy.gtf \
  --sjdbOverhang 99 --genomeSAindexNbases 5 --genomeChrBinNbits 10
```

The reduced suffix-array setting follows the STAR small-genome guidance:
https://github.com/alexdobin/STAR/blob/master/source/parametersDefault

Validation: genome generation finished successfully; index loading in an
alignment smoke check succeeded. That check reported zero input reads,
so successful read mapping has not been verified.
