import time

from loguru import logger
import random

from help import Account, send_message, sleeping_between_wallets, intro, outro
from settings import bot_status, shuffle, bot_id, bot_token, rotes_modules, wait_zro_time
from module import Okex, LayerZero

def main():
    with open('proxies.txt', 'r') as file:  # login:password@ip:port в файл proxy.txt
        proxies = [row.strip() for row in file]
    with open('wallets.txt', 'r') as file:
        wallets = [row.strip() for row in file]
    send_list = []
    intro(wallets)
    count_wallets = len(wallets)

    if len(proxies) == 0:
        proxies = [None] * len(wallets)
    if len(proxies) != len(wallets):
        logger.error('Proxies count doesn\'t match wallets count. Add proxies or leave proxies file empty')
        return

    data = [(wallets[i], proxies[i]) for i in range(len(wallets))]

    if shuffle:
        random.shuffle(data)

    for idx, (wallet, proxy) in enumerate(data, start=1):
        if ':' in wallet:
            private_key, cex_address = wallet.split(':')[0], wallet.split(':')[1]
        else:
            private_key = wallet
            cex_address = None

        account = Account(idx, private_key, proxy, "Optimism")

        print(f'{idx}/{count_wallets} : {account.address}\n')
        send_list.append(f'{account.id}/{count_wallets} : [{account.address}]({"https://debank.com/profile/" + account.address})')
        flag_claim_in_list = False
        flag_result_claim = True
        for module in rotes_modules:
            try:
                if module[0] == 'Okex_withdrawal':
                    send_list.append(Okex(id=account.id, private_key=account.private_key, proxy=account.proxy, rpc='Arbitrum one').withdraw_from_okex())
                if module[0] == 'claim':
                    flag_claim_in_list = True
                    result = LayerZero(id=account.id, private_key=account.private_key, proxy=account.proxy, rpc='Arbitrum one').check_eligibility()
                    flag_result_claim = result[1]
                    send_list.append(result[0])
                elif module[0] == 'Cex_deposit':
                    if flag_result_claim:
                        if flag_claim_in_list:
                            logger.info(f'Жду токены {wait_zro_time} секунд...')
                            time.sleep(wait_zro_time)
                        if cex_address != None:
                            send_list.append(LayerZero(account.id, account.private_key, account.proxy, 'Arbitrum one').deposit_to_cex(cex_address))
                        else:
                            logger.info(f'Не найден адрес депозита...')
                    else:
                        logger.info(f'Перехожу к следующему акку...')

            except Exception as e:
                logger.error(f'{idx}/{count_wallets} Failed: {str(e)}')
                sleeping_between_wallets()

        if bot_status == True:
            if account.id == count_wallets:
                send_list.append(f'\nSubscribe: https://t.me/CryptoMindYep')
            send_message(bot_token, bot_id, send_list)
            send_list.clear()

        if idx != count_wallets:
            sleeping_between_wallets()
            print()

    outro()
main()