#!/bin/bash
mkdir -p output
INPUT_PATH=$(cd "$1"; pwd)

if [ -z "$2" ]
then
   SUFFIX=$(date "+%Y.%m.%d-%H.%M.%S")
else
   SUFFIX=$2
fi

CPU_PARALLEL_USAGE="50%"

echo "filepath,score,monetary_quantity,signature,personal_email,mobile_phone_number,financial_data,document_id,custom_words,meta:content-type,meta:encrypted,meta:author,meta:pages,meta:lang,meta:date,meta:filesize,meta:ocr" > output/scan.$SUFFIX.csv

# Run faro over a recursive list of appropriate filetypes
find "$INPUT_PATH" -type f \( ! -regex '.*/\.[^.].*' \) | parallel -P $CPU_PARALLEL_USAGE python faro_detection.py -i {} --output_entity_file output/scan.$SUFFIX.entity --dump >> output/scan.$SUFFIX.csv
