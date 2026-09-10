SAMPLES = ["sample1", "sample2"]

rule all:
    input:
        expand("results/{sample}.txt", sample=SAMPLES),
        expand("results/{sample}.log", sample=SAMPLES)

rule process_sample:
    input:
        r1="data/{sample}_R1.txt",
        r2="data/{sample}_R2.txt"
    output:
        merged="results/{sample}.txt",
        log="results/{sample}.log"
    shell:
        """
        mkdir -p results
        cat {input.r1} {input.r2} > {output.merged}
        echo "Processed {wildcards.sample}" > {output.log}
        """
