SAMPLES = ["sample1", "sample2"]

rule all:
    input:
        expand("results/{sample}.txt", sample=SAMPLES)

rule process_sample:
    input:
        "data/{sample}.txt"
    output:
        "results/{sample}.txt"
    shell:
        """
        cat {input} > {output}
        """