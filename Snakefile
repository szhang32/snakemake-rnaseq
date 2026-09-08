SAMPLES = ["sample1", "sample2", "sample3"]

rule all:
    input:
        expand("bam/{sample}.bam", sample=SAMPLES)

rule align:
    input:
        "reads/{sample}.fastq.gz"
    output:
        "bam/{sample}.bam"
    shell:
        """
        mkdir -p bam
        echo "Processing {input}"
        touch {output}
        """