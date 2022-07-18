import logging

from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from ..models import Assets, AssetsConfig, AssetsValues
from .values import get_history_values, get_all_companies


logger = logging.getLogger(__name__)


def assets(request):
    if request.user.is_authenticated:
        data = {
            "assets": get_assets_per_page(request),
            "history_values": get_history_values(request)
        }

        return render(request, 'assets/assets.html', data)

    return redirect('login')


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
    paginator = Paginator(assets, 12)
    page = request.GET.get("page")
    assets_per_page = paginator.get_page(page)

    return assets_per_page


def insert_assets():
    companies = get_all_companies()
    for company in companies:
        tickers = company["cd_acao"].split(",")
        for ticker in tickers:
            try:
                asset = Assets.objects.create(
                    name=company["nm_empresa"],
                    ticker=ticker.strip()
                )
                asset.save()

            except Exception:
                logger.error(
                    "Something went wrong when trying to insert a company. Maybe the company is already in database.")


def get_all_assets_config_actived():
    assets_config = AssetsConfig.objects.filter(is_active=True)

    return assets_config

