# 3403Project

The purpose of this website is for users to rank movies preferentially and then compare their rankings against everyone else in the website. 
The main theme we had in mind when creating this website was avoiding choice paralysis. This website would be curated by small team with only a few (<=10) polls available to vote on at one time. These polls would be rotated out regularly (weekly, biweekly, etc.), replaced with new polls created by the admin team. 
To avoid dissatisfaction from the userbase due to movies they believe should be included, the movies
in the polls should be chosen based on a mix of critical reception and/or audience reception. More specific topics
are also great for avoiding this issue as the likely candidate pool would shrink (e.g: The best movie of 2019 vs The best movie sound design of 2019). This would also get users thinking more deeply about movies.

The voting page for each poll consists of a set of all the movie "posters", or which may be dvd covers or images of the actual movie posters. The user selects them in the order they feel best fits the poll. (eg: For the best sci-fi horror poll, I select Event Horizon first, followed by Alien, etc).
To prevent confusion, when an option is selected, it disappears, meaning it can not be selected again or unselected. If the user is unhappy with their choices, they may choose to participate again. Doing so will remove all all their previous votes for that particular poll before starting.
Each movie is assigned a number when the user votes for them, from 1 to however many movies are in the poll (no more than 10). Once this has been done. The data is stored in a votes table. These votes can be aggregated to produce the global results for a particular poll.

## Architecture
TODO the architecture of the web application

## Getting Started
TODO fill out OS versions
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes (tested on Windows, Linux and macOS 10.14.4). See deployment for notes on how to deploy the project on a live system.

### Prerequisites
While in your virtual environment, install the following:
- [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/)
  * <code>pip install flask-wtf</code>
- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
  * <code>pip install flask-sqlalchemy</code>
- [Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate)
  * <code>pip install flask-migrate</code>
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
  * <code>pip install flask-login</code>
- [Flask-Admin](https://flask-admin.readthedocs.io/en/latest/)
  * <code>pip install flask-admin</code>
- [Pillow](https://pillow.readthedocs.io/en/stable/)
  * <code>pip install pillow</code>
- [python-dotenv](https://github.com/theskumar/python-dotenv#installation)
  * <code>pip install -U python-dotenv</code>

### Installing
You will need to be in a virtual environment whenever you run the server or follow the below instructions. 
You <em>can</em> run it without one, but we are not responsible if anything goes wrong.
#### Step 1 Creating a python virtual environment
TODO

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

- TODO describe some unit tests for the web application, and how to run them.

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
* and of course good 'ol HTML, CSS and Javascript

## Authors
TODO Student number
* **Billtone Mey Oum (21806052)** - *Initial work* - [billmey](https://github.com/billmey)
* **Conor Smith ()** - *Initial work* - [conor-smith](https://github.com/conor-smith)

## License

This project is licensed under the GNU General Public License v3.0 or later - see the [LICENSE.md](LICENSE) file for details

## Acknowledgments
TODO other references go here like poster image sources
* [PurpleBooth](https://gist.github.com/PurpleBooth) for the readme template
* Hat tip to anyone whose code was used
* Inspiration
* etc

## Commit Logs
