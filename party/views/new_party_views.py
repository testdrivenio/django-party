from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from party.forms import PartyForm


@login_required
def page_new_party(request):
    form = PartyForm()

    if request.method == "POST":
        form = PartyForm(request.POST)
        if form.is_valid():
            party = form.save(commit=False)
            party.organizer = request.user
            party.save()
            return redirect("page_single_party", party_uuid=party.uuid)

    return render(request, "party/new_party/page_new_party.html", {"form": form})


@login_required
def partial_check_party_date(request):
    form = PartyForm(request.GET)

    return HttpResponse(as_crispy_field(form["party_date"]))


@login_required
def partial_check_invitation(request):
    form = PartyForm(request.GET)

    return HttpResponse(as_crispy_field(form["invitation"]))
