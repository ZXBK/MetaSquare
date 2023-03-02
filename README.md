# MetaSquare 1.0

## Introduction
Taxonomy classification is a crucial component of metagenome analysis. Since next-generation sequencing has been the majority method to generate those data, accurately identifying these sequences has become fundamental to research in a microbial community study. 16S amplicon analysis is one of the standard processes to identify metagenome taxonomy. However, only a few databases are available for 16S amplicon analysis, and most popular and extensive databases, such as Silva, have their limitations. To improve classification efficiency, we use the computational method to integrate those popular databases and establish a meta-metagenome database called MetaSquare. 

## Metasquare for Nanopore 16S full-length analysis
1.  Download **Metasquare_Kraken2_database** from [https://hub.docker.com/r/lsbnb/metasquare_db](https://hub.docker.com/r/lsbnb/metasquare_db)
```
$docker pull lsbnb/metasquare_db
$docker run -it --rm -v $PWD:/in lsbnb/metasquare_db cp /home/Metasquare.tar.gz /in
$tar zxvf Metasquare.tar.gz 
#Metasquare database files are in the folder "Metasquare"
```
2.  Transfer **Metasquare_Kraken2_database** to the _**output_dir**_
3.  Run Porechop to clean up the sequences before classification  ([Porechop's DockerHub](https://hub.docker.com/r/robegan21/porechop))

```
$docker run --rm -v $(pwd):/data --name=porechop -it robegan21/porechop
$cd data
$porechop -i input_reads.fastq.gz -o output_reads_1.fastq.gz
$porechop -i output_reads_1.fastq.gz -b output_dir/seq.fastq

```

4.  Install Kraken2 through [**GitHub**](https://github.com/DerrickWood/kraken2) or [**DockerHub**](https://hub.docker.com/r/staphb/kraken2)
5.  Run Kraken2 to Classification at _**output_dir**_

```
kraken2 -db /PATH/TO/Metasquare_Kraken2_database --threads N --report seq.fasta.report seq.fastq
```

6.  The .report file could be vizualized and analyzed through online-tool [**Pavian**](https://github.com/fbreitwieser/pavian)

## Metasquare for illumina 16S variants (V3-V4) amplicons analysis

1.  Download combine6DB_V3V4_classifier.qza to target folder from [https://hub.docker.com/r/lsbnb/metasquare_db](https://hub.docker.com/r/lsbnb/metasquare_db)
```
$docker pull lsbnb/metasquare_db
$docker run -it --rm -v $PWD:/in lsbnb/metasquare_db cp /home/Metasquare.tar.gz /in
$tar zxvf Metasquare.tar.gz 
#Metasquare database files are in the folder "Metasquare"
```
2.  Initialize **QIIME2** 2019.10 version

P.S. Because our Classifier is trained with QIIME2 2019.10 version, it is necessary to use QIIME2 2019.10 version for the following classification.

```
$docker pull quay.io/qiime2/core:2019.10
$docker run -itd --name qm2_2019_10 -v $PWD:/in -w /in quay.io/qiime2/core:2019.10 bash
$docker exec -it qm2_2019_10 bash
#Now you are in the Qiime2 container and ready to analysis
```

3.  Processing data with tutorial steps mentioned in [QIIME2 Moving Pictures tutorial](https://docs.qiime2.org/2021.4/tutorials/moving-pictures/)
   Necessary steps included: 
   - qiime tools import (data formats refer to [QIIME2 Importing data](https://docs.qiime2.org/2021.4/tutorials/importing/))
   - qiime demux summarize
   - qiime dada2 

4.  Run QIIME2 clasaification
```
qiime feature-classifier classify-sklearn \
--i-classifier /PATH/TO/Metasquare_QIIME2_V3V4_classifier.qza \
--i-reads rep-seqs.qza \
--p-n-jobs N \  
--o-classification taxonomy.qza
```

5.  Export QIIME2 visualized file
```
qiime taxa barplot \
--i-table table.qza \
--i-taxonomy taxonomy.qza \
--m-metadata-file sample-metadata.tsv \
--o-visualization taxa-bar-plots.qzv
```

6.  QZV file could be analysis on website [**QIIME 2 View**](https://view.qiime2.org/)


**Version history:**

First Version: v1.0, 2, June, 2021

**Reference:**

1.[https://github.com/rrwick/Porechop](https://github.com/rrwick/Porechop)

2.Wood, D.E., Lu, J. & Langmead, B. Improved metagenomic analysis with Kraken 2. Genome Biol 20, 257 (2019). [https://doi.org/10.1186/s13059-019-1891-0](https://doi.org/10.1186/s13059-019-1891-0)

3.Bolyen E, et. al 2019. Reproducible, interactive, scalable and extensible microbiome data science using QIIME 2. Nature Biotechnology 37: 852–857. [https://doi.org/10.1038/s41587-019-0209-9](https://doi.org/10.1038/s41587-019-0209-9)

---
## Add new sequences

### Goal: Filtering out homopolymer and ambiguous_bases

```
pip install scikit-bio
pip install scipy==1.8.1
#python version: 3.8.14
python3.8 main.py -i read.fa -o1 o1 -o2 o2
```
- scipy requirement error :
https://github.com/biocore/scikit-bio/issues/1818
