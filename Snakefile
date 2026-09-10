SAMPLES = ["sample1", "sample2"]

rule all:
    input:
        expand("results/{sample}.txt", sample=SAMPLES)

rule process_sample:
    input:
        r1="data/{sample}_R1.txt",
        r2="data/{sample}_R2.txt"
    output:
        "results/{sample}.txt"
    shell:
        """
        mkdir -p results
        cat {input.r1} {input.r2} > {output}
        """
