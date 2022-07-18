from django.shortcuts import redirect, render
from django.contrib import messages

from ..models import Assets, AssetsConfig
from .assets import get_assets_per_page
from .values import insert_history_value
from .. import scheduler

def configuration(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST["id"]:
                update_config(request)
            else:
                insert_config(request)

        data = {
            "assets": get_assets_configuration_per_page(request)
        }

        return render(request, 'assets/configuration.html', data)

    return redirect('login')


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
    params = get_config_params(request)

    asset_config.min_value = params["min_value"]
    asset_config.max_value = params["max_value"]
    asset_config.frequency = params["frequency"]
    asset_config.is_active = params["is_active"]
    asset_config.save()
    
    if params["is_active"]:
        asset = Assets.objects.get(pk=params["asset_id"])
        insert_history_value(asset, request.user)
        scheduler.create_job(asset_config)
    else:
        scheduler.delete_job(f"{asset_config.id}")

    messages.success(
        request, f"Asset {asset_config.asset_id} Configuration Updated Successfully")


def insert_config(request):
    params = get_config_params(request)

    asset = Assets.objects.get(pk=params["asset_id"])

    asset_config = AssetsConfig.objects.create(
        asset_id=asset,
        user_id=request.user,
        min_value=params["min_value"],
        max_value=params["max_value"],
        frequency=params["frequency"],
        is_active=params["is_active"]
    )

    asset_config.save()

    if params["is_active"]:
        asset = Assets.objects.get(pk=params["asset_id"])
        insert_history_value(asset, request.user)
        scheduler.create_job(asset_config)

    messages.success(
        request, f"Asset {asset} Configuration Added Successfully")


def get_config_params(request):
    asset_id = request.POST["asset_id"]
    min_value = int(request.POST["min_value"].replace(
        ",", "").replace(".", ""))
    max_value = int(request.POST["max_value"].replace(
        ",", "").replace(".", ""))
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