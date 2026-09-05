rule hello:
    input:
        "data/name.txt"
    output:
        "results/hello.txt"

    shell:
        """
        echo "Hello $(cat {input})" > {output}
        """