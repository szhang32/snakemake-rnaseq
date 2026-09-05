rule hello:
    output:
        "results/hello.txt"

    shell:
        """
        echo "Hello Snakemake" > {output}
        """