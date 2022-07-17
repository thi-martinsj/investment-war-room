from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Assets, AssetsConfig, AssetsValues


def assets(request):
    data = {
        "assets": get_assets_per_page(request),
        "history_values": get_history_values()
    }

    return render(request, 'assets/assets.html', data)


def configuration(request):
    if request.method == "POST":
        if request.POST["id"]:
            update_config(request)
        else:
            insert_config(request)

    data = {
        "assets": get_assets_configuration_per_page(request)
    }

    return render(request, 'assets/configuration.html', data)


def get_user_monitored_assets(request):
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


def get_history_values():
    values = AssetsValues.objects.all().order_by("-created_dt")

    for value in values:
        value.value = f"{(value.value)/100:.2f}"

    return values


def get_assets_configuration_per_page(request):
    assets_per_age = get_assets_per_page(request)

    for asset in assets_per_age:
        asset_config = AssetsConfig.objects.filter(
            asset_id=asset.id, user_id=request.user.id).last()
        if asset_config is not None:
            asset.config_id = asset_config.id
            asset.min_value = f"{(asset_config.min_value)/100:.2f}"
            asset.max_value = f"{(asset_config.max_value)/100:.2f}"
            asset.frequency = asset_config.frequency
            asset.is_active = asset_config.is_active

    return assets_per_age


def update_config(request):
    id = request.POST["id"]
    asset_config = AssetsConfig.objects.get(pk=id)
    params = _get_config_params(request)

    asset_config.min_value = params["min_value"]
    asset_config.max_value = params["max_value"]
    asset_config.frequency = params["frequency"]
    asset_config.is_active = params["is_active"]
    asset_config.save()

    messages.success(request, f"Asset {asset_config.asset_id} Configuration Updated Successfully")

def insert_config(request):
    params = _get_config_params(request)

    asset = Assets.objects.get(pk=params["asset_id"])

    asset_config = AssetsConfig.objects.create(
        asset_id = asset,
        user_id = request.user,
        min_value = params["min_value"],
        max_value = params["max_value"],
        frequency = params["frequency"],
        is_active = params["is_active"]
    )

    asset_config.save()

    messages.success(request, f"Asset {asset} Configuration Added Successfully")

def _get_config_params(request):
    asset_id = request.POST["asset_id"]
    min_value = int(request.POST["min_value"].replace(",", "").replace(".",""))
    max_value = int(request.POST["max_value"].replace(",", "").replace(".",""))
    frequency = int(request.POST["frequency"])
    is_active = False

    if "is_active" in request.POST:
        is_active = True

    return {
        "asset_id": asset_id,
        "min_value": min_value,
        "max_value": max_value,
        "frequency": frequency,
        "is_active": is_active
    }
