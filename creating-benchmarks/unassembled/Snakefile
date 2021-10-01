DATASETS = ['CAMI_low']

def checkpoint_output_decompress_source_genomes(wildcards):
    # checkpoint_output encodes the output dir from the checkpoint rule.
    checkpoint_output = checkpoints.decompress_source_genomes.get(**wildcards).output[0]    
    file_names = expand("outputs/eggnog_source_genomes/{source_genome}.emapper.annotations",
                        source_genome = glob_wildcards(os.path.join(checkpoint_output, "{source_genome}")).source_genome)
    file_names.remove("outputs/eggnog_source_genomes/.snakemake_timestamp.emapper.annotations")
    #file_names = file_name[:-1]
    return file_names

rule all:
    input:
        #expand("outputs/bowtie2/{dataset}_unmapped.fa", dataset = DATASETS),
        checkpoint_output_decompress_source_genomes

#############################################################
## Obtaining data
#############################################################

rule download_CAMI:
    output: "inputs/CAMI_low.tar"
    resources: 
        mem_mb = "500"
    shell:'''
    wget https://ftp.cngb.org/pub/gigadb/pub/10.5524/100001_101000/100344/ChallengeDatasets.dir/CAMI_low.tar
    '''

rule decompress_CAMI:
    input: "inputs/CAMI_low.tar"
    output: 
        "inputs/CAMI_low/RL_S001__insert_270.fq.gz",
        "inputs/CAMI_low/source_genomes_low.tar.gz",
        "inputs/CAMI_low/gsa_mapping.binning",
        "inputs/CAMI_low/gs_read_mapping.binning.gz",
    shell:'''
    tar xvf {input} -C inputs/
    '''

#################################################################
## Identifying unassembled reads
#################################################################

rule fastp:
    """
    The CAMI I and CAMI II challenge both showed that "using read quality trimming or error correction software, such as ...Fastp... impoved assembly quality." https://doi.org/10.1101/2021.07.12.451567
    Set minimum read length to megahit default minimum kmer length, k = 21
    """
    input: "inputs/{dataset}/RL_S001__insert_270.fq.gz"
    output: 
        r1 = "outputs/fastp/{dataset}_R1.fastp.fq.gz",
        r2 = "outputs/fastp/{dataset}_R2.fastp.fq.gz",
        json = "outputs/fastp/{dataset}.json",
        html = "outputs/fastp/{dataset}.html"
    resources: mem_mb = "8000"
    threads: 8
    benchmark: "benchmarks/fastp_{dataset}.txt"
    conda: "envs/fastp.yml"
    shell:'''
    fastp -i {input} --interleaved_in -o {output.r1} -O {output.r2} -q 4 -j {output.json} -h {output.html} -R {wildcards.dataset} -l 21 -c -w {threads}
    '''

rule assemble:
    """
    The CAMI II challenge indicated that megahit and metaSPAdes performed approximately equally for assembly accuracy and strain recall. Given that megahit requires less ram/runtime, start with that assembler.
    """
    input:
        r1 = "outputs/fastp/{dataset}_R1.fastp.fq.gz",
        r2 = "outputs/fastp/{dataset}_R2.fastp.fq.gz",
    output: "outputs/megahit/{dataset}.contigs.fa"
    params: outdir = lambda wildcards: "outputs/megahit/" + wildcards.dataset + "_tmp/"
    resources: mem_mb = 32000
    benchmark: "benchmarks/megahit_{dataset}.txt"
    conda: "envs/megahit.yml"
    shell:'''
    megahit -1 {input.r1} -2 {input.r2} -o {params.outdir} --out-prefix {wildcards.dataset} --min-contig-len 500
    mv {params.outdir}/{wildcards.dataset}.contigs.fa {output}
    '''

rule index_assembly:
    """
    The CAMI I challenge used bowtie2 with --end-to-end parameter to assess the number of reads that mapped back to the assembly.
    """
    input: "outputs/megahit/{dataset}.contigs.fa"
    output: "outputs/bowtie2_index/{dataset}.1.bt2"
    resources: mem_mb = 8000
    params: prefix = lambda wildcards: "outputs/bowtie2_index/" + wildcards.dataset
    benchmark: "benchmarks/bowtie2_index_{dataset}.txt"
    conda: "envs/bowtie2.yml"
    threads: 1
    shell:'''
    bowtie2-build {input} {params.prefix}
    '''

