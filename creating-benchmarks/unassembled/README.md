# PSSS Team 3, Hard Annotation, Benchmarking annotation of unassembled reads

## Notes

### Input datasets -- CAMI

+ Resources
    + Paper: https://www.nature.com/articles/nmeth.4458#MOESM1
    + Data portal: https://data.cami-challenge.org/
+ Creation of challenge datasets (from paper)
    + We simulated three metagenome data sets of different organismal complexities and sizes by generating 150-bp paired-end reads with an Illumina HighSeq error profile from the genome sequences of 689 newly sequenced bacterial and archaeal isolates and 598 sequences of plasmids, viruses and other circular elements (Supplementary Note 1, Supplementary Tables 3, 6 and 12 and Supplementary Figs. 47 and 48). These data sets represent common experimental setups and specifics of microbial communities. They consist of a 15-Gbp single sample data set from a low-complexity community with log normal abundance distribution (40 genomes and 20 circular elements), a 40-Gbp differential log normal abundance data set with two samples of a medium-complexity community (132 genomes and 100 circular elements) and long and short insert sizes, as well as a 75-Gbp time series data set with five samples from a high-complexity community with correlated log normal abundance distributions (596 genomes and 478 circular elements). The benchmark data sets had some notable properties; all included (i) species with strain-level diversity (Supplementary Fig. 47) to explore its effect on program performance; (ii) viruses, plasmids and other circular elements, for assessment of their impact on program performances; and (iii) genomes at different evolutionary distances to those in reference databases, to explore the effect of increasing taxonomic distance on taxonomic binning. Gold-standard assemblies, genome bin and taxon bin assignments and taxonomic profiles were generated for every individual metagenome sample and for the pooled samples of each data set.
    + The figure below is from the SI of the CAMI paper. The red and orange fractions should contribute sufficient strain variation to produce unassembled fractions of reads. All CAMI datasets contain red and orange fractions, so we'll start with the low complexity dataset as our benchmark dataset and a develop a pipeline that can be extended to include the medium and high complexity datasets.

