import pytest


def test_equal_or_not_equal():
    assert 3 == 3
    

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student('Jhon', 'Doe', 'Computer Science', 3)


def test_person_initial(default_employee):
    assert default_employee.first_name == 'Jhon', 'first name should be Jhon'
    assert default_employee.last_name == 'Doe', 'first name should be Doe'
    assert default_employee.major == 'Computer Science'
    assert default_employee.years == 3
