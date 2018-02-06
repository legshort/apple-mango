# Light weight BDD Pattern

## Installation
* `pip install apple-mango`

## Goal
* Easy to Use
* Compatible with Python unittest
* Compatible with existing test code
* Support Python3

## Next Step
* Register to pypi
* Add CI
* Support pytest

## Usage
* Define regular test class
* Define regular test method with `@mango.given()`
* Define inner `when` method with `@mango.when()`
* Define inner `then` method with `@mango.then()`
* Run python test: `python -m unittest test_file.py`
* No need to call inner `when` and `then` method becuase `given(), when(), then()` decorators will take care of it

### Example
```python
# test_exampel.py

class MangoUseCase(TestCase):
    def setUp(self):
        self.user = 'jun'

    @mango.given('I am logged-in user')
    def test_profile(self):
        self.given.user_profile = 'my_profile'
        self.given.user_photo = 'my_photo'

        self.given.notifications_count = 3
        self.given.unread_notifications_count = 1

        @mango.when('I click profile')
        def when_click_profile():
            print('click')

            @mango.then('I see profile')
            def then_profile():
                self.assertEqual(self.given.user_profile, 'my_profile')

            @mango.then('I see my photo')
            def then_photo():
                self.assertEqual(self.given.user_photo, 'my_photo')

        @mango.when('I click notification')
        def when_click_notification():
            print('click')

            @mango.then('I see 3 notifications')
            def then_notification():
                self.assertEqual(self.given.notifications_count, 3)

            @mango.then('I see 1 unread notification')
            def then_unread_notification():
                self.assertEqual(self.given.unread_notifications_count, 1)

    @mango.given('I am logged-out user')
    def test_auth(self):
        self.given.status_code = 401

        @mango.when('I access profile by url')
        def when_access_profile():
            print('access profile')

            @mango.then('I see 401 error')
            def then_error():
                self.assertEqual(self.given.status_code, 401)

```

### Run Example
```python
python -m unittest test_example.py
```

## Contributing

### Run Test
```python
python -m unittest tests/test_mango.py
```
