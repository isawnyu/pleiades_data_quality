# pleiades_data_quality

Generate reporting data on select quality-related aspects of the [Pleiades gazetteer](https://pleiades.stoa.org) dataset.

This code expects to be run against Pleiades JSON data such as that found in https://github.com/isawnyu/pleiades.datasets/tree/main/data/json and produces report output such as that found in https://github.com/isawnyu/pleiades.datasets/tree/main/data/data_quality

## how to run it:

### generate reporting data, all of which is saved to issues.json

```
python scripts/report.py ../pleiades.datasets/data/json/ ../pleiades.datasets/data/data_quality/
```

### create CSV files containing issue-specific reporting data pulled from issues.json

```
python scripts/issues2csv.py ../pleiades.datasets/data/data_quality/issues.json
```

## quick tip

To get an overview of how many issues there are in any given category, see the "summary" key in issues.json.


