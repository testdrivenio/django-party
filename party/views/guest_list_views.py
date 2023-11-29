from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from party.models import Guest


class GuestListPage(LoginRequiredMixin, ListView):
    model = Guest
    template_name = "party/guest_list/page_guest_list.html"
    context_object_name = "guests"

    def get_queryset(self):
        return Guest.objects.filter(party_id=self.kwargs["party_uuid"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["party_id"] = self.kwargs["party_uuid"]
        context["attending_num"] = self.object_list.filter(attending=True).count()

        return context


@login_required
@require_http_methods(["PUT"])
def mark_attending_partial(request, party_uuid):
    mark_attending = QueryDict(request.body).getlist("guest_ids")
    Guest.objects.filter(uuid__in=mark_attending).update(attending=True)

    guests = Guest.objects.filter(party_id=party_uuid)

    return render(request, "party/guest_list/partial_guest_filter_and_list.html", {"guests": guests, "party_id": party_uuid})


@login_required
@require_http_methods(["PUT"])
def mark_not_attending_partial(request, party_uuid):
    mark_not_attending = QueryDict(request.body).getlist("guest_ids")
    Guest.objects.filter(uuid__in=mark_not_attending).update(attending=False)

    guests = Guest.objects.filter(party_id=party_uuid)

    return render(request, "party/guest_list/partial_guest_filter_and_list.html", {"guests": guests, "party_id": party_uuid})


def filter_attending(party_id, **kwargs):
    return Guest.objects.filter(party_id=party_id, attending=True)


def filter_not_attending(party_id, **kwargs):
    return Guest.objects.filter(party_id=party_id, attending=False)


def filter_attending_and_search(party_id, **kwargs):
    return Guest.objects.filter(party_id=party_id, attending=True, name__icontains=kwargs["search_text"])


def filter_not_attending_and_search(party_id, **kwargs):
    return Guest.objects.filter(party_id=party_id, attending=False, name__icontains=kwargs["search_text"])


def filter_search(party_id, **kwargs):
    return Guest.objects.filter(party_id=party_id, name__icontains=kwargs["search_text"])


def filter_default(party_id, **kwargs):
    return Guest.objects.filter(party_id=party_id)


QUERY_FILTERS= {
    ("attending", False): filter_attending,
    ("not_attending", False): filter_not_attending,
    ("attending", True): filter_attending_and_search,
    ("not_attending", True): filter_not_attending_and_search,
    ("all", True): filter_search,
}


@require_http_methods(["POST"])
def filter_guests_partial(request, party_uuid):
    attending_filter = request.POST.get("attending_filter")
    search_text = request.POST.get("guest_search")

    query_filter = QUERY_FILTERS.get((attending_filter, bool(search_text)), filter_default)

    guests = query_filter(party_id=party_uuid, search_text=search_text)

    return render(request, "party/guest_list/partial_guest_list.html", {"guests": guests})
