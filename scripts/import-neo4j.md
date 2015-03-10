Importing CDP and other datasets
================================

### import nodes from CDP 2013 emmission dataset
```
LOAD CSV WITH HEADERS FROM 'https://data.cdp.net/api/views/marp-zazk/rows.csv?accessType=DOWNLOAD' AS line
CREATE (company:Company { name: line.`Company Name `, account_number: toInt(line.`Account Number`)})
MERGE (country:Country { name: line.`Country `})
CREATE (company)-[:RESIDES]->(country)
CREATE (report:EmissionReport { year: toInt(line.`Reporting Year`), disclosure_score: toInt(line.`Disclosure Score`), performance_band: line.`Performance Band`, scope1: toInt(line.`Scope 1 (metric tonnes CO2e)`), scope2: toInt(line.`Scope 2 (metric tonnes CO2e)`) })
CREATE (company)-[:REPORTED]->(report)
MERGE (sector:Sector { name: line.`Sector `})  
CREATE (company)-[:IN]->(sector)
```

### Query sum of USA CO2 emissions
```
MATCH (country:Country)--(company:Company)--(report:EmissionReport)
WHERE country.name = 'USA'
WITH sum(report.scope1) AS direct, sum(report.scope2) AS indirect
CREATE (country)-[:EMITS]->(emit: DirectEmission { name: direct})
RETURN direct, indirect
```

### Sum of all country emissions
```
MATCH (country:Country)--(company:Company)--(report:EmissionReport)
WITH country.name AS country_name, sum(report.scope1) AS direct, sum(report.scope2) AS indirect 
CREATE (country)-[:EMITS1]->(emission: DirectEmission {name: direct})
RETURN country_name, direct, indirect
ORDER BY indirect DESC
```


