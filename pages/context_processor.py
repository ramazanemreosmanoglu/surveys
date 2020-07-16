from .models import Page

def func(request):
    datas = Page.objects.filter(is_it_in_navbar=True)
    context = dict(
        NAV_PAGES=datas,
    )

    return context
