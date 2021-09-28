# The Count

This directory represents what a consumer would need to provide in order to run
the benchmark against "the_count". The Count is a tool for counting exact K-mer 
occurrences in a DNA or RNA sequence very, very quickly (where K=32).
It's a more realistic example than mock-search that uses an existing docker image 
to run the benchmark.

```
docker build -t psss-harness .
```

This should be the only command you need to run to continue benchmarking the software. 
Next, cd ../ and run the nextflow commands using the psss-harness docker image.
