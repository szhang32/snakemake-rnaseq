SAMPLES = ["sample1", "sample2"]

rule all:
    input:
        expand("results/fastqc/{sample}_R1_fastqc.html", sample=SAMPLES),
        expand("results/fastqc/{sample}_R2_fastqc.html", sample=SAMPLES)


rule fastqc:
    input:
        r1="data/{sample}_R1.fastq.gz",
        r2="data/{sample}_R2.fastq.gz"

    output:
        r1_html="results/fastqc/{sample}_R1_fastqc.html",
        r1_zip="results/fastqc/{sample}_R1_fastqc.zip",
        r2_html="results/fastqc/{sample}_R2_fastqc.html",
        r2_zip="results/fastqc/{sample}_R2_fastqc.zip"

    conda:
        "workflow/envs/fastqc.yaml"

    shell:
        """
        mkdir -p results/fastqc
        fastqc {input.r1} {input.r2} --outdir results/fastqc
        """


