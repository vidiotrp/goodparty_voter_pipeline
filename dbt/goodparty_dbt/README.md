\# GoodParty Voter Pipeline



This project demonstrates a \*\*dbt + Airflow voter data pipeline\*\*. It ingests voter data, standardizes it, computes key metrics, and produces visualizations for reporting.



---



\## Project Overview



The pipeline consists of:



1\. \*\*Ingestion \& Orchestration (Airflow)\*\*  

&nbsp;  - Raw voter data is ingested from the source system.

&nbsp;  - Airflow DAG manages dependencies and schedules the pipeline.



2\. \*\*Staging (`stg\_voters`)\*\*  

&nbsp;  - Raw data is loaded into a staging table for initial cleanup and validation.



3\. \*\*Intermediate (`int\_voters\_cleaned`)\*\*  

&nbsp;  - Data is cleaned and standardized:

&nbsp;    - Names capitalized

&nbsp;    - Emails lowercased

&nbsp;    - Missing data flags (`missing\_email`, `missing\_age`, etc.)

&nbsp;    - States standardized to 2-letter abbreviations

&nbsp;    - Only valid ages are kept (0–120)



4\. \*\*Marts\*\*  

&nbsp;  - Aggregate metrics for reporting:

&nbsp;    - `voter\_county\_by\_state`: voters by state, gender, age metrics, missing emails, voters not voted in last year

&nbsp;    - `party\_affiliation\_distribution`: voters by party, gender, age metrics, missing emails, voters not voted in last year



---



\## Pipeline Status



\### Airflow \& dbt



| Airflow DAG Run | dbt Lineage Graph | dbt Tests (with intentional failures) |

|-----------------|-----------------|--------------------------------------|

| \[!\[Airflow DAG success](screenshots/airflow\_success.png)](screenshots/airflow\_success.png) | \[!\[dbt Lineage Graph](screenshots/dbt\_lineage\_graph.png)](screenshots/dbt\_lineage\_graph.png) | \[!\[dbt Tests](screenshots/dbt\_test\_with\_intentional\_failures.png)](screenshots/dbt\_test\_with\_intentional\_failures.png) |



---



\## Visualizations



\### Voter Counts



| Voter Count by State | Male vs Female Voters by State |

|---------------------|-------------------------------|

| \[!\[Voter Count by State](charts/voter\_count\_by\_state.png)](charts/voter\_count\_by\_state.png) | \[!\[Voter Gender by State](charts/voter\_gender\_by\_state.png)](charts/voter\_gender\_by\_state.png) |



\### Party Metrics



| Total Voters by Party |

|----------------------|

| \[!\[Voter Count by Party](charts/voter\_count\_by\_party.png)](charts/voter\_count\_by\_party.png) |



---



\## File Structure



goodparty\_voter\_pipeline/

│

├─ models/ # dbt models (staging, intermediate, marts)

├─ scripts/ # Python scripts for visualization

├─ charts/ # Generated visualizations

├─ screenshots/ # Pipeline screenshots

├─ dags/ # Airflow DAG definitions

├─ dbt\_project.yml # dbt project configuration

└─ README.md





\## Notes



\- Some dbt tests were intentionally left failing to demonstrate quality checks.

\- All states are standardized to 2-letter abbreviations.

\- Null states were removed to visualize better. They could be addressed elsewhere in the pipeline.

\- Visualization scripts generate charts in `charts/` using Matplotlib.

\- Clicking on any image will open the full-size PNG in a new tab.





