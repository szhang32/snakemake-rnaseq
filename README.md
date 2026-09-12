# Toy RNA-seq workflow

Run from the repository root with the Snakemake environment activated:

```sh
snakemake --cores 4 --use-conda -p
```

`--use-conda` installs and activates the tools declared in `workflow/envs/`.
Without it, tools such as STAR must already be on your shell's PATH.
