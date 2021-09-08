from django.test import TestCase
import pytest
# Create your tests here.
from django.urls import reverse, resolve
from django.test import RequestFactory
from bot.models import User, Item, UserRating, CreditCard, Order
from bot.views import ItemView


@pytest.mark.parametrize('url_name', [('home'), ('create_card'), ('order_history'),])
def test_post_content_url(url_name):
        path = reverse(url_name)
        assert resolve(path).view_name == url_name


@pytest.mark.parametrize('url_name', [('buy_item'), ('item_rating')])
def test_post_content_url_with_kwargs(url_name):
        path = reverse(url_name, kwargs={'pk':1})
        assert resolve(path).view_name == url_name


@pytest.fixture
def user(db):
    return User.objects.create_user("A")


@pytest.fixture
def item(db, user):
    item = Item.objects.create(
        name='test_item',
        price=100,
        description='test description',
        amount=10,
        user=user
    )
    user.items.add(item)
    return item


@pytest.fixture
def user_rating(db, user, item):
    return UserRating.objects.create(
        item=item,
        user=user,
        value=3
    )


@pytest.fixture
def credit_card(db, user):
    return CreditCard.objects.create(
        user=user,
        card_number='1234567890123456',
        card_holder_name='test name',
        expiration_month='12',
        expiration_year='30',
        cvv_number='555'
    )


@pytest.fixture
def order(db, credit_card, item):
    return Order.objects.create(
        credit_card=credit_card,
        item=item,
        item_amount=2,
        total_price=200
    )


@pytest.fixture
def self_request(db, user, mocker):
    self = mocker.MagicMock()
    self.request.user = user
    return self


def test_context(db, user, item):
    factory = RequestFactory()
    request = factory.get('/item-table')
    request.user = user
    response = ItemView.as_view()(request)
    print(response)
    assert response
    assert response.context_data.get("items")


def test_should_check_password(db, user: User) -> None:
    user.set_password("secret")
    assert user.check_password("secret") is True


def test_should_not_check_unusable_password(db, user: User) -> None:
    user.set_password("secret")
    user.set_unusable_password()
    assert user.check_password("secret") is False


