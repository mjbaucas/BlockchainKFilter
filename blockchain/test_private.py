from private_blockchain import Chain as PrivateBlockchain

@profile
def main():
    trusted_list = [
        "10.120.16.240",
        "10.120.16.240",
        "10.120.16.240",
        "10.120.16.240"
    ]

    pchain = PrivateBlockchain()
    pchain.gen_next_block("0", trusted_list)

    print("" in pchain.output_ledger())


if __name__ == "__main__":
    main()