# party/views/party_details_views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView

from party.forms import PartyForm
from party.models import Party


class PartyDetailPage(LoginRequiredMixin, DetailView):
    model = Party
    template_name = "party/party_detail/page_party_detail.html"
    pk_url_kwarg = "party_uuid"
    context_object_name = "party"


class PartyDetailPartial(LoginRequiredMixin, View):

    def get(self, request, party_uuid, *args, **kwargs):
        party = get_object_or_404(Party, uuid=party_uuid)
        form = PartyForm(instance=party)

        return render(request, "party/party_detail/partial_party_edit_form.html", {"party": party, "form": form})

    def put(self, request, party_uuid, *args, **kwargs):
        party = get_object_or_404(Party, uuid=party_uuid)
        data = QueryDict(request.body).dict()
        form = PartyForm(data, instance=party)

        if form.is_valid():
            form.save()

        return render(request, "party/party_detail/partial_party_detail.html", {"party": party})