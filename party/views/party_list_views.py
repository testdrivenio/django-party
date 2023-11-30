import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from party.models import Party


class PartyListPage(LoginRequiredMixin, ListView):
    model = Party
    context_object_name = "parties"
    paginate_by = 6

    def get_queryset(self):
        return Party.objects.filter(
            organizer=self.request.user, party_date__gte=datetime.date.today()
        ).order_by("party_date")

    def get_template_names(self):
        if "HTTP_HX_REQUEST" in self.request.META:
            return ["party/party_list/partial_parties_list.html"]
        else:
            return ["party/party_list/page_parties_list.html"]
