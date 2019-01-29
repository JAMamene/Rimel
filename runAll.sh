#!/usr/bin/env bash

if [[ ! -f merges.csv ]]; then
    touch merges.csv
fi

echo "WARNING : sonarQube server must be running !"

cd repository-finder
python3 extract.py 10 1000 16000

cd ../merge-extractor/
python3 main.py

cd ../merge-conflict-extractor/
python3 main.py ../repositories/ ../merges.csv

cd ../repositories/
for d in */ ; do
    cd $d
    key=$(basename $d)
    if [[ ! -d ./target ]]; then
        mkdir ./target
    fi
    /home/thyvador/Apps/sonar-scanner-3.3.0.1492-linux/bin/sonar-scanner -Dsonar.projectKey=$key -Dsonar.sources=. -Dsonar.java.binaries=./target
    cd ..
done

cd ../quality-analyser/
python3 analyse_file_quality.py ../merges-conflicts.json ../quality-report.json



