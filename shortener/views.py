from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import URL
from .forms import URLForm


def home(request):
    form = URLForm(request.POST or None)
    short_url = None

    if form.is_valid():
        original_url = form.cleaned_data["original_url"]
        custom_code = form.cleaned_data.get("custom_code")

        if custom_code and URL.objects.filter(custom_code=custom_code).exists():
            return HttpResponse("Custom code already token. TRY another one.")

        url_obj = form.save(commit=False)
        url_obj.custom_code = custom_code
        url_obj.save()
        short_url = request.build_absolute_uri("/") + url_obj.final_code
    urls = URL.objects.all().order_by("-created_at")
    return render(request, "shortener/home.html", {"form": form, "short_url": short_url, "urls": urls})


def redirect_url(request, code):
    url_obj = get_object_or_404(URL, custom_code=code) if URL.objects.filter(custom_code=code).exists() else get_object_or_404(URL, short_code=code)
    url_obj.clicks += 1
    url_obj.save()
    return redirect(url_obj.original_url)
