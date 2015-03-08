from . import PyramidMongoEngineTestCase


class TestSimpleApp(PyramidMongoEngineTestCase):

    def setUp(self):

        super(TestSimpleApp, self).setUp()

        from .apptest import main
        app = main({
            "mongodb_name": "dbapp_test",
            "mongo_url": "mongodb://localhost"
        })
        from webtest import TestApp
        self.app = TestApp(app)

        from .apptest import User
        params = {"email": "default@email.com", "username": "testerd"}
        User(**params).save()

    def tearDown(self):
        super(TestSimpleApp, self).tearDown()

        from .apptest import User
        User.drop_collection()

    def test_get_msg_app(self):
        res = self.app.get('/')

        self.assertEquals(200, res.status_code)
        self.assertEquals({"msg": "hello test app"}, res.json)

    def test_post_save_user(self):
        params = {"email": "test@email.com", "username": "tester"}
        res = self.app.post('/users/', params=params)

        json_res = res.json["user"]

        self.assertEquals(200, res.status_code)
        self.assertEquals(params["username"], json_res["username"])

    def test_get_all_users(self):
        res = self.app.get("/users/")

        self.assertEquals(1, len(res.json["users"]))

    def test_get_by_username(self):
        res = self.app.get("/user/testerd/get")
        user = res.json["user"]

        self.assertEquals(200, res.status_code)
        self.assertEquals(user["username"], "testerd")

    def test_get_not_found_username(self):
        res = self.app.get("/user/notfound/get", expect_errors=True)

        self.assertEquals(404, res.status_code)

    def test_get_first_user(self):
        res = self.app.get("/users/?first=true")
        user = res.json["users"]

        self.assertEquals(200, res.status_code)
        self.assertEquals(user["username"], "testerd")

    def test_get_first_user_not_found(self):
        from .apptest import User
        User.drop_collection()

        res = self.app.get("/users/?first=true", expect_errors=True)
        self.assertEquals(404, res.status_code)

    def test_delete_user(self):
        res = self.app.delete("/user/testerd/delete")
        self.assertEquals(200, res.status_code)

        res2 = self.app.get("/user/testerd/get", expect_errors=True)
        self.assertEquals(404, res2.status_code)
