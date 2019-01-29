# Quality analyser

## Prerequisites
 
 - Python 3 installed
 - Need a SonarQube server up and running. [How to install SonarQube](https://docs.sonarqube.org/latest/setup/get-started-2-minutes/)
 - Need a sonar scanner : [How to install](https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner)
 
## Analyse project

The script `project_quality_analyser.py` can be used to analyse the whole project software quality using sonar.

To run this script you need to be in the directory of the project to analyse.
**How to use** :
 ```bash
 $ python3 project_quality_analyse.py <sonar-scanner-path> <project_key> -s <src-path>
```


## Analyse files

The script `analyse_file_quality.py` can be used to analyse the quality of designated files.
Before running this script you need to run sonar-scanner on the project to analyse. 
(You can also run the previous script that will run the scanner)

**How to use** :
```bash
 $ python3 analyse_file_quality.py <input_file_path>
```
