"""Predefines some column names we know they're numeric."""


COLUMN_TYPES = {
    "numeric":
    ["Start", "End", "vardb_life", "vardb_gatk", "vardb_tvc",
     "GATK.counts", "GATK.Depth", "TVC.counts", "TVC.Depth",
     "PopFreqMax", "1000G_ALL", "1000G_AFR", "1000G_AMR", "1000G_EAS",
     "1000G_EUR", "1000G_SAS", "ExAC_ALL", "ExAC_AFR", "ExAC_AMR", "ExAC_EAS",
     "ExAC_FIN", "ExAC_NFE", "ExAC_OTH", "ExAC_SAS", "ESP6500siv2_ALL",
     "ESP6500siv2_AA", "ESP6500siv2_EA", "CG46", "SIFT_score",
     "Polyphen2_HDIV_score", "Polyphen2_HVAR_score", "LRT_score",
     "MutationTaster_score", "MutationAssessor_score", "FATHMM_score",
     "PROVEAN_score", "VEST3_score", "CADD_raw", "CADD_phred", "DANN_score",
     "fathmm-MKL_coding_score", "MetaSVM_score", "MetaLR_score",
     "integrated_fitCons_score", "integrated_confidence_value",
     "GERP++_RS", "phyloP7way_vertebrate", "phyloP20way_mammalian",
     "phastCons7way_vertebrate", "phastCons20way_mammalian",
     "SiPhy_29way_logOdds", "dbscSNV_ADA_SCORE", "dbscSNV_RF_SCORE", "dann"],
    "str":
    ["Chr", "Ref", "Alt", "Callers", "TVC.counts", "TVC.samples",
     "Func.refGene", "Gene.refGene", "vardb_1x",
     "GeneDetail.refGene", "ExonicFunc.refGene", "AAChange.refGene",
     "Func.ensGene", "Gene.ensGene", "GeneDetail.ensGene",
     "ExonicFunc.ensGene", "AAChange.ensGene", "phastConsElements46way",
     "genomicSuperDups", "OMIM_id", "OMIM_disorder", "GeneReviews_disease",
     "clinvar_20150330", "avsnp147", "snp144Flagged", "cosmic70", "SIFT_pred",
     "Polyphen2_HDIV_pred", "Polyphen2_HVAR_pred", "LRT_pred",
     "MutationTaster_pred", "MutationAssessor_pred", "FATHMM_pred",
     "PROVEAN_pred", "fathmm-MKL_coding_pred", "MetaSVM_pred", "MetaLR_pred",
     "Interpro_domain", "Zygosity", "Qual", "Depth", "CHROM", "POS",
     "ID", "REF", "ALT", "QUAL", "FILTER", "AF", "AO", "DP", "FAO", "FDP",
     "FR", "FRO", "FSAF", "FSAR", "FSRF", "FSRR", "FWDB", "FXX HRUN",
     "LEN MLLD", "OALT", "OID", "OMAPALT", "OPOS", "OREF", "QD", "RBI",
     "REFB", "REVB", "RO", "SAF", "SAR", "SRF", "SRR", "SSEN", "SSEP", "SSSB",
     "STB", "STBP", "TYPE", "VARB", "GT", "GQ"]}

# Update 2017/03/20
COLUMN_TYPES["numeric"].extend(
    ["gnomAD_genome_ALL", "gnomAD_genome_AFR", "gnomAD_genome_AMR",
     "gnomAD_genome_ASJ", "gnomAD_genome_EAS", "gnomAD_genome_FIN",
     "gnomAD_genome_NFE", "gnomAD_genome_OTH", "gnomAD_exome_ALL",
     "gnomAD_exome_AFR", "gnomAD_exome_AMR", "gnomAD_exome_ASJ",
     "gnomAD_exome_EAS", "gnomAD_exome_FIN", "gnomAD_exome_NFE",
     "gnomAD_exome_OTH", "gnomAD_exome_SAS", "MaxPopFreq", "1000g2015aug_afr",
     "1000g2015aug_eas", "1000g2015aug_sas", "1000g2015aug_amr",
     "1000g2015aug_eur", "1000g2015aug_all", "M-CAP_score",
     "GenoCanyon_score", "phastCons100way_vertebrate_rankscore", "Eigen-raw",
     "Eigen-PC-raw", "integrated_fitCons_score_rankscore", "DANN_rankscore",
     "GenoCanyon_score_rankscore", "GERP++_RS_rankscore""CADD_raw_rankscore",
     "SIFT_converted_rankscore", "LRT_converted_rankscore", "VEST3_rankscore",
     "SiPhy_29way_logOdds_rankscore", "phyloP20way_mammalian_rankscore",
     "MutationTaster_converted_rankscore", "fathmm-MKL_coding_rankscore",
     "M-CAP_rankscore", "phastCons20way_mammalian_rankscore",
     "PROVEAN_converted_rankscore", "MetaSVM_rankscore",
     "phyloP100way_vertebrate_rankscore", "Polyphen2_HVAR_rankscore",
     "Polyphen2_HDIV_rankscore", "FATHMM_converted_rankscore",
     "MutationAssessor_score_rankscore", "MetaLR_rankscore",
     "phyloP100way_vertebrate", "phastCons100way_vertebrate", "M-CAP_pred"
     "REVEL", "PBP", "QT", "LEN", "HRUN", "MLLD", "PB", "FXX"])

COLUMN_TYPES["str"].extend(
    ["OMIM_ID", "OMIM_Disorder", "snp147Flagged", "GTEx_V6_gene",
     "GeneReviews_ID", "MCAP", "ClinVar_Phenotype", "ICGC_Id",
     "Eigen_coding_or_noncoding", "ICGC_Occurrence", "GeneReviews_Disease",
     "GTEx_V6_tissue", "ClinVar_Significance"])
