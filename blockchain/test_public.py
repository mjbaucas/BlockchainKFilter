from public_blockchain import Chain as PublicBlockchain

@profile
def main():
    pchain = PublicBlockchain(3)

    proof = pchain.proof_of_work(pchain.gen_block)
    print(pchain.verify_proof(pchain.gen_block, proof))

if __name__ == "__main__":
    main()