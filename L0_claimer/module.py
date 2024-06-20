from sys import stderr
import time
import json
from pyuseragents import random as random_ua
from requests import Session
import random
import ccxt
from loguru import logger
from hexbytes import HexBytes

from settings import amount, symbolWithdraw, decimal_places, transfer_subaccount, API, auto_withdraw
from help import Account, retry, sign_and_send_transaction, sleeping_between_transactions, SUCCESS, FAILED, get_tx_data_withABI, get_tx_data, get_min_to_amount, get_token_price


send_list = ''

thruster_router_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH9","type":"address"},{"internalType":"address","name":"_manager","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"ClaimGas","type":"event"},{"inputs":[],"name":"BLAST","outputs":[{"internalType":"contract IBlast","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WETH9","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_recipient","type":"address"},{"internalType":"uint256","name":"_minClaimRateBips","type":"uint256"}],"name":"claimGas","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"}],"internalType":"struct ISwapRouter.ExactInputParams","name":"params","type":"tuple"}],"name":"exactInput","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct ISwapRouter.ExactInputSingleParams","name":"params","type":"tuple"}],"name":"exactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"}],"internalType":"struct ISwapRouter.ExactOutputParams","name":"params","type":"tuple"}],"name":"exactOutput","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct ISwapRouter.ExactOutputSingleParams","name":"params","type":"tuple"}],"name":"exactOutputSingle","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"manager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"refundETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowed","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowedIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_manager","type":"address"}],"name":"setManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"sweepToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"sweepTokenWithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"int256","name":"amount0Delta","type":"int256"},{"internalType":"int256","name":"amount1Delta","type":"int256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"uniswapV3SwapCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"unwrapWETH9","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"unwrapWETH9WithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_admin","type":"address"}],"name":"updatePointsAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]')
liquidity_router_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH9","type":"address"},{"internalType":"address","name":"_tokenDescriptor_","type":"address"},{"internalType":"address","name":"_manager","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"ClaimGas","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":false,"internalType":"int24","name":"tickLower","type":"int24"},{"indexed":false,"internalType":"int24","name":"tickUpper","type":"int24"},{"indexed":false,"internalType":"address","name":"pool","type":"address"}],"name":"Collect","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"uint128","name":"liquidity","type":"uint128"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":false,"internalType":"int24","name":"tickLower","type":"int24"},{"indexed":false,"internalType":"int24","name":"tickUpper","type":"int24"},{"indexed":false,"internalType":"address","name":"pool","type":"address"}],"name":"DecreaseLiquidity","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"uint128","name":"liquidity","type":"uint128"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":false,"internalType":"int24","name":"tickLower","type":"int24"},{"indexed":false,"internalType":"int24","name":"tickUpper","type":"int24"},{"indexed":false,"internalType":"address","name":"pool","type":"address"}],"name":"IncreaseLiquidity","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"BLAST","outputs":[{"internalType":"contract IBlast","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WETH9","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_recipient","type":"address"},{"internalType":"uint256","name":"_minClaimRateBips","type":"uint256"}],"name":"claimGas","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint128","name":"amount0Max","type":"uint128"},{"internalType":"uint128","name":"amount1Max","type":"uint128"}],"internalType":"struct INonfungiblePositionManager.CollectParams","name":"params","type":"tuple"}],"name":"collect","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"}],"name":"createAndInitializePoolIfNecessary","outputs":[{"internalType":"address","name":"pool","type":"address"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256","name":"amount1Min","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"internalType":"struct INonfungiblePositionManager.DecreaseLiquidityParams","name":"params","type":"tuple"}],"name":"decreaseLiquidity","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"amount0Desired","type":"uint256"},{"internalType":"uint256","name":"amount1Desired","type":"uint256"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256","name":"amount1Min","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"internalType":"struct INonfungiblePositionManager.IncreaseLiquidityParams","name":"params","type":"tuple"}],"name":"increaseLiquidity","outputs":[{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"manager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"uint256","name":"amount0Desired","type":"uint256"},{"internalType":"uint256","name":"amount1Desired","type":"uint256"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256","name":"amount1Min","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"internalType":"struct INonfungiblePositionManager.MintParams","name":"params","type":"tuple"}],"name":"mint","outputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"positions","outputs":[{"internalType":"uint96","name":"nonce","type":"uint96"},{"internalType":"address","name":"operator","type":"address"},{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256","name":"feeGrowthInside0LastX128","type":"uint256"},{"internalType":"uint256","name":"feeGrowthInside1LastX128","type":"uint256"},{"internalType":"uint128","name":"tokensOwed0","type":"uint128"},{"internalType":"uint128","name":"tokensOwed1","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"refundETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowed","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowedIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_manager","type":"address"}],"name":"setManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"sweepToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount0Owed","type":"uint256"},{"internalType":"uint256","name":"amount1Owed","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"uniswapV3MintCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"unwrapWETH9","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_admin","type":"address"}],"name":"updatePointsAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]')

switch_cex = "okx"
proxy_server = ""
proxies = {
  "http": proxy_server,
  "https": proxy_server,
}


class LayerZero(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.rpc = rpc
        self.session = Session()
        self.session.headers['user-agent'] = random_ua()
        self.proxy = proxy
        if self.proxy != None:
            self.session.proxies.update({'http': "http://" + self.proxy, 'https': "http://" + self.proxy})

    @retry
    def check_eligibility(self):
        global send_list
        send_list = ''
        self.session.headers.update({
            'authority': 'www.layerzero.foundation',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'cookie': '_ga=GA1.1.191457852.1718897787; _ga_W6E6GKBERD=GS1.1.1718897787.1.0.1718897787.0.0.0; _clck=1tkuza6%7C2%7Cfms%7C0%7C1632; _clsk=138ndj9%7C1718897787679%7C1%7C1%7Ca.clarity.ms%2Fcollect',
            'referer': 'https://www.layerzero.foundation/claim',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        })


        response = self.session.get(f'https://www.layerzero.foundation/api/allocation/{self.address}', headers=self.session.headers)

        # print(response)
        response = response.json()
        if response['isEligible']:
            amount_zro_wei = int(response['zroAllocation']['asBigInt'])
            amount_zro = float(response["zroAllocation"]["asString"])
            logger.info(f'Поздравляю! Доступно для клейма - {amount_zro} ZRO')

            json_data = [
                {
                    'method': 'eth_call',
                    'params': [
                        {
                            'to': '0xd6b6a6701303b5ea36fa0edf7389b562d8f894db',
                            'data': f'0xd6d754db{hex(amount_zro_wei)[2:].lower().zfill(64)}',
                        },
                        'latest',
                    ],
                    'id': 44,
                    'jsonrpc': '2.0',
                },
            ]

            response = self.session.post('https://arb1.arbitrum.io/rpc', json=json_data).json()
            amount_eth_hex = response[0]['result'][-64:]
            amount_eth_wei = int(amount_eth_hex, 16)
            amount_eth = amount_eth_wei / 10 ** 18

            response = self.session.get(f'https://www.layerzero.foundation/api/proof/{self.address}', headers=self.session.headers).json()

            data = (f'0xac6ae3ee'
                    f'0000000000000000000000000000000000000000000000000000000000000002'
                    f'{hex(amount_eth_wei)[2:].lower().zfill(64)}'
                    f'{hex(amount_zro_wei)[2:].lower().zfill(64)}'
                    f'00000000000000000000000000000000000000000000000000000000000000c0'
                    f'{self.address[2:].lower().zfill(64)}'
                    f'0000000000000000000000000000000000000000000000000000000000000380'
                    f'0000000000000000000000000000000000000000000000000000000000000015')

            list_data = response['proof'].split('|')
            for i in list_data:
                data += i[2:]
            data += '0000000000000000000000000000000000000000000000000000000000000000'

            balance = self.get_balance()

            if amount_eth_wei > balance['balance_wei']:
                logger.info(f'Не хватает эфира на донат... Перехожу к следующему аккаунту {amount_eth}|{balance["balance"]}')
                send_list +=  (f'\n{FAILED}Airdrop: Claim {amount_zro_wei} ZRO - failed (Не хватает эфира на донат)')
                if auto_withdraw:
                    logger.info(f'Пробую вывести с окекса {amount_eth} ETH')
                    Okex(id=self.id, private_key=self.private_key, proxy=self.proxy, rpc='Arbitrum one').withdraw_from_okex(amount_eth)
                else:
                    return send_list, False


            transaction = get_tx_data(self, self.w3.to_checksum_address('0xb09f16f625b363875e39ada56c03682088471523'), value=amount_eth_wei, data=data)

            logger.info(f'Airdrop: Claim {amount_zro} ZRO...')
            txstatus, tx_hash = sign_and_send_transaction(self, transaction)

            if txstatus == 1:
                logger.success(f'Airdrop: Claim {amount_zro} ZRO : {self.scan + tx_hash}')
                send_list +=  (f'\n{SUCCESS}Airdrop: Claim {amount_zro} ZRO - [tx hash]({self.scan + tx_hash})')
                return send_list, True

            else:
                logger.error(f'Airdrop: Claim {amount_zro} ZRO : {self.scan + tx_hash}')
                send_list +=  (f'\n{FAILED}Airdrop: Claim {amount_zro} ZRO - failed')
                return send_list, False

        elif response['isEligible'] == False:
            logger.info(f'Не повезло')
            send_list += (f'\n{FAILED}Airdrop: Claim - failed (нот эллигбл)')
            return send_list, False
        else:
            logger.info(f'Ошибка')
            return send_list, False

    @retry
    def deposit_to_cex(self, addresscex):
        global send_list
        send_list = ''
        balance = self.get_balance(contract_address='0x6985884c4392d348587b19cb9eaaf157f13271cd')
        amount_zro_wei = balance['balance_wei']
        amount_zro = balance['balance']
        if amount_zro < 0:
            logger.info(f'Airdrop: количество токенов 0')
            send_list += (f'\n{FAILED}Airdrop: количество токенов 0')
            return send_list

        data = (f'0xa9059cbb'
                f'{addresscex[2:].lower().zfill(64)}'
                f'{hex(amount_zro_wei)[2:].lower().zfill(64)}')

        transaction = get_tx_data(self, self.w3.to_checksum_address('0x6985884c4392d348587b19cb9eaaf157f13271cd'), data=data)

        logger.info(f'Airdrop: Send {amount_zro} ZRO to cex...')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)

        if txstatus == 1:
            logger.success(f'Airdrop: Send {amount_zro} ZRO to cex : {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}Airdrop: Send {amount_zro} ZRO to cex - [tx hash]({self.scan + tx_hash})')
            return send_list

        else:
            logger.error(f'Airdrop: Send {amount_zro} ZRO to cex : {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}Airdrop: Send {amount_zro} ZRO to cex - failed')
            return send_list

stay_eth = [0.0013, 0.0015]
class Okex(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.rpc = rpc

    @retry
    def deposit_to_okex(self, addressokx):
        stay_eth_in_network = round(random.uniform(stay_eth[0], stay_eth[1]), decimal_places)
        value_in_eth = self.get_balance()["balance"] - stay_eth_in_network
        value_in_wei = int(self.w3.to_wei(value_in_eth, "ether"))

        transaction = get_tx_data(self, self.w3.to_checksum_address(addressokx), value=value_in_wei)

        logger.info(f'OKx: Deposit {"{:0.9f}".format(value_in_eth)} ETH from {self.rpc}...')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)

        if txstatus == 1:
            logger.success(f'OKx: Deposit {"{:0.9f}".format(value_in_eth)} ETH from {self.rpc} : {self.scan + tx_hash}')
            return (
                f'\n{SUCCESS}OKx: Deposit {"{:0.4f}".format(value_in_eth)} ETH from {self.rpc} - [tx hash]({self.scan + tx_hash})')
        else:
            logger.error(f'OKx: Deposit {"{:0.9f}".format(value_in_eth)} ETH from {self.rpc} : {self.scan + tx_hash}')
            return (f'\n{FAILED}OKx: Deposit {"{:0.4f}".format(value_in_eth)} ETH from {self.rpc} - failed')

    def withdraw_from_okex(self, amount_eth=None):
        if amount_eth != None:
            amount_to_withdrawal = amount_eth

        if transfer_subaccount:
            Okex.transfer_from_subaccount(self)
            print()
        delay = [3, 5]
        amount_to_withdrawal = round(random.uniform(amount[0], amount[1]), decimal_places)
        Okex.choose_cex(self.address, amount_to_withdrawal, 1)
        time.sleep(random.randint(delay[0], delay[1]))
        self.wait_balance(int(self.w3.to_wei(amount_to_withdrawal, 'ether') * 0.8), rpc=self.rpc)
        sleeping_between_transactions()
        return (f'\n{SUCCESS}OKx: Withdraw {"{:0.4f}".format(amount_to_withdrawal)} ETH')

    def transfer_from_subaccount(self):
        exchange = ccxt.okx({
            'apiKey': API.okx_apikey,
            'secret': API.okx_apisecret,
            'password': API.okx_passphrase,
            'enableRateLimit': True,
            'proxies': proxies,
        })

        list_sub = exchange.private_get_users_subaccount_list()
        for sub_data in list_sub['data']:
            name_sub = sub_data['subAcct']
            balance = exchange.private_get_asset_subaccount_balances({'subAcct': name_sub, 'ccy': symbolWithdraw})
            sub_balance = balance['data'][0]['bal']
            logger.info(f'OKx: {name_sub} balance : {sub_balance} {symbolWithdraw}')
            if float(sub_balance) > 0:
                transfer = exchange.private_post_asset_transfer(
                    {"ccy": symbolWithdraw, "amt": str(sub_balance), "from": '6', "to": '6', "type": "2",
                     "subAcct": name_sub})
                logger.success(f'OKx: transfer to main {sub_balance} {symbolWithdraw}')
            else:
                continue
        time.sleep(15)
        return True

    def okx_withdraw(self, address, amount_to_withdrawal, wallet_number):
        exchange = ccxt.okx({
            'apiKey': API.okx_apikey,
            'secret': API.okx_apisecret,
            'password': API.okx_passphrase,
            'enableRateLimit': True,
            'proxies': proxies,
        })

        try:
            chainName = symbolWithdraw + "-" + self.rpc
            fee = Okex.get_withdrawal_fee(symbolWithdraw, chainName)
            exchange.withdraw(symbolWithdraw, amount_to_withdrawal, address,
                              params={
                                  "toAddress": address,
                                  "chainName": chainName,
                                  "dest": 4,
                                  "fee": fee,
                                  "pwd": '-',
                                  "amt": amount_to_withdrawal,
                                  "network": self.rpc
                              }
                              )
            logger.success(f'OKx: Вывел {amount_to_withdrawal} {symbolWithdraw}')
            return amount_to_withdrawal
        except Exception as error:
            logger.error(f'OKx: Не удалось вывести {amount_to_withdrawal} {symbolWithdraw}: {error}')

    def choose_cex(address, amount_to_withdrawal, wallet_number):
        if switch_cex == "okx":
            Okex.okx_withdraw(address, amount_to_withdrawal, wallet_number)

    def get_withdrawal_fee(symbolWithdraw, chainName):
        exchange = ccxt.okx({
            'apiKey': API.okx_apikey,
            'secret': API.okx_apisecret,
            'password': API.okx_passphrase,
            'enableRateLimit': True,
            'proxies': proxies,
        })
        currencies = exchange.fetch_currencies()
        for currency in currencies:
            if currency == symbolWithdraw:
                currency_info = currencies[currency]
                network_info = currency_info.get('networks', None)
                if network_info:
                    for network in network_info:
                        network_data = network_info[network]
                        network_id = network_data['id']
                        if network_id == chainName:
                            withdrawal_fee = currency_info['networks'][network]['fee']
                            if withdrawal_fee == 0:
                                return 0
                            else:
                                return withdrawal_fee
        raise ValueError(f"не могу получить сумму комиссии, проверьте значения symbolWithdraw и network")



