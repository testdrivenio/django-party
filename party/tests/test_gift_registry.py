# party/tests/test_gift_registry.py

from urllib.parse import urlencode

import pytest
from django.urls import reverse

from party.models import Gift


@pytest.mark.django_db
def test_gift_registry_page_lists_gifts_for_party_by_id(
    authenticated_client, create_user, create_party, create_gift
):
    party = create_party(organizer=create_user, venue="Best venue")
    gift_1 = create_gift(gift="Roses", party=party)
    gift_2 = create_gift(gift="Chocolate", party=party)

    another_party = create_party(organizer=create_user, venue="Another venue")
    create_gift(party=another_party)

    url = reverse("page_gift_registry", args=[party.uuid])
    response = authenticated_client(create_user).get(url)

    assert response.status_code == 200
    assert list(response.context_data["gifts"]) == [gift_1, gift_2]


def test_gift_detail_partial_returns_gift_detail_including_party(
    authenticated_client, create_user, django_user_model, create_party, create_gift
):
    party = create_party(organizer=create_user)
    gift = create_gift(party=party)

    url = reverse("partial_gift_detail", args=[gift.uuid])
    response = authenticated_client(create_user).get(url)

    assert response.status_code == 200
    assert response.context_data["gift"] == gift
    assert response.context_data["party"] == party


def test_partial_gift_update_returns_gift_update_form(authenticated_client, create_user, create_party, create_gift):
    party = create_party(create_user)
    gift = create_gift(party=party)

    url = reverse("partial_gift_update", args=[gift.uuid])
    response = authenticated_client(create_user).get(url)

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].instance == gift


def test_partial_gift_update_updates_gift_and_returns_its_details_including_party_id(authenticated_client, create_user, create_party, create_gift):
    party = create_party(create_user)
    gift = create_gift(party=party)

    data = urlencode(
        {
            "gift": "Updated gift",
            "price": "50",
            "link": "https://updatedtestlink.com",
        }
    )

    url = reverse("partial_gift_update", args=[gift.uuid])
    response = authenticated_client(create_user).put(url, content_type="application/json", data=data)

    assert Gift.objects.get(uuid=gift.uuid).gift == "Updated gift"
    assert Gift.objects.get(uuid=gift.uuid).price == 50.0
    assert Gift.objects.get(uuid=gift.uuid).link == "https://updatedtestlink.com"

    assert response.status_code == 200
    assert response.context["gift"].gift == "Updated gift"
    assert response.context["party"] == party


def test_partial_gift_delete_removes_gift(authenticated_client, create_user, create_party, create_gift):
    party = create_party(organizer=create_user)
    gift = create_gift(party=party)

    assert Gift.objects.count() == 1

    url = reverse("partial_gift_delete", args=[gift.uuid])

    authenticated_client(create_user).delete(url)

    assert Gift.objects.count() == 0


def test_get_partial_new_gift_returns_create_gift_form_with_party(authenticated_client, create_user, create_party):
    party = create_party(organizer=create_user)

    url = reverse("partial_new_gift", args=[party.uuid])
    response = authenticated_client(create_user).get(url)

    assert response.status_code == 200
    assert "form" in response.context
    assert not response.context["form"].is_bound
    assert response.context["party_id"] == party.uuid


def test_put_partial_new_gift_saves_gift(authenticated_client, create_user, create_party):
    party = create_party(organizer=create_user)

    data = {
        "gift": "New gift",
        "price": "50",
        "link": "https://newtestlink.com",
    }

    url = reverse("partial_new_gift", args=[party.uuid])

    response = authenticated_client(create_user).post(url, data=data)

    assert response.status_code == 200
    assert Gift.objects.count() == 1
    assert response.context["gift"].gift == "New gift"
    assert response.context["party"] == party