from functools import wraps
import sys
import wrapt

whens = []
thens = []


class Emtpy:
    pass


def given(desc):

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        nonlocal desc
        verbose('\nGiven:', desc)
        clear(instance)

        result = wrapped(*args, **kwargs)

        for when_, desc in whens:
            with instance.subTest(when_=when_):
                call_when(instance, when_, desc)

        clear(instance)

        return result

    def clear(instance):
        instance.given = Emtpy()
        instance.when = Emtpy()
        instance.then = Emtpy()

        global whens
        whens = []

    return wrapper


def when(desc):

    def decorate(func):
        whens.append((func, desc,))
    return decorate


def then(desc):
    
    def decorate(func):
        thens.append((func, desc,))
    return decorate


def call_when(instance, func, desc):
    verbose('When:', desc)
    
    result = func()

    global thens
    for then_, desc in thens:
        with instance.subTest(then_=then_):
            verbose('Then:', desc)
            then_()

    thens = []
    verbose()

    return result

def verbose(mode='', desc=''):
    if '-v' in sys.argv or '--verbose' in sys.argv:
        print(mode, desc)