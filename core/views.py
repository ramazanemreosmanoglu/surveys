from django.shortcuts import render
from polls.models import Poll, Alert
from django.db.models import Q


def index(request):
    if not request.user.is_authenticated:
        return render(request, "welcome.html")

    query = request.GET.get("q")
    polls = Poll.objects.all()
    alerts = Alert.objects.filter(is_active=True)

    if query:
        polls = polls.filter(
            Q(title__icontains=query) |
            Q(explanation__icontains=query)
        ).distinct()

    context = {
        "polls": polls,
        "alerts": alerts,
    }

    return render(request, "index.html", context=context)
