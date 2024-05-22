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
- LEAD_ID - INT - PK
- FIRST_NAME - STRING (Req)
- LAST_NAME - STRING (Req)
- EMAIL - STRING (Req)
- RESUME - STRING (Optional)

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

App is now running. Below you will find some tests to run


- Hello World:
Sanity test. verify a hello world response

```
curl http://localhost:8000

Response:
"hello world!"

```

- Test CREATE
```
curl -X POST "http://127.0.0.1:8000/create" -H "Content-Type: application/json" -d '{"FIRST_NAME": "John", "LAST_NAME": "Doe", "EMAIL": "john.doe@example.com", "RESUME": "This is a resume"}'

Response:
1

Info:
Creates a new Lead with name John Doe. The return is the lead_id of our new lead

```
- Test UPDATE
```
curl -X POST "http://127.0.0.1:8000/update?lead_id=1" -H "Content-Type: application/json" -d '{"FIRST_NAME": "Jeff", "LAST_NAME": "Meff", "EMAIL": "john.doe@example.com", "REACHED_OUT": "This is a resume"}'

Response:
1

Info:
Updates our leads name to Jeff Meff, adds a simple resume, 
and changes status to REACHED_OUT

```
- Test GET with Lead_id
```
curl "http://localhost:8000/get?lead_id=1"

Response:
[{"RESUME":"This is a resumeeee","LAST_NAME":"Meff","EMAIL":"john.doe@example.com","LEAD_ID":1,"FIRST_NAME":"Jeff","STATE":"PENDING"}]%

Info:
Retrieves our updated lead 1. note the name, resume and status change
```

- Test GET with invalid Lead_id
```
curl "http://localhost:8000/get?lead_id=7"

Response:
{"detail":"Lead with id 7 not found"}

Info:
Lead id 7 does not exist so gives us gentle reminder

```

- Test CREATE for a second lead
```
curl -X POST "http://127.0.0.1:8000/create" -H "Content-Type: application/json" -d '{"FIRST_NAME": "Apple", "LAST_NAME": "Bye", "EMAIL": "appleBye@gmail.com"}'


Response:
2

Info:
We have now added our second lead. the service returns our associated lead id

```


- Test GET without Lead_id
```
curl "http://localhost:8000/get"

Response:
[Jeff, Apple lead objects]

Info: 
Returns all leads in database. So far we only have 2
```
