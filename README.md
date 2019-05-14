# 3403Project

TODO:
- the purpose of the web application, explaining both the context and the social choice mechanism used.
- the architecture of the web application
- describe how to launch the web application.
- describe some unit tests for the web application, and how to run them.
- Include commit logs, showing contributions and review from both contributing students 

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


### Installing

A step by step series of examples that tell you how to get a development env running

#### To add admin account
- in project directory
- go into your virtual environment (if needed)
- open the python interpreter using 'python'
- do the following commands
  - from app import db
  - from app.models import User
  - u = User(username='usern', admin = 1)
  - u.set_password('pword')
  - db.session.commit()
  - db.session.add(u)
  - db.session.commit()
- replace "usern" with your desired username and "pword" with your desired password

#### To init db:
- flask db init
- flask db migrate
- flask db upgrade

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

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

