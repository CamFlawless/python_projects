## Podio API - Data Extraction Script
This project is inteneded to provide a means of extracting the underlying data from applications and its items using the [Podio API](https://developers.podio.com/) and [PyPodio2](https://github.com/podio/podio-pyc) python library. 


### <ins> Outstanding Tasks & Goals </ins>
- [x] Make connection with API using credentials
- [x] Retrieve items from applications
- [x] Identify structure of object returned for application items
- [ ] Remove need to explicitly state field_id values and field_name descriptions
  - [ ] Instead, loop through the returned items and use the included field_id and labels
  - [ ] That way, it can grow or shrink depending on which fields are used between items
- [ ] Set-up process automation to re-ping API @ 15 minute intervals
- [ ] Migrate cleaned data from API into AWS RDS PostGres DB
