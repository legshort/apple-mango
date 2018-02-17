from collections import defaultdict
from unittest import TestCase

from apple_mango import mango


class BDDTestCase(TestCase):
    def setUp(self):
        self.user = 'jun'

        # assert bdd module
        self.assertFalse(mango.whens)
        self.assertFalse(mango.thens)

        self.assertFalse(hasattr(self, 'when_call_stack'))
        self.assertFalse(hasattr(self, 'then_call_stack'))

        self.when_call_stack = defaultdict(list)
        self.then_call_stack = defaultdict(lambda: defaultdict(list))

    @mango.given('I am logged-in user')
    def test_profile(self):
        self.given.user_profile = 'my_profile'
        self.given.user_photo = 'my_photo'

        self.given.notifications_count = 3
        self.given.unread_notifications_count = 1

        self.given.name = 'I am logged-in user'

        @mango.when('I click profile')
        def when_a():
            print('click')

            self.when.name = 'I click profile'
            self.when_call_stack[self.given.name].append('I click profile')

            @mango.then('I see profile')
            def then_a():
                self.assertEqual(self.given.user_profile, 'my_profile')

                self.then_call_stack[self.given.name][self.when.name].append(
                    'I see profile')

            @mango.then('I see my photo')
            def then_b():
                self.assertEqual(self.given.user_photo, 'my_photo')

                self.then_call_stack[self.given.name][self.when.name].append(
                    'I see my photo')

        @mango.when('I click notification')
        def when_b():
            print('click')

            self.when.name = 'I click notification'
            self.when_call_stack[self.given.name].append(
                'I click notification')

            @mango.then('I see 3 notifications')
            def then_a():
                self.assertEqual(self.given.notifications_count, 3)

                self.then_call_stack[self.given.name][self.when.name].append(
                    'I see 3 notifications')

            @mango.then('I see 1 unread notification')
            def then_b():
                self.assertEqual(self.given.unread_notifications_count, 1)

                self.then_call_stack[self.given.name][self.when.name].append(
                    'I see 1 unread notification')

    @mango.given('I am logged-out user')
    def test_auth(self):
        self.given.status_code = 401

        self.given.name = 'I am logged-out user'

        @mango.when('I access profile by url')
        def when():
            print('access profile')

            self.when.name = 'I access profile by url'
            self.when_call_stack[self.given.name].append(self.when.name)

            @mango.then('I see 401 error')
            def then():
                self.assertEqual(self.given.status_code, 401)
                self.then_call_stack[self.given.name][self.when.name].append(
                    'I see 401 error')

    @mango.given()
    def test_default_given_desc(self):
        @mango.when()
        def when():
            @mango.then()
            def then():
                pass

    def tearDown(self):
        # assert bdd module
        expect_then_call_stack = {
            'I am logged-in user': {
                'I click profile': ['I see profile', 'I see my photo'],
                'I click notification': ['I see 3 notifications', 'I see 1 unread notification']
            },
            'I am logged-out user': {
                'I access profile by url': ['I see 401 error']
            }
        }

        for called_given, called_whens in self.when_call_stack.items():
            self.assertListEqual(called_whens, list(
                expect_then_call_stack[called_given].keys()))

        for called_given, called_whens_thens in self.then_call_stack.items():
            self.assertDictEqual(called_whens_thens,
                                 expect_then_call_stack[called_given])

        self.assertFalse(mango.whens)
        self.assertFalse(mango.thens)
