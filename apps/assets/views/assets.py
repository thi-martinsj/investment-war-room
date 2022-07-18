from django.shortcuts import render
from django.core.paginator import Paginator

from ..models import Assets, AssetsConfig, AssetsValues
from .values import get_history_values

def assets(request):
    data = {
        "assets": get_assets_per_page(request),
        "history_values": get_history_values()
    }

    return render(request, 'assets/assets.html', data)

def get_monitored_assets_from_user(request):
    monitored_assets = AssetsConfig.objects.filter(
        user_id=request.user.id,
        is_active=True
    )

    for asset in monitored_assets:
        value = AssetsValues.objects.filter(
            asset_id=asset.asset_id).order_by("created_dt").last()
        asset.value = f"{(value.value)/100:.2f}"

    return monitored_assets

def get_assets_per_page(request):
    assets = Assets.objects.all()

    for asset in assets:
        value = AssetsValues.objects.filter(
            asset_id=asset.id).order_by("created_dt").last()
        asset.value = f"{(value.value)/100:.2f}"

    paginator = Paginator(assets, 10)
    page = request.GET.get("page")
    assets_per_page = paginator.get_page(page)

    return assets_per_page

