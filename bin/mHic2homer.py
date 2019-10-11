from collections import defaultdict
import pandas as pd

"""Converts HiC interaction matrices generated by the mHiC pipeline [1]
(and all tools that have the same output format) into the format used by Homer [2].


[1] https://github.com/yezhengSTAT/mHiC
[2] http://homer.salk.edu/homer/index.html
"""

binning_information = pd.read_csv(
    snakemake.input[0], names=["interaction", "count"], sep="\t")

tmp = binning_information["interaction"].str.split(' ', expand=True)

interaction_matrix = pd.DataFrame()
interaction_matrix["bin_a"] = tmp[0] + "-" + tmp[1]
interaction_matrix["bin_b"] = tmp[2] + "-" + tmp[3]
interaction_matrix["frequency"] = binning_information["count"]

bin_pair_to_value = defaultdict(dict)
for bin_a, bin_b, value in zip(
        interaction_matrix["bin_a"], interaction_matrix["bin_b"],
        interaction_matrix["frequency"]):
    bin_pair_to_value[bin_a][bin_b] = value
    bin_pair_to_value[bin_b][bin_a] = value

result_matrix = pd.DataFrame()
result_matrix["HiCMatrix"] = interaction_matrix["bin_a"]
result_matrix["Regions"] = result_matrix["HiCMatrix"]

# Add column for each bin
for bin_a in interaction_matrix["bin_a"]:
    result_matrix[bin_a] = interaction_matrix["bin_a"].apply(
        lambda bin_b: bin_pair_to_value[bin_a].get(bin_b, 0))

result_matrix.to_csv(snakemake.output[0], sep="\t", index=False)
