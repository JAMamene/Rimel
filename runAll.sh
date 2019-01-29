#!/usr/bin/env bash

cd repository-finder
python extract.py

cd ../merge-extractor/
python main.py

cd ../merge-conflict-extractor/
python main.py ../repositories/ ../merges.csv