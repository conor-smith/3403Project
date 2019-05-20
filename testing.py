import unittest, os
from app import app, db, routes, models, forms
from app.models import User, Media, Poll

class TestProject(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        class Config(object):
            SECRET_KEY = os.environ.get("SECRET_KEY") or "HV4gKFWjPz"
            SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
            SQLALCHEMY_TRACK_MODIFICATIONS = False
        app.config.from_object(Config)
        self.app = app.test_client()
        db.create_all()
        # Users
        testadmin = User(username='testadmin', admin=1)
        testadmin.set_password('admin')
        testuser = User(username='testuser')
        testuser.set_password('user')
        db.session.add(testadmin)
        db.session.add(testuser)
        # Movies
        testmovie1 = Media(title='testmovie1', poster="img/test.jpg")
        testmovie2 = Media(title='testmovie2')
        testmovie3 = Media(title='testmovie3')
        testmovie4 = Media(title='testmovie4')
        testmovie5 = Media(title='testmovie5')
        db.session.add(testmovie1)
        db.session.add(testmovie2)
        db.session.add(testmovie3)
        db.session.add(testmovie4)
        db.session.add(testmovie5)
        # Polls
        testpoll1 = Poll(name='testpoll1',creator=testadmin.id)
        testpoll1.add_media(testmovie1)
        testpoll1.add_media(testmovie2)
        testpoll1.add_media(testmovie3)
        testpoll1.add_media(testmovie4)
        testpoll1.add_media(testmovie5)
        testpoll2 = Poll(name='testpoll2',creator=testadmin.id)
        testpoll2.add_media(testmovie1)
        testpoll2.add_media(testmovie3)
        testpoll2.add_media(testmovie5)

        db.session.add(testpoll1)
        db.session.add(testpoll2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # User function tests
    def test_set_password(self):
        u = User.query.filter_by(username = "testuser").first()
        u.set_password('test')
        self.assertFalse(u.check_password("case"))
        self.assertTrue(u.check_password("test"))

    def test_delete_account(self):
        u = User.query.filter_by(username = "testuser").first()
        u.delete_account()
        self.assertIsNone(User.query.filter_by(username = "testuser").first())
        self.assertIsNotNone(User.query.filter_by(username = "testadmin").first())

    def test_already_voted(self):
        u = User.query.filter_by(username = "testuser").first()
        p = Poll.query.filter_by(name = "testpoll1").first()
        p2 = Poll.query.filter_by(name = "testpoll2").first()
        u.vote_on_media(p,p.choices[0],5)
        u.vote_on_media(p,p.choices[1],4)
        u.vote_on_media(p,p.choices[2],3)
        u.vote_on_media(p,p.choices[3],2)
        u.vote_on_media(p,p.choices[4],1)
        self.assertTrue(u.already_voted(p))
        self.assertFalse(u.already_voted(p2))

    def test_remove_user_poll(self):
        u = User.query.filter_by(username = "testuser").first()
        p = Poll.query.filter_by(name = "testpoll1").first()
        u.vote_on_media(p,p.choices[0],5)
        u.vote_on_media(p,p.choices[1],4)
        u.vote_on_media(p,p.choices[2],3)
        u.vote_on_media(p,p.choices[3],2)
        u.vote_on_media(p,p.choices[4],1)
        p2 = Poll.query.filter_by(name = "testpoll2").first()
        u.vote_on_media(p2,p2.choices[0],2)
        u.vote_on_media(p2,p2.choices[1],3)
        u.vote_on_media(p2,p2.choices[2],1)
        u.remove_user_poll(p)
        db.session.commit()
        self.assertFalse(u.already_voted(p))
        self.assertTrue(u.already_voted(p2))

    def test_all_polls(self):
        u = User.query.filter_by(username = "testuser").first()
        p = Poll.query.filter_by(name = "testpoll1").first()
        p2 = Poll.query.filter_by(name = "testpoll2").first()
        u.vote_on_media(p,p.choices[0],5)
        u.vote_on_media(p,p.choices[1],4)
        u.vote_on_media(p,p.choices[2],3)
        u.vote_on_media(p,p.choices[3],2)
        u.vote_on_media(p,p.choices[4],1)
        self.assertIn(p,u.all_polls())
        self.assertNotIn(p2,u.all_polls())
    
    def test_poll_results(self):
        u = User.query.filter_by(username = "testuser").first()
        p = Poll.query.filter_by(name = "testpoll1").first()
        u.vote_on_media(p,p.choices[0],5)
        u.vote_on_media(p,p.choices[1],4)
        u.vote_on_media(p,p.choices[2],3)
        u.vote_on_media(p,p.choices[3],2)
        u.vote_on_media(p,p.choices[4],1)
        self.assertIn({"Media" : p.choices[0], "Score" : 5},u.poll_results(p))
        self.assertNotIn({"Media" : p.choices[1], "Score" : 2},u.poll_results(p))

    # Poll function tests
    def test_add_media(self):
        p = Poll.query.filter_by(name = "testpoll2").first()
        m = Media.query.filter_by(title = "testmovie2").first()
        self.assertTrue(p.add_media(m))
        self.assertFalse(p.add_media(m))

    def test_remove_media(self):
        p = Poll.query.filter_by(name = "testpoll2").first()
        m = Media.query.filter_by(title = "testmovie2").first()
        p.add_media(m)
        self.assertTrue(p.remove_media(m))
        self.assertFalse(p.remove_media(m))

    def test_voters(self):
        u = User.query.filter_by(username = "testuser").first()
        p = Poll.query.filter_by(name = "testpoll1").first()
        p2 = Poll.query.filter_by(name = "testpoll2").first()
        u.vote_on_media(p,p.choices[0],5)
        u.vote_on_media(p,p.choices[1],4)
        u.vote_on_media(p,p.choices[2],3)
        u.vote_on_media(p,p.choices[3],2)
        u.vote_on_media(p,p.choices[4],1)
        self.assertIn(u, p.voters())
        self.assertNotIn(u, p2.voters())

    def test_totals(self):
        u = User.query.filter_by(username = "testuser").first()
        a = User.query.filter_by(username = "testadmin").first()
        p = Poll.query.filter_by(name = "testpoll1").first()
        u.vote_on_media(p,p.choices[0],5)
        u.vote_on_media(p,p.choices[1],4)
        u.vote_on_media(p,p.choices[2],3)
        u.vote_on_media(p,p.choices[3],2)
        u.vote_on_media(p,p.choices[4],1)
        a.vote_on_media(p,p.choices[0],5)
        a.vote_on_media(p,p.choices[1],4)
        a.vote_on_media(p,p.choices[2],3)
        a.vote_on_media(p,p.choices[3],2)
        a.vote_on_media(p,p.choices[4],1)
        t = p.totals()
        self.assertEqual(t[0], {'Media': p.choices[0], 'GlobalScore': 10})
        self.assertEqual(t[3], {'Media': p.choices[3], 'GlobalScore': 4})

    def test_contains(self):
        p = Poll.query.filter_by(name = "testpoll2").first()
        m = Media.query.filter_by(title = "testmovie1").first()
        m2 = Media.query.filter_by(title = "testmovie2").first()
        self.assertTrue(p.contains(m))
        self.assertFalse(p.contains(m2))

    def test_cover(self):
        p = Poll.query.filter_by(name = "testpoll1").first()
        self.assertEqual("img/test.jpg", p.choices[0].poster)
        self.assertEqual("img/poster.png", p.choices[1].poster)

    def test_close_all(self):
        p = Poll.query.filter_by(name = "testpoll1").first()
        p2 = Poll.query.filter_by(name = "testpoll2").first()
        Poll.close_all()
        db.session.commit()
        self.assertEqual(False, p.active)
        self.assertEqual(False, p2.active)

    #def test_delete_poll(self):
    #    p = Poll.query.filter_by(name = "testpoll2").first()
    #    p.delete_poll()
    #    self.assertIsNone(Poll.query.filter_by(name = "testpoll2").first())

    # Media function tests
    #def test_delete_media(self):
    #    m = Media.query.filter_by(title = "testmovie1").first()
    #   m.delete_media()
    #    self.assertIsNone(Media.query.filter_by(title = "testmovie1").first())


if __name__ == '__main__':
    unittest.main()