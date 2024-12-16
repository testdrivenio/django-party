# party/tests/test_party_details.py

import datetime
from urllib.parse import urlencode

import pytest
from django.urls import reverse

from party.models import Party


@pytest.mark.django_db
def test_party_detail_page_returns_whole_page_with_single_party(authenticated_client, create_user, django_user_model, create_party):
    party = create_party(organizer=create_user)

    url = reverse("page_single_party", args=[party.uuid])
    response = authenticated_client(create_user).get(url)

    assert response.status_code == 200
    assert response.context_data["party"] == party


@pytest.mark.django_db
def test_party_detail_partial_get_method_returns_a_form_prefilled_with_party_details(authenticated_client, create_user, django_user_model, create_party):
    party = create_party(organizer=create_user)

    url = reverse("partial_party_detail", args=[party.uuid])
    response = authenticated_client(create_user).get(url)

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].instance == party


@pytest.mark.django_db
def test_party_detail_partial_put_method_returns_updated_party_details(authenticated_client, create_user, create_party):
    party = create_party(organizer=create_user)

    url = reverse("partial_party_detail", args=[party.uuid])

    data = urlencode(
        {
            "party_date": "2025-06-06",
            "party_time": "18:00:00",
            "venue": "New Venue",
            "invitation": "New Bla bla",
        }
    )

    response = authenticated_client(create_user).put(url, content_type="application/json", data=data)

    assert response.status_code == 200
    assert Party.objects.get(uuid=party.uuid).party_date == datetime.date(2025, 6, 6)
    assert Party.objects.get(uuid=party.uuid).party_time == datetime.time(18, 0)
    assert Party.objects.get(uuid=party.uuid).venue == "New Venue"
    assert Party.objects.get(uuid=party.uuid).invitation == "New Bla bla"