from {{python_package}}.greeting import greet


def test_greet():
    assert greet("world") == "Hello, world!"
    assert greet("") == "Hello, stranger!"
