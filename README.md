# Toy RNA-seq workflow

Run from the repository root with the Snakemake environment activated:

```sh
snakemake --cores 4 --use-conda -p
```

`--use-conda` installs and activates the tools declared in `workflow/envs/`.
Without it, tools such as STAR must already be on your shell's PATH.

On Apple Silicon, `workflow/envs/star.osx-arm64.pin.txt` installs a tested
Intel STAR 2.7.10b environment via Rosetta. This avoids the native STAR
2.7.11b build's zero-input-read bug. Rosetta must be installed on the Mac.
The STAR rule sets 1.1 GB of BAM-sorting memory because the toy index is
too small for STAR's default sorting-memory estimate.
