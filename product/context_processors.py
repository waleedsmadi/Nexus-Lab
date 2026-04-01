from .models import Category


def categories(request):
    return {"categories": Category.choices}