![Screen shot of figure from publication SI.](https://i.imgur.com/wMv2uy2.png)

+ DOIs for CAMI I data products
    + http://gigadb.org/dataset/view/id/100344

+ CAMI low files
    + `gsa_mapping.binning`: map between gold standard contig, genome of origin, and contig bp
        + will need to be parsed to be in a useful format
        + unclear if coords are 0 or 1 based
    + `gs_read_mapping.binning.gz`: mapping of each read to contig in genome of origin, and I'm guessing start bp of mapping 
        + will need to be parsed to be in a useful format
### Demo tools

+ Mifaser on reads
+ PathRacer on MetaSPAdes assembly graph, built from reads
    + Expectation that this will be lossy, since the ms assembly graph drops many of the unassemble-able reads
    + contact pathracer author to understand modifications that would allow pathracer to run on a cDBG
+ spacegraphcats multifasta annotation
    + also probably built from reads, although could potentially name bcalm graph appropriately to be input to demonstrate starting from cDBG. 

### Working Goals

+ [X] Determine whether CAMI low has sufficient strain variation to confound assemblers
+ [x] ~~look up/record CAMI assembler performances, including # reads that do not align to the assembly~~
    + Re-generate for dataset. CAMI I was too long ago for stats to be relevant.
+ [x] Determine whether annotations exist for the gold standard assembly
    + They don't appear to...so
    + **Question:** is there a good-enough/best practices way to annotate the "gold standard" assembly, which will in turn propogate annotations ot the reads?
+ [ ] snakefile to generate benchmarking data
    + [x] data download
    + [x] fastq assembly
        + note -- CAMI I was done a long time ago. Tools have changed and improved, best to use new versions.
    + [x] identification of unassembled reads via mapping (bowtie2). Create a df annotating by read name whether a read is assembled or unassembled
    + [x] annotation of source genomes
        + **Question**: what database/tool should we use to generate silver standard annotations?
            + prokka -> hmmer
    + [ ] Use `gs_read_mapping.binning.gz` and source genome gff file to generate a read:annotation map. Join with unassembled/assembled df to produce full gs metadata table.
+ [ ] Run example assessments/generate tutorial for how to use benchmarking data
+ [ ] Assess whether subsequent CAMI datasets are in the same format
    + May need a CAMI I snakefile and a CAMI II snakefile to generate more benchmarking datasets.

### AWS config

+ Instance config
        - **AMI:** Ubuntu Server 20.04 (under Quick Start)
![](https://i.imgur.com/uBj4Qh3.png)
        - **Instance Type:** t3.2xlarge
        - harddrive/root: 32gb
        - volume: 500G
```
ssh private/key ubuntu@EC2-address
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge

# set up volume
sudo bash
lsblk
file -s /dev/nvme1n1
mkfs -t xfs /dev/nvme1n1
ls /mnt
mount /dev/nvme1n1 /mnt
df -h
chown ubuntu:ubuntu /mnt
exit
```

## Documentation

### Sequence search problem investigated

The general goal of Team 3 was to generate benchmarking datasets that allow us to assess how well tools perform in annotating divergent or difficult sequences, and how well these methods scale for time/computational resources as the query sizes increase. Originally this was couched within the context of annotating contiguous sequences produced via assembly of metagenome reads or by long read sequencing. However, many short reads captured by metagenome sequencing fail to assemble and therefore comprise fragments that are too small to annotate with methods aimed at ORF annotation. These sequences often originate from low abundance organisms and are low coverage, or from strain variation, and represent functional potential that may be important in a community of interest (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5955982/). 

We sought to understand how well available tools annotate short metagenomic sequencing reads that are not assembled. To this end, we generated a benchmarking dataset comprised of short metagenome sequencing reads, where each read is labelled by its source genome, contiguous sequence, base pair, open read frame, ortholog annotation, and assembly status. We demonstrate the use of this data set with existing methods, and provide recommendations for extensions and improvements on this benchmarking data set.

### Existing methods

**Annotation of short reads.** Some methods annotate reads directly, bypassing assembly. In general, these methods compare sequences in the reads against sequences in a database to assign annotations. Common methods include DIAMOND+MEGAN (https://currentprotocols.onlinelibrary.wiley.com/doi/full/10.1002/cpz1.59) and mifaser (https://academic.oup.com/nar/article/46/4/e23/4670955?login=true). However, annotation is more difficult with short sequences, and more time consuming due to the high volume and repetition/depth in short sequencing reads. 

**Annotation of assembly graphs.** Assembly graphs like de Bruijn graphs (DBG) and compact de Bruijn graphs (cDBG) contain all sequences (k-mers) present in the reads, regardless of whether they end up in the linear assembly. However, working with metagenome \(c)DBGs is challenging because they are large data structures, and depending on sequence complexity, contain many short sequences and branches. These properties make gene annotation directly on assembly graphs a challenging problem. 

Even still, some tools address this problem. PathRacer aligns profile hidden markov models to an assembly graph (https://www.biorxiv.org/content/10.1101/562579v1). It performs amino acid translation and allows annotations to span edges, potentially improving upon annotation of fragmented metagenome assemblies. The current implementation of PathRacer takes a metaSPAdes assembly graph as input, which is a simplified data structure compared to a cDBG; this assembly graph does not include all sequences in the reads which disconnects low coverage edges (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5411777/). 

The spacegraphcats also recently implemented a new search approach, `multifasta query`, that enables cDBG annotation (https://spacegraphcats.github.io/spacegraphcats/05-alpha-spacegraphcats/#multifasta-queries). Spacegraphcats introduces a computationally efficient framework for organizing and querying cDBGs at scale (https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02066-4). The `multifasta query` approach takes a multifasta file and queries into the cDBG graph with each sequence individually. It transfers the annotation of the query sequence to every node in the cDBG that shares at least one k-mer with the query (default *k* = 31). Because it relies on exact matching of nucleotide k-mer sequences, this method of annotation may be brittle to evolutionary distance or divergent sequences. Additionally, it is reliant on the completeness of the database (multifasta file) to transfer annotations to cDBG nodes. Given the prevelance of lateral gene transfer and other evolutionary processes that give rise to distinct nucleotide content in microbial communities, it may be difficult to acheive complete annotation of the cDBG by this method. Lastly, because this approach annotates full cDBG nodes, a node, particularly long unitigs (nodes with many k-mers), may carry multiple annotations. Similarly, this method does not demarcate the boundaries of annotations, only the nodes on which a annotation occurrs.

~To mitigate some of these issues, there is also a protein search implemented in spacegraphcats (https://github.com/spacegraphcats/spacegraphcats/pull/379). To enable this search, there is a second index that is built atop the cDBG, where each unitig is translated into all six open reading frames, and the resultant protein k-mers are connected to their unitigs. This index can then be searched with a protein query, returning all dominating set pieces with at least one k-mer in common with the query.~~ *NB this would have to expanded to the multifasta structure to be practically useful for cDBG annotation.*

### Datasets

We extended the benchmarking datasets provided by the Critical Assessment of Metagenome Interpretation (CAMI) challenge. The CAMI challenge datasets simulate short and long read metagenome data for microbial communities from source input genomes. The simulated data includes diverse genomes, natural and simulated strain variation, and viral and plasmid sequences. The sequencing reads are simulated from source genomes with known taxonomy, and the origin of each read is recorded (genome, contiguous sequence, and basepair). 

We extended the CAMI benchmarking datasets to include annotations (open reading frames, orthologs) for the source genomes and propagated these annotations to the simulated sequencing reads. We also labelled each sequencing read as assembled or unassembled. We provide this information as a CSV file that includes annotations, as well as those provided by the CAMI challenge, in a user-friendly format. We also provide a fastq file of the unassembled reads.

To determine whether a read was assembled or not, we used the provided simulated short sequencing reads to generate a metagenome assembly with MEGAHIT. We then mapped the reads back to the assembly. Reads that did not map back to the assembly were designated as a "unassembled." We arbitrarily selected MEGAHIT as a metagenome assembler in this pipeline; MEGAHIT and metaSPAdes performed approximately equally in the CAMI II challenge (https://www.biorxiv.org/content/10.1101/2021.07.12.451567v1). We used bowtie2 with parameter `--end-to-end` to map reads back to the assembly, as was done in the original CAMI I challenge.

For this codeathon, we started with the CAMI I CAMI_low dataset, the smallest dataset.

### Benchmark metrics
Define and justify the metrics you used to measure performance on the sequence search problem.

TBD

+ false positives
+ false negatives
+ true positives
+ true negatives

### Codeathon products

+ **A CSV files that extends the metadata provided by the CAMI data challenge to include read assembly status and read annotations.** The data provided by the CAMI challenge, read name, genome source, contig source, and bp start, are re-formatted to be more user friendly. The columns of this csv file are: ` read name, genome source, contig source, bp start, ORF, gene annot, assembly_status, cDBG node?`
+ **A snakemake workflow to generate the benchmark datasets.** The workflow is parameterized so that if other CAMI datasets are named and formatted in the same way as the dataset processed herein, it can be easily extended to generate more benchmarking datasets.
+ **Tertiary workflow products**, including the MEGAHIT assembly and source genome annotations.
+ **READMEs demonstrating how to use the provided benchmarking dataset to evaluate software.** We provide example workflows for mifaser, a tool that annotates reads, and spacegraphcats, a tool that annotates assembly graphs.
+ **Notebooks documenting code for summary statistics and plots to evaluate and summarize tool performance on the benchmarking dataset.**


### Future work

**Improving the silver standard annotations.** In generating "silver standard" annotations, we used eggnog mapper in hmmer mode as a first pass. We applied to the same annotation protocol to all CAMI source genomes, namely using the eggnog-provided hmmer database "Bacteria". While this is appropriate for many of the source genomes, there may be more specific/better databases for the viral and plasmid source genomes. In the future, code to perform source genome annotations could flexibly call on different databases, likely orchestrated by a CSV file that designates source genome name, source genome taxonomy, and annotation database.

**Generating a benchmark dataset with gold standard annotations.** For the creation of an initial benchmarking dataset, we relied on the annotation of source genomes by computational methods. We used prokka to annotate and translate open reading frames, and then used eggnog to assign orthologs names. While we expect genome annotation to perform better than metagenome annotation, there is no way to ground-truth the annotation assignments. In the future, benchmarking datasets could be improved if they were built from source genomes for which gene annotations were known (e.g., a set of source genomes for which gold standard gene annotations have been simulated.). If such a set of source genomes can be produced, they can be used as input to the CAMISIM software (https://github.com/CAMI-challenge/CAMISIM; https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-019-0633-6) which will produce metagenome reads with known gene and genome provenance, including with simulated strain-level diversity.

**Extending to additional CAMI datasets.** The CAMI datasets are valuable community tools for the broader ecosystem of metagenome analysis. The CAMI I and CAMI II challenges produced many simulated metagenomes. In the future, we would like to extend our benchmarking datasets to include additional CAMI datasets. If the files within these datasets are similarly named and formatted then the snakemake pipeline used to generate our initial benchmarking dataset should be easily extensible to include more. However, if the files are named or formatted differently, then it would be worthwhile to encode a separate snakemake workflow that will take as input the default output of the CAMISIM software.

## Getting Started

```
conda env create --name psss --file environment.yml
conda activate psss

# slurm-based cluster
snakemake -j 16 --use-conda --rerun-incomplete --latency-wait 15 --resources mem_mb=200000 --cluster "sbatch -t 10080 -J pm -p bmm -n 1 -N 1 -c {threads} --mem={resources.mem_mb}" -k -n

# AWS
snakemake -j 8 --use-conda --rerun-incomplete -n
```
