# party/tests/test_guest_list.py

import pytest
from django.urls import reverse

from party.models import Guest


@pytest.mark.django_db
def test_page_guest_list_lists_guests_for_certain_party(authenticated_client, create_user, create_party, create_guest):
    party = create_party(organizer=create_user, venue="Main venue")
    guest_1 = create_guest(party=party, name="Anna Brown")
    guest_2 = create_guest(party=party, name="Lia Keyes")

    another_party = create_party(organizer=create_user, venue="Another venue")
    create_guest(party=another_party, name="Guest from another party")

    url = reverse("page_guest_list", args=[party.uuid])

    response = authenticated_client(create_user).get(url)
    response_guests_list = list(response.context["guests"])

    assert response.status_code == 200
    assert response.context["party_id"] == party.uuid
    assert response_guests_list == [guest_1, guest_2]
    assert len(response_guests_list) == 2


@pytest.mark.django_db
def test_mark_guest_attending(authenticated_client, create_user, create_party, create_guest):
    party = create_party(organizer=create_user)
    guest_1 = create_guest(party=party, attending=False)
    guest_2 = create_guest(party=party, attending=False)

    url = reverse("partial_mark_attending", args=[party.uuid])

    data = f"guest_ids={guest_1.uuid}"
    response = authenticated_client(create_user).put(url, data=data, content_type="application/x-www-form-urlencoded")

    assert Guest.objects.get(uuid=guest_1.uuid).attending is True
    assert Guest.objects.get(uuid=guest_2.uuid).attending is False

    assert response.status_code == 200
    assert len(list(response.context["guests"])) == 2
    assert response.context["party_id"] == party.uuid


@pytest.mark.django_db
@pytest.mark.parametrize(
    "guest_attending_status,  search_text, attending_filter, expected_number_of_filtered_guests",
    [
        (True, "an", "all", 1),
        (True, "be", "all", 0),
        (True, "be", "attending", 0),
        (True, "be", "not_attending", 0),
        (True, "an", "attending", 1),
        (True, "an", "not_attending", 0),
        (True, "", "attending", 1),
        (True, "", "not_attending", 0),
        (False, "an", "all", 1),
        (False, "be", "all", 0),
        (False, "be", "attending", 0),
        (False, "be", "not_attending", 0),
        (False, "an", "attending", 0),
        (False, "an", "not_attending", 1),
        (False, "", "attending", 0),
        (False, "", "not_attending", 1),
    ],
)
def test_filter_guest_by_status_and_search(
        guest_attending_status,
        search_text,
        attending_filter,
        expected_number_of_filtered_guests,
        authenticated_client,
        create_user,
        create_party,
        create_guest,
):
    party = create_party(organizer=create_user)
    create_guest(party=party, name="Anna", attending=guest_attending_status)

    url = reverse("partial_filter_guests", args=[party.uuid])

    data = {"attending_filter": attending_filter, "guest_search": search_text}

    response = authenticated_client(create_user).post(url, data)

    assert len(response.context["guests"]) == expected_number_of_filtered_guests


@pytest.mark.django_db
def test_mark_guest_not_attending(authenticated_client, create_user, create_party, create_guest):
    party = create_party(organizer=create_user)
    guest_1 = create_guest(party=party, attending=True)
    guest_2 = create_guest(party=party, attending=True)

    url = reverse("partial_mark_not_attending", args=[party.uuid])

    data = f"guest_ids={guest_1.uuid}"
    response = authenticated_client(create_user).put(url, data=data, content_type="application/x-www-form-urlencoded")

    assert Guest.objects.get(uuid=guest_1.uuid).attending is False
    assert Guest.objects.get(uuid=guest_2.uuid).attending is True

    assert response.status_code == 200
    assert len(list(response.context["guests"])) == 2
    assert response.context["party_id"] == party.uuid
