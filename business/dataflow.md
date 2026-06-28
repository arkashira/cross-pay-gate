# Dataflow Architecture
## Overview
The cross-pay-gate dataflow architecture is designed to handle the flow of data from external sources, through processing and storage, to ultimately serve users. The architecture is divided into six tiers: External data sources, Ingestion layer, Processing/transform layer, Storage tier, Query/serving layer, and Egress to user.

## Architecture Diagram
```
                                      +---------------+
                                      |  External    |
                                      |  Data Sources  |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Ingestion    |
                                      |  Layer        |
                                      |  (API Gateway,|
                                      |   Message Queue)|
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Processing/  |
                                      |  Transform Layer|
                                      |  (Data Processing,|
                                      |   Data Validation)|
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Storage Tier  |
                                      |  (Database, Data |
                                      |   Warehouse)    |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Query/Serving |
                                      |  Layer         |
                                      |  (Query Engine, |
                                      |   API Gateway)  |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Egress to User|
                                      |  (Web Application,|
                                      |   Mobile Application)|
                                      +---------------+
```

## Components per Tier
* **External Data Sources**
  + Banks and payment providers' APIs
  + Digital asset exchanges' APIs
  + Market data feeds
* **Ingestion Layer**
  + API Gateway (e.g. AWS API Gateway, Google Cloud Endpoints)
  + Message Queue (e.g. Apache Kafka, Amazon SQS)
  + Authentication and Authorization (e.g. OAuth, JWT)
* **Processing/Transform Layer**
  + Data Processing (e.g. Apache Beam, Apache Spark)
  + Data Validation (e.g. Apache Airflow, Great Expectations)
  + Data Transformation (e.g. Apache NiFi, AWS Glue)
* **Storage Tier**
  + Database (e.g. relational database, NoSQL database)
  + Data Warehouse (e.g. Amazon Redshift, Google BigQuery)
  + Blockchain network (e.g. Ethereum, Hyperledger Fabric)
* **Query/Serving Layer**
  + Query Engine (e.g. Apache Hive, Presto)
  + API Gateway (e.g. AWS API Gateway, Google Cloud Endpoints)
  + Authentication and Authorization (e.g. OAuth, JWT)
* **Egress to User**
  + Web Application (e.g. React, Angular)
  + Mobile Application (e.g. iOS, Android)
  + Authentication and Authorization (e.g. OAuth, JWT)

## Auth Boundaries
* **Ingestion Layer**: Authentication and Authorization using OAuth or JWT to secure API Gateway and Message Queue
* **Processing/Transform Layer**: Authentication and Authorization using OAuth or JWT to secure Data Processing and Data Validation
* **Query/Serving Layer**: Authentication and Authorization using OAuth or JWT to secure Query Engine and API Gateway
* **Egress to User**: Authentication and Authorization using OAuth or JWT to secure Web Application and Mobile Application

Note: The auth boundaries are designed to secure the flow of data between tiers and ensure that only authorized users and systems can access and manipulate the data.