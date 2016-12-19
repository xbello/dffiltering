"""Deals with TAB files to load, munge and filter them."""
import pandas as pd

COLUMN_TYPES = {
    "numeric":
    ["Start", "End", "vardb_life", "vardb_gatk", "vardb_tvc", "vardb_1x",
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
    ["Chr", "Ref", "Alt", "Func.refGene", "Gene.refGene",
     "GeneDetail.refGene", "ExonicFunc.refGene", "AAChange.refGene",
     "Func.ensGene", "Gene.ensGene", "GeneDetail.ensGene",
     "ExonicFunc.ensGene", "AAChange.ensGene", "phastConsElements46way",
     "genomicSuperDups", "OMIM_id OMIM_disorder", "GeneReviews_disease",
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


def dffilter(df, conditions):
    """Return a dataframe filtered by the conditions."""
    if not conditions:
        return df

    condition = conditions.pop()

    if "contains" in condition:
        column, query = condition.split(" contains ")
        return dffilter(df[df[column].str.contains(query)], conditions)
    else:
        return dffilter(df.query(condition), conditions)


def load(filepath):
    """Return the filepath loaded as a DataFrame."""
    try:
        df = pd.read_table(filepath)
    except UnicodeDecodeError:
        df = pd.read_table(filepath, encoding="iso-8859-1")

    # Correct columns with "." to zeroes.
    df.replace(".", 0, inplace=True)
    # Correct columns with "1." to ones.
    df.replace("1.", 1, inplace=True)
    # Fill the NaN with zeroes
    df.fillna(0, inplace=True)

    df[COLUMN_TYPES["numeric"]] = df[COLUMN_TYPES["numeric"]].\
        apply(pd.to_numeric)

    return df


def argparser():
    """Return the parsed arguments."""
    import argparse

    parser = argparse.ArgumentParser(description="DataFrame Filtering")
    parser.add_argument("filepath",
                        help="Path to the TSV file")
    parser.add_argument("json_filter",
                        help="JSON file with list of filters")

    return parser


def main(args):
    """Main entry point to be called as command line."""
    import json

    with open(args.json_filter) as json_filter:
        df = dffilter(load(args.filepath), json.load(json_filter))

    return df


if __name__ == "__main__":
    import sys
    print(main(argparser().parse_args(sys.argv[1:])))
