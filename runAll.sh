#!/usr/bin/env bash

cd repository-finder
python extract.py 10 1000 16000

cd ../merge-extractor/
python main.py

cd ../merge-conflict-extractor/
python main.py ../repositories/ ../merges.csv