rule map_reads_to_assembly:
    """
    The CAMI I challenge used bowtie2 with --end-to-end parameter to assess the number of reads that mapped back to the assembly.
    """
    input:
        index="outputs/bowtie2_index/{dataset}.1.bt2",
        r1 = "outputs/fastp/{dataset}_R1.fastp.fq.gz",
        r2 = "outputs/fastp/{dataset}_R2.fastp.fq.gz",
    output: "outputs/bowtie2/{dataset}.bam"
    params: prefix = lambda wildcards: "outputs/bowtie2_index/" + wildcards.dataset
    resources: mem_mb = 8000
    benchmark: "benchmarks/bowtie2_{dataset}.txt"
    conda: "envs/bowtie2.yml"
    threads: 8
    shell:'''
    bowtie2 -x {params.prefix} -1 {input.r1} -2 {input.r2} -p {threads} --end-to-end | \
    samtools view -Sbh --threads {threads} - > {output}
    '''

rule identify_unmapped_reads:
    input: "outputs/bowtie2/{dataset}.bam"
    output: "outputs/bowtie2/{dataset}_unmapped.sam"
    resources: mem_mb = 8000
    benchmark: "benchmarks/samtools_f4_{dataset}.txt"
    conda: 'envs/bowtie2.yml'
    shell:'''
    samtools view -f 4 {input} > {output}
    '''

rule convert_unmapped_reads_to_fastq:
    input: "outputs/bowtie2/{dataset}_unmapped.sam"
    output: "outputs/bowtie2/{dataset}_unmapped.fa"
    resources: mem_mb = 8000
    benchmark: "benchmarks/samtools_fasta_{dataset}.txt"
    conda: 'envs/bowtie2.yml'
    threads: 1
    shell:'''
    samtools fasta {input} > {output}
    '''

############################################################
## Generating silver-standard annotations of source genomes
############################################################

checkpoint decompress_source_genomes:
    input: "inputs/CAMI_low/source_genomes_low.tar.gz"
    output: directory("inputs/CAMI_low/source_genomes")
    shell:'''
    tar xvf {input} -C inputs/CAMI_low
    # these next two lines are probably not the best idea, but the fai can be regenerated easily
    # while its not clear that the circular_one_repeats were used to build the reads.
    # I think if I don't move them out of this directory, I won't be able to properly solve for
    # the root source genome names for downstream rules. It's annoying that the source fasta
    # files shipped with two file endings, *fasta and *fna. 
    rm {output}/*fai
    mv {output}/circular_one_repeat inputs/CAMI_low
    '''

rule prokka_source_genomes:
    input: "inputs/CAMI_low/source_genomes/{source_genome}"
    output: 
        "outputs/prokka_source_genomes/{source_genome}.faa",
        "outputs/prokka_source_genomes/{source_genome}.gff",
        "outputs/prokka_source_genomes/{source_genome}.fna",
    resources: mem_mb = 8000
    benchmark: "benchmarks/prokka_{source_genome}.txt"
    conda: 'envs/prokka.yml'
    params: 
        outdir = 'outputs/prokka_source_genomes/',
        lt = lambda wildcards: wildcards.source_genome.split(".")[0]
    threads: 1
    shell:'''
    prokka {input} --outdir {params.outdir} --prefix {wildcards.source_genome} \
        --force --locustag {params.lt} --cpus {threads} \
        --compliant --centre X
    '''

rule download_eggnog_db:
    output: "inputs/eggnog_db/eggnog.db"
    threads: 1   
    resources: mem_mb = 1000
    conda: "envs/eggnog.yml"
    shell:'''
    download_eggnog_data.py -H -d 2 -y --data_dir inputs/eggnog_db
    '''

rule eggnog_annotate_source_genomes:
    input: 
        faa = "outputs/prokka_source_genomes/{source_genome}.faa",
        db = 'inputs/eggnog_db/eggnog.db'
    output: "outputs/eggnog_source_genomes/{source_genome}.emapper.annotations"
    conda: 'envs/eggnog.yml'
    resources:
        mem_mb = 32000
    threads: 8
    params: 
        outdir = "outputs/eggnog_source_genomes/",
        dbdir = "inputs/eggnog_db"
    shell:'''
    emapper.py --cpu {threads} -i {input.faa} --output {wildcards.source_genome} \
       --output_dir {params.outdir} -m hmmer -d none --tax_scope auto \
       --go_evidence non-electronic --target_orthologs all --seed_ortholog_evalue 0.001 \
       --seed_ortholog_score 60 --override --temp_dir tmp/ \
       -d 2 --data_dir {params.dbdir}
    '''
