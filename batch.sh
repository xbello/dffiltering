for tsv in *.tsv; do
  [ -f ${tsv} ] || break
  dff --filepath ${tsv} --json-filter path/to/filters.json > output_${tsv};
done
