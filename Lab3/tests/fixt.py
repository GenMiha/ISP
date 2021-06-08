import pytest
from telebot import types

from models import *
#from .tests_constants import *


@pytest.fixture()
def data_user():
    user = User('Evgeniy', 'qwerty1234')
    database.session.add(user)
    database.session.commit()
    yield user
    database.session.delete(user)
    database.session.commit()