# leads-dashboard
alma ai leads dashboard backend


## Notes:
application should support creating, getting, and updating leads

A lead includes:
- first name
- last name
- email
- resume / CV

Each lead also has a STATE: (PENDING / REACHED_OUT)
this state is manually marked by attorney
---
## Design

## Lead Schema

The `Lead` model represents a lead in the system with the following attributes:

| Column Name | Data Type | Description                  | Required |
|-------------|------------|------------------------------|----------|
| `LEAD_ID`   | `INT`      | Primary Key                  | Yes      |
| `FIRST_NAME`| `STRING`   | First name of the lead       | Yes      |
| `LAST_NAME` | `STRING`   | Last name of the lead        | Yes      |
| `EMAIL`     | `STRING`   | Email address of the lead    | Yes      |
| `RESUME`    | `STRING`   | Resume of the lead           | No       |


Will assume the Resume is plain text for now, can double as CV.

Planning to go with **SQLLite** for persistence.

__Pros:__ 
- Very very easy to set up. Makes it easier to test

__Cons:__
- not super scalable. really bad at concurrent writes but thats not an issue for this project (i hope)
- migration from SQLLite to something like Postgres isnt 1to1, certain fields dont translate

### APIs:
#### `/create `
- submit json with required lead params. creates lead, sets status to PENDING, returns id
- will start with no validation to see if lead already exists
- add no duplicate emails if have time, can extend validation later

#### `/get `
- returns all leads
- would be used to hydrate leads for internal UI
- in future could add certain filters to return specific views of leads

#### `/get{lead_id} `
- returns data of specific lead id


#### `/update{lead_id}`
- takes in json with required lead params.
- TODO: verify that email doesnt exist for another user
- update lead_id object to reflect updated lead. 
- return lead_id if success

    /update can be a very dangerous api, originally planned to use /setReached{lead_id} api to allow safe
    update to leads and only allow changing the STATE. But requirements does say updating leads should
    be allowed so will allow all fields to be updated


To structure this project, Ive split into 3 logical files.
One for main service logic, one for db setup, one for models. splitting it this way from experience.
should be enough separation for now.

---
## To Run

- Run `pip install -r requirements.txt`
- Run `uvicorn main:app --reload`

You are live! Look below for some test curl commands. Run these in order for a walkthrough.
You'll need a fresh db for these to run correctly. just delete your `leads.db` file to reset.


- Sanity Test

```
curl http://localhost:8000

Response:
"hello world!"

Info:
Basic ping test. if you see the correct response, continue onto the next!
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
[{"LAST_NAME":"Meff","EMAIL":"john.doe@example.com","STATE":"PENDING","RESUME":"This is a resume","FIRST_NAME":"Jeff","LEAD_ID":1}]%

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
[{"LAST_NAME":"Meff","EMAIL":"john.doe@example.com","STATE":"PENDING","RESUME":"This is a resume","FIRST_NAME":"Jeff","LEAD_ID":1},{"LAST_NAME":"Bye","EMAIL":"appleBye@gmail.com","STATE":"PENDING","RESUME":null,"FIRST_NAME":"Apple","LEAD_ID":2}]  

Info: 
Returns all leads in database. So far we only have these 2
```


## Recap
A handful of assumptions have been made for this project.
I am assuming low scale, simple objects, and assuming a UI would be created to fit my specifications.

My biggest challenge with this project is knowing how much effort to put into it? I have a very solid simple service
but not sure if something way over the top is being looked for. given the requirements i hope this is fine

Thank you for reviewing my code!
