
# ===================================== options ===================================== #

#----main-options----#
shuffle = False                                                     # True / False. если нужно перемешать кошельки
decimal_places = 7                                                  # количество знаков, после запятой для генерации случайных чисел, Okex_withdrawal
delay_wallets = [5, 10]                                             # минимальная и максимальная задержка между кошельками
RETRY_COUNT = 2                                                     # кол-во попыток при возникновении ошибок
wait_zro_time = 20                                                  # сколько ждать пока придут токены, используется, если активированы 2 модуля (claim and Cex_deposit)

#------okex-options------#
auto_withdraw = False                                               # автовывод недостающей суммы ETH для доната, claim
symbolWithdraw = "ETH"                                              # символ токена, не менять, нахуя вам другой токен
amount = [0.0014, 0.00159]                                          # минимальная и максимальная сумма для вывода, Okex_withdrawal
transfer_subaccount = False                                         # перевод эфира с суббакков на мейн, Okex_withdrawal

class API:
    # okx API
    okx_apikey = ""
    okx_apisecret = ""
    okx_passphrase = ""

#------bot-options------#
bot_status = False                                                  # True / False
bot_token  = ''                                                     # telegram bot token
bot_id     = 0                                                      # telegram id

'''
Okex_withdrawal, Cex_deposit, claim
'''

rotes_modules = [
            ['claim'],
            ['Cex_deposit'],

]

# =================================== end-options =================================== #


