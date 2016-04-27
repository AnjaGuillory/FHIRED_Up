import unittest

from fhired.User import User, auth


class UserTests(unittest.TestCase):
    def test_create_user(self):
        user = User("Tester", "t35t")

        self.assertTrue(user.is_authenticated())
        self.assertTrue(user.is_active())
        self.assertFalse(user.is_anonymous())
        self.assertEqual(u'Tester', user.get_id())

    def test_auth_user(self):
        user = auth("FHIRedUp", "PjV7kGTD")

        self.assertTrue(user.is_authenticated())
        self.assertTrue(user.is_active())
        self.assertFalse(user.is_anonymous())
        self.assertEqual(u'FHIRedUp', user.get_id())


if __name__ == "__main__":
    unittest.main()
