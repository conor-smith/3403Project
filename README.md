# 3403Project

The purpose of this website is for users to rank movies preferentially and then compare their rankings against everyone else in the website. 
The main theme we had in mind when creating this website was avoiding choice paralysis. This website would be curated by small team with only a few (<=10) polls available to vote on at one time. These polls would be rotated out regularly (weekly, biweekly, etc.), replaced with new polls created by the admin team. 
To avoid dissatisfaction from the userbase due to movies they believe should be included, the movies
in the polls should be chosen based on a mix of critical reception and/or audience reception. More specific topics
are also great for avoiding this issue as the likely candidate pool would shrink (e.g: The best movie of 2019 vs The best movie sound design of 2019). This would also get users thinking more deeply about movies.
Sidenote: We had initially intended to rank  multiple forms of media (movies, music and games) but we scaled down due to time constraints and overcomplexity. This is why in the code, we refer to movies as media.
TODO explain social mechanism/voting mechanism used.

## Architecture
TODO the architecture of the web application

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes (tested on Linux and macOS).

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
- Open add_admin.py and replace 'admin' in <code>u = User(username='admin', admin = 1)</code> with your desired username 
  and replace 'admin' in <code>u.set_password('admin')</code> with your desired password
- Then use <code>python add_admin.py</code> to add the admin account
  
Once you have added the first admin account, adding further admin accounts is made easy using the User page of the admin view of the website.

#### Step 4. Starting then server
Simply use <code>flask run</code> to start the server. You can then head to 
[localhost:5000](localhost:5000) or [127.0.0.1:5000](127.0.0.1:5000) to see the website in action.

## Running the tests
To run the unit tests, use <code>python testing.py</code> 
When the unit tests are finished you will need to:
- <code>flask db migrate</code> 
- <code>flask db upgrade</code>

to rebuild the database.
### Break down into end to end tests
#### User function tests
- test_set_password
  * Tests ability to assign and hash a password to a user
- test_delete_account
  * Tests ability to delete a user
- test_already_voted
  * Tests ability to check if a user has already voted on the poll passed to the function
- test_remove_user_poll
  * Tests ability to remove previous votes made on the poll passed to the function
- test_all_polls
  * Tests ability to return all polls a user has participated in
- test_poll_results
  * Tests ability to return results of a poll if the user has participated in it
#### Poll function tests
- test_add_media
  * Tests ability to add media to a poll
- test_remove_media
  * Tests ability to remove media from a poll
- test_voters
  * Tests ability to return all participants of a poll
- test_totals
  * Tests ability to return global (multiuser) rankings of a poll
- test_contains
  * Tests ability to chcek if a poll contains a certain media 
- test_cover
  * Tests ability to return the first movie poster of a poll
- test_close_all
  * Tests ability to deactivate all active polls (i.e. archive polls)
#### Routes function tests
- test_front
  * Tests that the front page functions
- test_about_us
  * Tests that the about us page functions
- test_login_logout
  * Tests that the login and logout functionality works
- test_archives
  * Tests that the archives page doesn't allow users not logged in
- test_register
  * Tests that the register page functions
- test_missing
  * Tests that the 404 page displays properly

## Built With
* [Bootstrap](https://getbootstrap.com/) - Javascript Library
* [Jquery](https://jquery.com/) - Javascript Library
* [Flask](http://flask.pocoo.org/) - Web Framework
* and of course good 'ol HTML, CSS and Javascript

## Authors
* **Billtone Mey Oum (21806052)** - *Initial work* - [billmey](https://github.com/billmey)
* **Conor Smith (21959981)** - *Initial work* - [conor-smith](https://github.com/conor-smith)

## License
This project is licensed under the GNU General Public License v3.0 or later - see the [LICENSE.md](LICENSE) file for details

## Acknowledgments
* [PurpleBooth](https://gist.github.com/PurpleBooth) for the readme template
* [IMP Awards](http://www.impawards.com/) for various movie posters
* [Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) for the mega tutorial

## Commit Logs
