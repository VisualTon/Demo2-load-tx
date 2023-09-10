import time
import json
import requests
import asyncio
from datetime import datetime

my_list = []

async def get_tx_info(txid: str):
    # get transaction info
    url = f"https://tonapi.io/v2/blockchain/transactions/{txid}"
    response = await get_request(url)
    # time.sleep(5)
    data = response.json()
    in_msgs = data.get("in_msg", [])
    if in_msgs:
        trans_id = data['hash']
        sender_address = data["account"]["address"]
        receiver_address = data["in_msg"]["destination"]["address"]
        amount = int(data["in_msg"]["value"]) // 10**9
        asset = "TON"
        confirm_time = data["utime"]

        if amount > 0 and sender_address != receiver_address:
            in_msg_data = {
                "Transaction_id": trans_id,
                "Sender_address": sender_address,
                "Receiver_address": receiver_address,
                "Amount": amount,
                "Confirm_time": confirm_time,
            }
            in_msg_data = json.dumps(in_msg_data)
            my_list.append(in_msg_data)

    else:
        print("doesn't get in_msg in get_tx_info()")

    out_msgs = data.get("out_msgs", [])
    if out_msgs:
        trans_id = data['hash']
        sender_address = data["account"]["address"]
        receiver_address = data["out_msgs"][0]["destination"]["address"]
        amount = int(data["out_msgs"][0]["value"]) // 10**9
        asset = "TON"
        confirm_time = data["utime"]

        if amount > 0 and sender_address != receiver_address:
            out_msgs_data = {
                "Transaction_id": trans_id,
                "Sender_address": sender_address,
                "Receiver_address": receiver_address,
                "Amount": amount,
                "Confirm_time": confirm_time,
            }
            out_msgs_data = json.dumps(out_msgs_data, indent=2)
            my_list.append(out_msgs_data)
    """
    else:
        print("doesn't get out_msgs in get_tx_info()\n")
    """


async def get_request(block_url):
    response = None
    while response is None or response.status_code != 200:
        try:
            response = requests.get(block_url)
        except requests.exceptions.RequestException as e:
            # 处理请求异常，例如连接问题
            print("Request failed:", e)
            continue
    if response.status_code == 200:
        # 这里可以处理成功响应的内容
        print("Request succeeded")
        return response
    else:
        # 处理其他响应状态码
        print("Request failed with status code:", response.status_code)


# block_id = 37876848
# get block info
async def main():
    block_id = 38303087
    for i in range(10):
        block_url = f"https://tonapi.io/v2/blockchain/blocks/(0,8000000000000000,{block_id})/transactions"
        response = await get_request(block_url)
        # time.sleep(5)
        block_data = response.json()
        if "transactions" in block_data:
            for transaction in block_data["transactions"]:
                hash_value = transaction["hash"]
                print(hash_value)
                await get_tx_info(hash_value)
            block_id += 1
        else:
            print(f"can't find transaction in block {block_id}")
            block_id += 1
            continue


if __name__ == "__main__":
    asyncio.run(main())
    for item in my_list:
        print(item, end="")
