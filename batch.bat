for %%f in (*.tsv) do (
  dff --filepath %%f --json-filter path/to/filters.json > output_%%f
)

del output_output*.tsv
