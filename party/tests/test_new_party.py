import pytest
from django.urls import reverse

from party.models import Party


@pytest.mark.django_db
def test_create_party(authenticated_client, create_user):
    url = reverse("page_new_party")
    data = {
        "party_date": "2025-06-06",
        "party_time": "18:00:00",
        "venue": "My Venue",
        "invitation": "Come to my party!",
    }

    response = authenticated_client(create_user).post(url, data)

    assert response.status_code == 302
    assert Party.objects.count() == 1


def test_create_party_invitation_too_short_returns_error(authenticated_client, create_user):
    url = reverse("page_new_party")
    data = {
        "party_date": "2025-06-06",
        "party_time": "18:00:00",
        "venue": "My Venue",
        "invitation": "Too short",
    }

    response = authenticated_client(create_user).post(url, data)

    assert not response.context["form"].is_valid()
    assert "You really should write an invitation." in response.content.decode()
    assert Party.objects.count() == 0


def test_create_party_past_date_returns_error(authenticated_client, create_user):
    url = reverse("page_new_party")

    data = {
        "party_date": "2020-06-06",
        "party_time": "18:00:00",
        "venue": "My Venue",
        "invitation": "Come to my party!",
    }

    response = authenticated_client(create_user).post(url, data)

    assert not response.context["form"].is_valid()
    assert "You chose a date in the past." in response.content.decode()
    assert Party.objects.count() == 0


def test_partial_check_party_date(authenticated_client, create_user):
    url = reverse("partial_check_party_date")
    data = {
        "party_date": "2020-06-06",
    }

    response = authenticated_client(create_user).get(url, data)

    assert response.status_code == 200
    assert 'id="id_party_date"' in response.content.decode()
    assert "You chose a date in the past." in response.content.decode()


def test_partial_check_invitation(authenticated_client, create_user):
    url = reverse("partial_check_invitation")
    data = {
        "invitation": "Too short",
    }

    response = authenticated_client(create_user).get(url, data)

    assert response.status_code == 200
    assert 'id="id_invitation"' in response.content.decode()
    assert "You really should write an invitation." in response.content.decode()
