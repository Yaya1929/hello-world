def main():
    privates = [line.strip() for line in open('privates.txt').readlines()]
    proxies = [{'http': f'http://{line.strip()}', 'https': f'http://{line.strip()}'} for line in open('proxies.txt').readlines()]

    privates_proxies = list(zip(privates, proxies))
    random.shuffle(privates_proxies)
    for private, proxy in privates_proxies:
        try:
            bearer = get_bearer(private, proxy)
            if claim_ronin_also and privates_proxies.count((private, proxy)) == 1 and chain_id != 2020:
                prepare_transaction_data(web3.eth.account.from_key(private).address, bearer, proxy, 2020)
            tx_data = prepare_transaction_data(web3.eth.account.from_key(private).address, bearer, proxy, chain_id)
            if chain_id != 2020:
                claim_daily(private, tx_data)
            sleep = random.randint(*delay)
            logger.info(f'Sleeping for {sleep} s.')
            time.sleep(sleep)
        except Exception as e:
            logger.error(f'{web3.eth.account.from_key(private).address} | {e}')
            if privates_proxies.count((private, proxy)) < retry_count:
                privates_proxies.append((private, proxy))
