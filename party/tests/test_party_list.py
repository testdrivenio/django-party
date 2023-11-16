import datetime

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_party_list_page_returns_list_of_users_future_parties(authenticated_client, create_user, create_party, django_user_model):
    today = datetime.date.today()
    user = create_user
    other_user = django_user_model.objects.create_user(username="some_other_user", password="whatever")

    valid_party_1 = create_party(
        organizer=user, party_date=today, venue="Venue 1"
    )
    valid_party_2 = create_party(
        organizer=user,
        party_date=today + datetime.timedelta(days=30),
        venue="Venue 2",
    )
    create_party(
        organizer=other_user,
        venue="Venue 3"
    )
    create_party(
        organizer=user,
        party_date=today - datetime.timedelta(days=10),
        venue="Venue 4",
    )

    url = reverse("page_party_list")
    response = authenticated_client(user).get(url)

    parties_list = list(response.context_data["parties"])

    assert response.status_code == 200
    assert len(parties_list) == 2
    assert parties_list == [valid_party_1, valid_party_2]
