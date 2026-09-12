SAMPLES = ["sample1", "sample2"]

rule all:
    input:
        "results/multiqc/multiqc_report.html"

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

rule multiqc:
    input:
        expand("results/fastqc/{sample}_R1_fastqc.zip", sample=SAMPLES),
        expand("results/fastqc/{sample}_R2_fastqc.zip", sample=SAMPLES)

    output:
        "results/multiqc/multiqc_report.html"

    conda:
        "workflow/envs/multiqc.yaml"

    shell:
        """
        mkdir -p results/multiqc
        multiqc results/fastqc \
            --outdir results/multiqc
        """
