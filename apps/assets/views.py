from django.shortcuts import render
from .models import AssetsConfig, AssetsValues

def assets(request):
    return render(request, 'assets/assets.html')

def configuration(request):
    return render(request, 'assets/configuration.html')

def get_user_monitored_assets(request):
    monitored_assets = AssetsConfig.objects.filter(
        user_id = request.user.id,
        is_active = True
    )

    for asset in monitored_assets:
        value = AssetsValues.objects.filter(asset_id=asset.asset_id).last()
        asset.value = f"{(value.value)/100:.2f}"

    return monitored_assets