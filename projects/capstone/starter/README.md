# Backend - Casting Agency API

## Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 
You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

### Models:
- Movies with attributes title and release date
- Actors with attributes name, age and gender

### Endpoints:
- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/

### Roles:
1. **Casting Assistant**
- Can view actors and movies

2. **Casting Director**
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies

3. **Executive Producer**
- All permissions a Casting Director has and…
- Add or delete a movie from the database

### Tests:
One test for success behavior of each endpoint
One test for error behavior of each endpoint
At least two tests of RBAC for each role


## Motivation
Use all of the concepts and the skills taught in the courses to build an API from start to finish and host it:

- Coding in Python 3
- Relational Database Architecture
- Modeling Data Objects with SQLAlchemy
- Internet Protocols and Communication
- Developing a Flask API
- Authentication and Access
- Authentication with Auth0
- Authentication in Flask
- Role-Based Access Control (RBAC)
- Testing Flask Applications
- Deploying Applications

## URL location for the hosted API
**Heroku git URL:** https://git.heroku.com/heroku-capstone-444y.git

## Getting Started

### Install Dependencies

#### Python 3.10

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Tasks

### Setup Auth0

1. Create an account with [Auth0] (https://auth0.com/)
2. Select a unique tenant domain
3. Create a new Regular Web Application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token

5. Create new API permissions:
    - `get:movies`
    - `post:movies`
    - `patch:movies`
    - `delete:movies`
    - `get:actors`
    - `post:actors`
    - `patch:actors`
    - `delete:actors`

6. Create new roles for
    - Casting Assistant: 
        - can `get:movies`
        - can `get:actors`
    - Casting Director: 
        - can perform all actions other than `post:movies` and `delete:movies`
    - Executive Producer:
        - can perform all actions

7. Acquire JWT's one for each role
   - Register 3 users - assign each of the roles in Step 6 to one user.
   - Visit https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}.  For example, https://dev-6lmvbxfp.us.auth0.com/authorize?audience=castingAgency&response_type=token&client_id=4nbbZSXgwwimOU7aYfJHGedqlwFLCMuX&redirect_uri=http://localhost:8080/login-results
   - Sign into each account (one role, one account) and make note of the JWT.

