# MERGE EXTRACTOR

You can run merge extractor with the following command :
```
python3 main.py
```

### Input :
A file named "repositories.csv" must present. Each line of this file should be formated like this :
```  
repositories_owner,repositories_name,url_to_clone
```

### Ouptut :
A file named merges.csv with all extracted merges, the csv file has the following format :
```
url,left,right,result,base
```

#### Warning :
*  A "token" file with github api token must be present
*  Git must be installed




