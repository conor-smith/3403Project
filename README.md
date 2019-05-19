# 3403Project

The purpose of this website is for users to rank movies preferentially and then compare their rankings against everyone else in the website. 
The main theme we had in mind when creating this website was avoiding choice paralysis. This website would be curated by small team with only a few (<=10) polls available to vote on at one time. These polls would be rotated out regularly (weekly, biweekly, etc.), replaced with new polls created by the admin team. 
To avoid dissatisfaction from the userbase due to movies they believe should be included, the movies
in the polls should be chosen based on a mix of critical reception and/or audience reception. More specific topics
are also great for avoiding this issue as the likely candidate pool would shrink (e.g: The best movie of 2019 vs The best movie sound design of 2019). This would also get users thinking more deeply about movies.

## Architecture
the architecture of the web application

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

- flask-wtf
- Flask-SQLAlchemy
- Flask-Migrate
- python-dotenv
- flask-login
- flask-admin
- Pillow


### Installing

There is an included python virtual environment that was used to run this server.  However if you wish to use your own,
below is instructions on how to do so. You will need to be in the virtual environment whenever you 
#### Step 1a. Using the included virtual environment
asdas

OR

#### Step 1b. Creating a python virtual environment
asdas

#### Step 2. Initializing the database
Use the following commands in order:
- <code>flask db init</code>
- <code>flask db migrate</code>
- <code>flask db upgrade</code>

#### Step 3. Adding an admin account
- Open the python interpreter using <code>python</code> or <code>python3</code>
- Replace "USERNAME" with your desired username and "PASSWORD" with your desired password in the following commands
- Use the following commands in order:
  - <code>from app import db</code>
  - <code>from app.models import User</code>
  - <code>u = User(username='USERNAME', admin = 1)</code>
  - <code>u.set_password('PASSWORD')</code>
  - <code>db.session.add(u)</code>
  - <code>db.session.commit()</code>
Once you have added the first admin account, adding further admin accounts is made easy using the User page of the admin view of the website.

#### Step 4. Starting then server
Simply use <code>flask run</code> to start the server. You can then head to 
[localhost:5000](localhost:5000) or [127.0.0.1:5000](127.0.0.1:5000) to see the website in action.

## Running the tests

- describe some unit tests for the web application, and how to run them.

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Bootstrap](https://getbootstrap.com/) - Javascript Library
* [Jquery](https://jquery.com/) - Javascript Library
* [Flask](http://flask.pocoo.org/) - Web Framework

## Authors

* **Billtone Mey Oum** - *Initial work* - [billmey](https://github.com/billmey)
* **Conor Smith** - *Initial work* - [conor-smith](https://github.com/conor-smith)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the GNU General Public License v3.0 or later - see the [LICENSE.md](LICENSE) file for details

## Acknowledgments

* [PurpleBooth](https://gist.github.com/PurpleBooth) for the readme template
* Hat tip to anyone whose code was used
* Inspiration
* etc

## Commit Logs
