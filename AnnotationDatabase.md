## Variation Annotation Database
---
### 转录本信息
1. refgene
 	- Description
 		- `absence` 	
	- Download
   		- hg19:  
   `http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz`
	  	- hg38:
   `http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/refGene.txt.gz`

2. ENSEMBL Gene
 	- Description
 		- `absence`	
	- Download
   		- hg19:  
	`http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/ensGene.txt.gz`
		- hg38:
	`http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/ensGene.txt.gz`
3. UCSC Known Gene
 	- Description
 		- `absence`	
	- Download
   		- hg19:  
	`http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/knownGene.txt.gz`
		- hg38:
	`http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/knownGene.txt.gz`	

---
### 突变频率数据库
1. ESP6500
  - Description
   	 - http://exac.broadinstitute.org
  - Download
   	 - ftp://ftp.broadinstitute.org/pub/ExAC_release/current/*

2. G1000
  - Description
 	 - http://ucscbrowser.genap.ca/cgi-bin/hgTables?db=hg19&hgta_group=varRep&hgta_track=tgpPhase3&hgta_table=tgpPhase3&hgta_doSchema=describe+table+schema
  	 - **Paper**: [A global reference for human genetic variation](http://www.nature.com/nature/journal/v526/n7571/full/nature15393.html)
  - Download
    	- hg19:
	    `ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz`
    	- hg38: 
    	`ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/other_mapping_resources/ALL.wgs.1000G_phase3.GRCh38.ncbi_remapper.20150424.shapeit2_indels.vcf.gz`

3. EXAC
4. pvfd

---
### 突变位点数据库
1. **dbSNP**
   - **Description**
   		- `...`	
   - **Download**
   		- hg19: 
	http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/snp147.txt.gz
		- hg38:  
	http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/snp147.txt.gz
	
---
### 基因信息数据库
 1. **HGNC**
  - **Description**
 		- standardised nomenclature to human genes
  		- `http://www.genenames.org/help/statistics-downloads`
  		- `http://www.genenames.org/cgi-bin/statistics#help`
  - **Download**:
  		- ftp://ftp.ebi.ac.uk/pub/databases/genenames/new/tsv/hgnc_complete_set.txt

---
### 遗传病及表型相关数据库：
1. **OMIM**
	- description:
		- 在线人类孟德尔遗传数据库，关于人类基因和遗传紊乱的数据库  
	- Download:
		- `absence`	

2. gwasCatalog
	- description:
		- 全基因组关联分析数据库，变异及疾病信息
	- Download:
		- [**hg19**](http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/gwasCatalog.txt.gz "http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/gwasCatalog.txt.gz"):
			`http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/gwasCatalog.txt.gz`
		- **hg38**:
		`http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/gwasCatalog.txt.gz`

3. CLINVAR:
	- description: 遗传变异-临床表型相关的数据库
4. HGMD
	- description
		- `人类基因突变数据库,提供有关人类遗传疾病突变的综合性数据`
5. CGD
	- description
		- `Clinical Genomic Database`
6. BGIGaP

### 功能及致病性预测数据库：
1. dbNSFP
	- description
		- `主要存储非同义单核苷酸突变的相关信息`