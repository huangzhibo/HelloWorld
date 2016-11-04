## Variation Annotation Database
---
### 转录本信息
1. **refgene**
 	- Description
 		- `absence` 	
	- Download
   		- hg19:  
   `http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz`
	  	- hg38:
   `http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/refGene.txt.gz`

2. **ENSEMBL Gene**
 	- Description
 		- `absence`	
	- Download
   		- hg19:  
	`http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/ensGene.txt.gz`
		- hg38:
	`http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/ensGene.txt.gz`
3. **UCSC Known Gene**
 	- Description
 		- `absence`	
	- Download
   		- hg19:  
	`http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/knownGene.txt.gz`
		- hg38:
	`http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/knownGene.txt.gz`	

---
### 突变频率数据库
1. **ESP6500**
  - Description
   	 - http://evs.gs.washington.edu/EVS/
  - Download
  	 - **hg19**
  	 `http://www.openbioinformatics.org/annovar/download/hg19_esp6500siv2_all.txt.gz`
   	 - **hg38**
   	 `http://www.openbioinformatics.org/annovar/download/hg38_esp6500siv2_all.txt.gz`
   	 - **hg19 & hg38**
   	 `http://evs.gs.washington.edu/evs_bulk_data/ESP6500SI-V2-SSA137.GRCh38-liftover.snps_indels.txt.tar.gz`
   	 `OR`
   	 `http://evs.gs.washington.edu/evs_bulk_data/ESP6500SI-V2-SSA137.GRCh38-liftover.snps_indels.vcf.tar.gz`

2. **G1000**
  - Description
 	 - [ucscbrowser tgpPhase3 describe](http://ucscbrowser.genap.ca/cgi-bin/hgTables?db=hg19&hgta_group=varRep&hgta_track=tgpPhase3&hgta_table=tgpPhase3&hgta_doSchema=describe+table+schema)
  	 - **Paper**: [A global reference for human genetic variation](http://www.nature.com/nature/journal/v526/n7571/full/nature15393.html)
  - Download
    	- GRCh37:
	    `ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz`
    	- GRCh38:   
    	使用[CrossMap](https://github.com/huangzhibo/CrossMap)进行坐标转换
1. **EXAC**
  - Description
   	 - http://exac.broadinstitute.org
   	 - [A Guide to the Exome Aggregation Consortium (ExAC) Data Set](https://macarthurlab.org/2014/11/18/a-guide-to-the-exome-aggregation-consortium-exac-data-set/)
   	 - [6 Population Catalogs Compared with the ExAC 61,486 Exomes](http://blog.goldenhelix.com/grudy/6-population-catalogs-compared-with-the-exac-61486-exomes/?_cldee=emhpYm85MEAxMjYuY29t)
  - Download  
   	 `ftp://ftp.broadinstitute.org/pub/ExAC_release/`
   	 `ftp://ftp.broadinstitute.org/pub/ExAC_release/current/ExAC.r0.3.1.sites.vep.vcf.gz`
   	 
4. **pvfd**
	- Description
		- `...`	

---
### 突变位点数据库
1. **dbSNP**
   - **Description**
   		- `...`	
   - **Download**
   		- **GRCh37**
	`ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b147_GRCh37p13/VCF/All_20160601.vcf.gz`
		- **GRCh38**
	`ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b147_GRCh38p2/VCF/All_20160527.vcf.gz`
	
---
### 基因信息数据库
 1. **HGNC**
  - **Description**
 		- standardised nomenclature to human genes
  		- [Contents](http://www.genenames.org/help/statistics-downloads)
  		- [download page](http://www.genenames.org/cgi-bin/statistics#help)
  - **Download**
  		- `ftp://ftp.ebi.ac.uk/pub/databases/genenames/new/tsv/hgnc_complete_set.txt`

---
### 遗传病及表型相关数据库：
1. **OMIM**
	- Description
		- 在线人类孟德尔遗传数据库，关于人类基因和遗传紊乱的数据库  
		- [简介](https://www.douban.com/note/544090098/)
	- Download
		- `ftp://ftp.ncbi.nih.gov/repository/OMIM/`

2. **gwasCatalog**
	- Description
		- 全基因组关联分析数据库，变异及疾病信息
	- Download
		- **hg19**
			`http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/gwasCatalog.txt.gz`
		- **hg38**
		`http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/gwasCatalog.txt.gz`

3. **CLINVAR**
	- Description
		- 遗传变异-临床表型相关的数据库, 记录了基因组变异和人类健康的关系
		- [clinvar数据库的使用](http://www.lyon0804.com/clinvarshu-ju-ku-de-shi-yong.html)
	- Download
		- **hg19 & hg38**
		`ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/`
		
4. **HGMD**
	- Description
		- `人类基因突变数据库,提供有关人类遗传疾病突变的综合性数据`
		- [HGMD 人类基因突变数据库专业版](http://blog.sciencenet.cn/home.php?mod=space&uid=668293&do=blog&id=627301)
	- Download  
		`http://www.hgmd.cf.ac.uk/docs/register.html`
5. **CGD**
	- Description
		- `Clinical Genomic Database`
	- Download
	
6. **BGIGaP**
	- - Description
		- `暂不可用`

### 功能及致病性预测数据库：
1. **dbNSFP**
	- Description
		- `主要存储非同义单核苷酸突变的相关信息`
	- Download
		- **hg19 & hg38**
		`ftp://dbnsfp:dbnsfp@dbnsfp.softgenetics.com/dbNSFPv3.2a.zip`
	- Hbase Import Table
		- `dbNSFP`
		- `dbNSFP_index_hg19_chr_pos_alt`
		- `dbNSFP_index_hg38_chr_pos_alt`

---
## Hbase数据库导入
1. 导入的数据应对alt进行


---		
## 附录
1. The abbreviation of 7 population groups (ExAC):
	- AFR: African & African American
	- AMR: American
	- EAS: East Asian
	- FIN: Finnish
	- NFE: Non-Finnish European
	- SAS: South Asian
	- OTH: Other

		