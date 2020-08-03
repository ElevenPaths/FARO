FARO Docker setup
-----------------

FARO can be executed inside docker. We are using `docker-compose` since FARO requires two containers to be working together `faro-server` and `tika-server`.

We have envisioned two scenarios: use faro as an end-user or using docker for faro development and provided different environments accordingly.

## Table of contents

* [Docker Prerequisites](#docker-prerequisites)
* [Environments](#docker-environments)
    * [Production](#build-docker-production-environment)
    * [Development](#build-docker-development-environment)
* [Run Faro Analysis](#run-analysis)
    * [Results](#Results)
* [Run Faro Tests](#run-tests)

## Docker prerequisites

It may be obvious but let's be explicit....you need to have a working docker engine on your machine. Since we use the latest grammatic sugar for the docker-compose.yml you need to be at least on engine version 19.03.0+. More info on docker versions [here](https://docs.docker.com/compose/compose-file/compose-versioning/)

## Docker environments

If you are only interested in using faro to quickly analyze some data you should use the production environment, read along.

If on the other hand you want to develop or contribute to faro use the [development environment](#build-docker-development-environment)

### Build Docker Production Environment

First you'll need to retrieve the images binaries from our repo using `docker load`:
```
$ docker load --input https://github.com/ElevenPaths/FARO/releases/download/v2.0.0/faro.tar.gz
$ docker load --input https://github.com/ElevenPaths/FARO/releases/download/v2.0.0/tika.tar.gz
```

Once you have retrieve those images you can launch FARO by running:
```
$ cd docker
$ docker-compose -f docker-compose-prod.yml up
```

### Build Docker Development Environment

```
$ cd docker
$ docker-compose up --build
```

## Run Analysis

Once you have built your environment and have it running you can use faro to analyse any folder by running

```unix
$ cd docker
$ ./run_faro.sh <your folder with files>
```

```windows
cd docker
run_faro.bat <your folder with files>
```

**Some customization like tuning the OCR process can be tweaked through the use of environment variables in a file** whose path needs to be provided as an argument to the script. We have provided a commented example to serve as a template [here](docker/faro_env_example.list).

For more information on its meaning take a look at the finetuning section in the project's README.

```unix
$ cd docker
$ ./run_faro.sh <your folder with files> <path to env file>
```

for example:

```
$ cd docker
$ ./run_faro.sh ../data faro_env_example.list
```

### Results

FARO creates an "output" folder inside the parent folder of `docker` normally the root folder for faro project if you have performed a `git clone`:

 * `output/scan.$CURRENT_TIME.csv`: is a csv file with the score given to the document and the frequence of indicators in each file.

```
filepath,score,monetary_quantity,signature,personal_email,mobile_phone_number,financial_data,document_id,custom_words,meta:content-type,meta:author,meta:pages,meta:lang,meta:date,meta:filesize,meta:num_words,meta:num_chars,meta:ocr
/Users/test/code/FARO_datasets/quick_test_data/Factura_NRU_0_1_001.pdf,high,0,0,0,0,0,1,4,application/pdf,Powered By Crystal,1,es,,85739,219,1185,False
/Users/test/code/FARO_datasets/quick_test_data/Factura_Plancha.pdf,high,6,0,0,0,0,2,8,application/pdf,Python PDF Library - http://pybrary.net/pyPdf/,1,es,,77171,259,1524,True
/Users/test/code/FARO_datasets/quick_test_data/20190912-FS2019.pdf,high,3,0,0,0,0,1,2,application/pdf,FPDF 1.6,1,es,2019-09-12T20:08:19Z,1545,62,648,False
```

* `output/scan.$CURRENT_TIME.entity`: is a json with the list of indicators (disaggregated) extracted in a file. For example:

```
{"filepath": "/Users/test/code/FARO_datasets/quick_test_data/Factura_NRU_0_1_001.pdf", "entities": {"custom_words": {"facturar": 3, "total": 1}, "prob_currency": {"12,0021": 1, "12,00": 1, "9,92": 1, "3,9921": 1, "3,99": 1, "3,30": 1, "15,99": 1, "13,21": 1, "1.106.166": 1, "1,00": 1, "99,00": 1}, "document_id": {"89821284M": 1}}, "datetime": "2019-12-11 14:19:17"}
{"filepath": "/Users/test/code/FARO_datasets/quick_test_data/Factura_Plancha.pdf", "entities": {"document_id": {"H82547761": 1, "21809943D": 2}, "custom_words": {"factura": 2, "facturar": 2, "total": 2, "importe": 2}, "monetary_quantity": {"156,20": 4, "2,84": 2, "0,00": 2, "159,04": 2, "32,80": 4, "191,84": 2}, "prob_currency": {"1,00": 6, "189,00": 2}}, "datetime": "2019-12-11 14:19:27"}
{"filepath": "/Users/test/code/FARO_datasets/quick_test_data/20190912-FS2019.pdf", "entities": {"document_id": {"C-01107564": 1}, "custom_words": {"factura": 1, "total": 1}, "monetary_quantity": {"3,06": 1, "0,64": 1, "3,70": 1}}, "datetime": "2019-12-11 14:19:33"}
```

## Run tests

If you are using docker development environment and would like to run some regression tests, run the following commands

```unix
$ cd docker
$ ./test_faro.sh
```

```windows
cd docker
test_faro.bat
```

As mentioned in the running analysis section, the test script also allows some finetuning of faro by providing a file with environment variables, for example:

```unix
$ cd docker
$ ./test_faro.sh <path to env file>
```
