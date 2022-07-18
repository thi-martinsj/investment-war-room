from apscheduler.schedulers.background import BackgroundScheduler

from ..views.assets import get_all_assets_config_actived
from ..views.values import check_price


scheduler = BackgroundScheduler()

def start():
    actived_configs = get_all_assets_config_actived()

    for config in actived_configs:
        create_job(config)

    scheduler.start()


def create_job(config):
    scheduler_id = f"{config.id}"
    print(f"Creating job ... ID: {scheduler_id}")
    scheduler.add_job(check_price, "interval", minutes=config.frequency, id=scheduler_id, replace_existing=True, args=[config])
    

def delete_job(scheduler_id):
    print(f"Deleting job ... ID: {scheduler_id}")
    scheduler.remove_job(scheduler_id)