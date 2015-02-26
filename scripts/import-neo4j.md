Importing CDP and other datasets
================================

### import nodes from CDP 2013 emmission dataset
```
LOAD CSV WITH HEADERS FROM 'https://data.cdp.net/api/views/marp-zazk/rows.csv?accessType=DOWNLOAD' AS line
CREATE (company:Company { name: line.`Company Name `, account_number: toInt(line.`Account Number`)})
MERGE (country:Country { name: line.`Country `})
CREATE (company)-[:RESIDES]->(country)
CREATE (report:EmissionReport { year: toInt(line.`Reporting Year`), disclosure_score: line.`Disclosure Score`, performance_band: line.`Performance Band`, scope1: toInt(line.`Scope 1 (metric tonnes CO2e)`), scope2: toInt(line.`Scope 2 (metric tonnes CO2e)`) })
CREATE (company)-[:REPORTED]->(report)
MERGE (sector:Sector { name: line.`Sector `})  
CREATE (company)-[:IN]->(sector)
```

### Query sum of USA CO2 emissions
```
MATCH (country:Country)--(company:Company)--(report:EmissionReport)
WHERE country.name = 'USA'
RETURN sum(report.scope1), sum(report.scope2)
```

### Sum of all country emissions
```
MATCH (country:Country)--(company:Company)--(report:EmissionReport)
RETURN country.name, sum(report.scope1), sum(report.scope2)
ORDER BY sum(report.scope2) DESC
```
