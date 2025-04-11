# typo_modal

Typology of modal choice logics -> relevant sustainable mobility recommendations

## Development

Use [poetry](https://python-poetry.org/) to manage dependencies.

### Prepare data

Data are included in the package in [parquet](https://parquet.apache.org/) format. This format is more efficient than CSV (reduced storage size and faster to read) and is recommended for large datasets.

To convert CSV and the Shape files from the data source folder to Parquet files in the package's data folder, run:

```bash
make parquet
```

### Install dependencies

```bash
make install
```

### Run tests

```bash
make test
```

### Build package

```bash
make build
```
