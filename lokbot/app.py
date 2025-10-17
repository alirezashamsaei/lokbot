import asyncio
import functools
import threading
import time

import schedule

import lokbot.util
from lokbot import project_root, logger, config
from lokbot.async_farmer import AsyncLokFarmer
from lokbot.exceptions import NoAuthException, FatalApiException
from lokbot.farmer import LokFarmer


def find_alliance(farmer: LokFarmer):
    while True:
        alliance = farmer.api.alliance_recommend().get('alliance')

        if alliance.get('numMembers') < alliance.get('maxMembers'):
            farmer.api.alliance_join(alliance.get('_id'))
            break

        time.sleep(60 * 5)


thread_map = {}


def run_threaded(name, job_func):
    if name in thread_map and thread_map[name].is_alive():
        return

    job_thread = threading.Thread(target=job_func, name=name, daemon=True)
    thread_map[name] = job_thread
    job_thread.start()


def async_main(token):
    async_farmer = AsyncLokFarmer(token)

    asyncio.run(async_farmer.parallel_buy_caravan())


def main(token=None, captcha_solver_config=None):
    # async_main(token)
    # exit()

    if captcha_solver_config is None:
        captcha_solver_config = {}
    
    # Load token from /data/token file
    if token is None:
        token_file = project_root.joinpath('data/token')
        
        if token_file.exists():
            token_from_file = token_file.read_text().strip()
            if token_from_file:
                logger.info(f'Using token from file: {token_file}')
                try:
                    farmer = LokFarmer(token_from_file, captcha_solver_config)
                except NoAuthException:
                    logger.warning('Token from file is invalid, prompting for new token')
                    token = input("Please enter x-token: ")
                    # Save the new token to /data/token
                    token_file.write_text(token)
                    farmer = LokFarmer(token, captcha_solver_config)
            else:
                # Empty token file, prompt user for token
                token = input("Please enter x-token: ")
                token_file.write_text(token)
                farmer = LokFarmer(token, captcha_solver_config)
        else:
            # No token file exists, prompt user for initial token
            token = input("Please enter x-token: ")
            token_file.write_text(token)
            farmer = LokFarmer(token, captcha_solver_config)
    else:
        # Token provided via command line, save it to /data/token
        project_root.joinpath('data/token').write_text(token)
        farmer = LokFarmer(token, captcha_solver_config)

    try:
        threading.Thread(target=farmer.sock_thread, daemon=True).start()
        threading.Thread(target=farmer.socc_thread, daemon=True).start()
    except FatalApiException as e:
        logger.error(f"Failed to start threads: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error starting threads: {e}")
        raise

    try:
        farmer.keepalive_request()
    except FatalApiException as e:
        logger.error(f"Failed to perform keepalive request: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during keepalive request: {e}")
        raise

    for job in config.get('main').get('jobs'):
        if not job.get('enabled'):
            continue

        name = job.get('name')

        schedule.every(
            job.get('interval').get('start')
        ).to(
            job.get('interval').get('end')
        ).minutes.do(run_threaded, name, functools.partial(getattr(farmer, name), **job.get('kwargs', {})))

    schedule.run_all()

    # schedule.every(15).to(20).minutes.do(farmer.keepalive_request)

    for thread in config.get('main').get('threads'):
        if not thread.get('enabled'):
            continue

        try:
            threading.Thread(target=getattr(farmer, thread.get('name')), kwargs=thread.get('kwargs'), daemon=True).start()
        except FatalApiException as e:
            logger.error(f"Failed to start thread {thread.get('name')}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error starting thread {thread.get('name')}: {e}")
            raise

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except FatalApiException as e:
            logger.error(f"Fatal error in main loop: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            raise
