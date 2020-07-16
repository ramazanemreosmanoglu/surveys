from .models import Page
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def view_page(request, url):
    page = get_object_or_404(Page, url=url)
    context = dict(
        page=page,
        navbar_links=Page.objects.filter(is_it_in_navbar=True)
    )

    return render(request, "page_view.html", context)
