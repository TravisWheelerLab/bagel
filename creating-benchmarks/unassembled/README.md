

```
conda env create --name psss --file environment.yml
conda activate psss

# slurm-based cluster
snakemake -j 16 --use-conda --rerun-incomplete --latency-wait 15 --resources mem_mb=200000 --cluster "sbatch -t 10080 -J pm -p bmm -n 1 -N 1 -c {threads} --mem={resources.mem_mb}" -k -n

# AWS
snakemake -j 8 --use-conda --rerun-incomplete -n
```
