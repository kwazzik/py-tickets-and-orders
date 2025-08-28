from django.db import transaction
from django.db.models import QuerySet
import datetime
from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list[dict], username: str, date: str = None):
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order(user=user)
        if date:
            order.created_at = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(id=ticket['movie_session'])
            ticket_obj = Ticket(
                movie_session=movie_session,
                order=order,
                row=ticket['row'],
                seat=ticket['seat'],
            )
            ticket_obj.full_clean()
            ticket_obj.save()

    return order

def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()