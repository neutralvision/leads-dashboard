# leads-dashboard
alma ai leads dashboard backend


## Notes:
application should support creating, getting, and updating leads

A lead includes:
- first name
- last name
- email
- resume / CV

Each lead also has a STATE: (PENDING/REACHED_OUT)
this state is manually marked by attorney

## Design

Schema for Lead:
- LEAD_ID
- FIRST_NAME
- LAST_NAME
- EMAIL
- RESUME

Will assume the Resume is plain text for now, can double as CV.

Planning to go with **SQLLite** for persistence.

__Pros:__ 
- Very very easy to set up. Makes it easier to test

__Cons:__
- not super scalable. really bad at concurrent writes but thats not an issue for this project (i hope)
- migration from SQLLite to something like Postgres isnt 1to1, certain fields dont translate

### APIs:
#### /create 
    - submit json with required lead params. creates lead, sets status to PENDING, returns id
    - will start with no validation to see if lead already exists
    - add no duplicate emails if have time, can extend validation later

#### /get 
    - returns all leads
    - would be used to hydrate leads for internal UI
    - in future could add certain filters to return specific views of leads

#### /get{lead_id} 
    - returns data of specific lead id


#### /update{lead_id}
    - takes in json with required lead params.
    - verify that email doesnt exist for another user
    - update lead_id object to reflect updated lead. 
    - return lead_id if success

This can be a very dangerous api, originally planned to use /setReached{lead_id} api to allow safe
update to leads and only allow changing the STATE. But requirements does say updating leads should
be allowed so will allow all fields to be updated


### To Run

- Run `pip install -r requirements.txt`
- Run `uvicorn main:app --reload`
- 
- Test Curl: `curl http://localhost:8000`

- Test POST
```
curl -X POST "http://127.0.0.1:8000/create" -H "Content-Type: application/json" -d '{"FIRST_NAME": "John", "LAST_NAME": "Doe", "EMAIL": "john.doe@example.com", "RESUME": "This is a resume"}'
```