### Setup Heroku
1. Create an account with [Heroku](https://signup.heroku.com/)
2. Download/install the Heroku CLI (Command Line Interface) 
3. Log into Heroku acount with the following command
```
heroku login -i
```

### Local Run
Run the Flask app locally so that you will know the expected behavior after the app is deployed on the Heroku cloud.  You should have Git installed on your local machine.  The prerequisite to running the app locally is to have a PostgreSQL database available in your local, and the Postgres server must be up and running.  With Postgres running, create a `capstone` database:

```bash
createdb capstone
```

- Create a project directory (e.g., <abc>/FSND/projects/capstone/starter)
- Create a virtual environment that will help you keep the Python packages isolated from the ones already installed in your local machine.
```
python3 -m venv myvenv
source myvenv/bin/activate
```
- Set up the environment variables
```
# You should have setup.sh and requirements.txt available
chmod +x setup.sh
source setup.sh
# The setup.sh will run the following:
# export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres"
# export EXCITED="true"
# Change the DATABASE_URL, as applicable to you.
echo $DATABASE_URL
# postgresql://postgres:postgres@localhost:5432/postgres
echo $EXCITED
# true
```
- Install the Python dependencies
```
pip install -r requirements.txt
# Run the app
python3 app.py
```
If the command above runs successfully, you can view the output at http://127.0.0.1:5000/

- Test your app locally 
   - Write at least one test for the success and at least one error behavior of each endpoint using the unittest library in the **test_app.py**
   - Use the noted JWT in Request Headers to test each endpoint
   - Run the tests and correct any errors.  To deploy the tests, run 
   ```
   python3 test_app.py
   ``` 
- Migrate your local database to another database in the Heroku cloud, you will have to run these commands:
```
# Create a app/migration repository
python manage.py db init
python manage.py db migrate -m "Initial migration"
# Create the migrations locally, and later, commit and deploy to Heroku
python manage.py db upgrade
```

### Deployment Instructions
1. Initialize Git
Initialize a git repository and make a commit:
```
# Run it just once, in the beginning
git init
# For the first time commit, you need to configure the git username and email:
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

2. Create an App in Heroku Cloud
Create /app directory in the Heroku platform
```
heroku create [my-app-name] --buildpack heroku/python
# For example, 
# heroku create myapp-663697908 --buildpack heroku/python
# https://myapp-663697908.herokuapp.com/ | https://git.heroku.com/myapp-663697908.git
```
where, [my-app-name] is a unique name that nobody else on Heroku has already used. You have to define the build environment using the option --buildpack heroku/python The heroku create command will create a Git "remote" repository on Heroku cloud and a web address for accessing your web app. You can check that a remote repository was added to your git repository with the following terminal command:
```
git remote -v
```
If you cannot see the Heroku "remote" repository URL in the output, you can use the command:
```
git remote add heroku [heroku_remote_git_url]
```
If you check your Heroku Dashboard in the browser, you'll see an application by that name. But it doesn't have our code or anything yet - it's completely empty. Let's get our code up there.

3. Add PostgreSQL addon for our database
Heroku has an addon for apps for a postgresql database instance. Run this code in order to create your database and connect it to your application:
```
heroku addons:create heroku-postgresql:hobby-dev --app [my-app-name]
```
In the command above,
- `heroku-postgresql` is the name of the addon that will create an empty Postgres database.
- `hobby-dev` on the other hand specifies the tier of the addon, in this case the free version which has a limit on the amount of data it will store, albeit fairly high.

4. Configure the App
After the database has been created, you would want to set up the Environment variables in the Heroku Cloud, specific to your application. Run the following command to fix your DATABASE_URL configuration variable in Heroku.
```
heroku config --app [my-app-name]
# DATABASE_URL:
# postgres://xjlhouchsdbnuw:0e9a708916e496be7136d0eda4c546253f1f5425ec041fd6e3efda3a1f819ba2@ec2-35-175-68-90.compute-1.amazonaws.com:5432/d3mrjpmsi4vvn1
```

5. Additional Environment Variables

- Copy the DATABASE_URL generated from the step above, and update your local DATABASE_URL environment variable:
```
export DATABASE_URL="postgres://xjlhouchsdbnuw:0e9a708916e496be7136d0eda4c546253f1f5425ec041fd6e3efda3a1f819ba2@ec2-35-175-68-90.compute-1.amazonaws.com:5432/d3mrjpmsi4vvn1"
# Verify
echo $DATABASE_URL
# postgres://xjlhouchsdbnuw:0e9a708916e496be7136d0eda4c546253f1f5425ec041fd6e3efda3a1f819ba2@ec2-35-175-68-90.compute-1.amazonaws.com:5432/d3mrjpmsi4vvn1
```
- Apart from the DATABASE_URL, for the sample project, add one additional variable to the Heroku app: 'EXCITED'.

- Go to your Heroku Dashboard in the browser and access your application's settings. You will have to go to the **Heroku dashboard >> Particular App >> Settings >> Reveal Config Vars** section and save the EXCITED variable and its value as `true` (all lowercase).

6. Push it!
Whenever you make any changes to your application folder contents, you will have to commit your changes:
```
# Every time you make any edits to any file in the web_app folder
# Check which files are ready to be committed
git add -A
git status
git commit -m "your message"
```
Now, push your changes. The push will trigger a heroku build automatically.
```
# Assuming you have already committed all your local edits.
git push heroku master
```
**Don't forget to push each time you make edits locally.**

7. Migrate the database
```
heroku run python manage.py db upgrade --app [my-app-name]
```
8. That's it.  Open the application from your Heroku Dashboard and see it work live!

## Documentation of API behavior and RBAC controls

All endpoints require
```json
{ 
    "Authorization": "Bearer <JWT>"
}
``` 
in Request Headers

### `GET '/movies'`
- Retrieves movies
- Request Arguments: None
- Returns: An object with a list of movies
```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "11/21/2021",
            "title": "Cats Revenge",
        },
        {
            "id": 2,
            "release_date": "11/21/2021",
            "title": "Dogs Gone Wild",
        }
    ]
}
```

### `POST '/movies'`
- Adds a new movie
- Request Body:
```json
{
    "release_date": "01/06/2023",
    "title": "Strange Pets"
}
```
- Returns: An object with a list of only the newly added movie
```json
{
    "movies": [
        {
            "id": 3,
            "release_date": "01/06/2023",
            "title": "Strange Pets"
        }
    ]
}
```

### `PATCH '/movies/<int:id>'`
- Update the movie specified by `id` request argument
- Request Arguments: `id` - integer
- Request Body:
```json
{
    "release_date": "07/27/2027",
    "title": "Strange Pets"
}
```
- Returns: An object with a list of only the updated movie
```json
{
    "movies": [
        {
            "id": 3,
            "release_date": "07/27/2027",
            "title": "Strange Pets"
        }
    ]
}
```

### `DELETE '/movies/<int:id>'`
- Deletes a specified movie where `id` is the existing movie `id`
- Request Arguments: `id` - integer
- Returns: An object with `id` of the deleted movie
```json
{
    "deleted_id": 3
}
```

### `GET '/actors'`
- Retrieves actors
- Request Arguments: None
- Returns: An object with a list of actors
```json
{
    "actors": [
        {
            "age": 21,
            "gender": "Female",
            "id": 1,
            "name": "Penny Hall"
        },
        {
            "age": 25,
            "gender": "Male",
            "id": 2,
            "name": "Henry Hall"
        },
    ]
}
```

### `POST '/actors'`
- Adds a new actor
- Request Body:
```json
{
    "age": 55,
    "gender": "Male",
    "name": "Kitty Hall"
}
```
- Returns: An object with a list of only the newly added actor
```json
{
    "actors": [
        {
            "age": 55,
            "gender": "Male",
            "id": 3,
            "name": "Kitty Hall"
        }
    ]
}
```

### `PATCH '/actors/<int:id>'`
- Update the actor specified by `id` request argument
- Request Arguments: `id` - integer
- Request Body:
```json
{
    "age": 56,
    "gender": "Male",
    "name": "Kitty Hall"
}
```
- Returns: An object with a list of only the updated actor
```json
{
    "actors": [
        {
            "age": 56,
            "gender": "Male",
            "id": 3,
            "name": "Kitty Hall"
        }
    ]
}
```

### `DELETE '/actors/<int:id>'`
- Deletes a specified actor where `id` is the existing actor `id`
- Request Arguments: `id` - integer
- Returns: An object with `id` of the deleted actor
```json
{
    "deleted_id": 3
}
```


