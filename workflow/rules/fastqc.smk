rule fastqc:
    input:
        r1=get_r1,
        r2=get_r2
    output:
        r1_html=f"{RESULTS}/fastqc/{{sample}}_R1_fastqc.html",
        r1_zip=f"{RESULTS}/fastqc/{{sample}}_R1_fastqc.zip",
        r2_html=f"{RESULTS}/fastqc/{{sample}}_R2_fastqc.html",
        r2_zip=f"{RESULTS}/fastqc/{{sample}}_R2_fastqc.zip"
    threads: 2
    resources:
        mem_mb=4000,
        runtime=60
    conda:
        "../envs/fastqc.yaml"
    shell:
        """
        mkdir -p {RESULTS}/fastqc

        fastqc \
            {input.r1:q} \
            {input.r2:q} \
            --threads {threads} \
            --outdir {RESULTS}/fastqc
        """
