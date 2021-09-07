import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, UpdateView, DeleteView, DetailView, ListView

from bot.forms import CreditCardForm, SignUpForm
from bot.models import Item, User, UserRating, CreditCard, Order

logger = logging.getLogger(__name__)


class TestView(LoginRequiredMixin, TemplateView):
    template_name = 'Test.html'

    def get_context_data(self, **kwargs):
        logger.debug('[+] Home page context is rendering...')

        items = Item.objects.all()
        ratings = UserRating.objects.prefetch_related('item')

        items_list = []

        for item in items:
            items_list.append(
                {
                    'name': item.name,
                    'description': item.description,
                    'id': item.id,
                    'rating': ratings.filter(item=item).aggregate(Avg('value'))['value__avg']
                }
            )

        context = {'items': items_list}

        logger.info('[+] Home page context rendered successfully.')
        return context


class CustomerView(LoginRequiredMixin, TemplateView):
    template_name = 'customersTable.html'

    def get_context_data(self, **kwargs):
        logger.debug("[+] Customer View's context is rendering...")
        items = User.items.through.objects.all()

        context = {'items': items}

        logger.info("[+] Customer View context rendered successfully")
        return context


class ItemView(LoginRequiredMixin, TemplateView):
    template_name = 'itemsTable.html'

    def get_context_data(self, **kwargs):
        logger.debug('[+] Item view context is rendering...')
        items = Item.objects.filter(user=self.request.user)
        print(items)

        context = {'items': items}

        logger.info('[+] Item view context rendered successfully')
        return context


class CreditCardCreateView(LoginRequiredMixin, FormView):
    template_name = 'creditCard.html'
    form_class = CreditCardForm
    success_url = reverse_lazy('card_info')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.request.user.creditcard
            logger.error('[+] User attempted to create extra card, redirecting...')
            return redirect(reverse_lazy('card_info'))
        except ObjectDoesNotExist:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        CreditCard.objects.create(user=self.request.user, **data)
        logger.info('[+] Card created successfully...')
        return redirect(self.success_url)


class CreditCardReadView(LoginRequiredMixin, TemplateView):
    template_name = 'creditcardinfo.html'


class CreditCardUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'creditCardUpdate.html'
    model = CreditCard
    fields = ('card_number', 'card_holder_name', 'expiration_month', 'expiration_year', 'cvv_number')
    success_url = reverse_lazy('card_info')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.request.user.creditcard
        except ObjectDoesNotExist:
            logger.error('[+] User attempted to update non-existent card, redirecting him to card info page...')
            return redirect(reverse_lazy('card_info'))

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, **kwargs):
        return self.request.user.creditcard


class CreditCardDeleteView(LoginRequiredMixin, DeleteView):
    model = CreditCard
    success_url = reverse_lazy('home')
    template_name = 'creditCardDelete.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.request.user.creditcard
        except ObjectDoesNotExist:
            logger.error('[+] User attempted to delete non-existent card, redirecting him to card info page...')
            return redirect(reverse_lazy('card_info'))

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, **kwargs):
        return self.request.user.creditcard


class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        logger.info('[+] New user created successfully.')
        return redirect(self.success_url)


class UserLoginView(LoginView):
    template_name = 'login.html'


class UserLogoutView(LogoutView):
    pass


class BuyItemView(LoginRequiredMixin, DetailView):
    template_name = 'buyItem.html'
    model = Item

    def post(self, request, *args, **kwargs):
        item = self.get_object()
        amount = int(request.POST['item-amount'])

        Order.objects.create(
            credit_card=request.user.creditcard,
            item=item,
            item_amount=amount,
            total_price=item.price*amount
        )

        item.amount = item.amount - amount
        item.save()

        return redirect(reverse_lazy('home'))


class OrderHistoryView(LoginRequiredMixin, ListView):
    template_name = 'orderHistory.html'

    def get_queryset(self):
        return Order.objects.filter(credit_card=self.request.user.creditcard)


class ItemRatingView(LoginRequiredMixin, DetailView):
    template_name = 'rating.html'
    model = Item

    def post(self, request, *args, **kwargs):
        item = self.get_object()
        rating_value = float(request.POST['item-rating'])
        rating = None

        try:
            rating = UserRating.objects.get(item=item, user=request.user)
        except ObjectDoesNotExist:
            UserRating.objects.create(
                item=item,
                value=rating,
                user=request.user
            )

            return redirect(reverse_lazy('home'))

        rating.value = rating_value
        rating.save()

        return redirect(reverse_lazy('home'))