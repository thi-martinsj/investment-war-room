from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Assets, AssetsConfig, AssetsValues

def assets(request):
    data = {
        "assets": get_assets_per_page(request),
        "history_values": get_history_values()
    }

    return render(request, 'assets/assets.html', data)

def configuration(request):
    return render(request, 'assets/configuration.html')

def get_user_monitored_assets(request):
    monitored_assets = AssetsConfig.objects.filter(
        user_id = request.user.id,
        is_active = True
    )

    for asset in monitored_assets:
        value = AssetsValues.objects.filter(asset_id=asset.asset_id).order_by("created_dt").last()
        asset.value = f"{(value.value)/100:.2f}"

    return monitored_assets

def get_assets_per_page(request):
    assets = Assets.objects.all()

    for asset in assets:
        value = AssetsValues.objects.filter(asset_id=asset.id).order_by("created_dt").last()
        asset.value = f"{(value.value)/100:.2f}"

    paginator = Paginator(assets, 10)
    page = request.GET.get("page")
    assets_per_page = paginator.get_page(page)

    return assets_per_page

def get_history_values():
    values = AssetsValues.objects.all().order_by("-created_dt")

    for value in values:
        value.value = f"{(value.value)/100:.2f}"

    return values
