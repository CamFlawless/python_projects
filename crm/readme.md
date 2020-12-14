## Podio API - Data Extraction Script
This project is inteneded to provide a means of extracting the underlying data from applications and its items using the [Podio API](https://developers.podio.com/) and [PyPodio2](https://github.com/podio/podio-pyc) python library. 


### <ins> Tasks & Goals </ins>
**Completed** 
- [x] Make connection with API using credentials
- [x] Retrieve items from applications
- [x] Identify structure of object returned for application items
- [x] Push returned (and cleansed) data into a locally hosted PostgresSQL database

**Outstanding**
- [ ] Remove need to explicitly state field_id values and field_name descriptions
  - [ ] Iterate through items returned and generate list of available fields in dynamic means -- not explicitly stating them
- [ ] Set-up process automation to re-ping API @ 15 minute intervals
- [ ] Migrate cleaned data from API into AWS RDS PostGres DB
