# Algorand USD Price Oracle

[![Pull Request](https://github.com/defimono/algo_price_oracle/actions/workflows/pull_request.yaml/badge.svg)](https://github.com/defimono/algo_price_oracle/actions/workflows/pull_request.yaml)

Open source project intending to serve as a starting point for dApp development on the Algorand blockchain. In the search of publicly accessible, documented, and auditable oracles in Algorand ecosystem there is a lack of readily available sources. To this end we decided to create an Oracle to provide price information for use in Smart Contracts, open and available for all.

#### Note, this project is the smart contract update logic, not the smart contract itself. For the smart contract itself, [reference this project](https://github.com/defimono/smart_contracts).

### What is an Oracle?

Reference if you will, this excellent explanation given by [binance.com](https://academy.binance.com/en/articles/blockchain-oracles-explained)

Blockchain oracles are third-party services that provide smart contracts with external information. They serve as bridges between blockchains and the outside world.

> Blockchains and smart contracts cannot access off-chain data (data that is outside of the network). However, for many contractual agreements, it is vital to have relevant information from the outside world to execute the agreement.
> 
>This is where blockchain oracles come into play, as they provide a link between off-chain and on-chain data. Oracles are vital within the blockchain ecosystem because they broaden the scope in which smart contracts can operate. Without blockchain oracles, smart contracts would have very limited use as they would only have access to data from within their networks. 
>
>It’s important to note that a blockchain oracle is not the data source itself, but rather the layer that queries, verifies, and authenticates external data sources and then relays that information. The data transmitted by oracles comes in many forms – price information, the successful completion of a payment, or the temperature measured by a sensor.


### Why build from scratch?

To this end there are some various projects in the works by others, but I could not wait nor conform to their pricing structure as it is restrictive and prohibitive. Every query costs a transaction fee, an oracle fee, and requires going through a centralized party who acts as the toll bridge to the information. They have full authority through close sourced code to provide (and potentially manipulate) information that is business critical to smart contract logic.

This application is open source, you are fee to view and audit the smart contract as you see fit. If you see anything concerning, feel free to reach out in the [Defimono discord](https://discord.gg/umjb43DQ), open an issue here, or reach out directly.

### Who is your price source?

Currently, Coinbase is the definitive price source. There are plans to distribute the price information source and have a consensus reached via the code so that if any price source is compromised, the on-chain price is unaffected as long as the majority agree. This will take time and is due in further iterations.

### Is it secure?

It is secure as I am able to make it during the MVP phase of the project. It has NOT been audited, and as it is under active development the location, names, etc. of information can be unreliable, missing, or renamed at any time. 

This is an alpha, and not live on the mainnet until third party auditing and compliance can be obtained.

### How does it run?

Currently, it is deployed via serverless to AWS and set with a cron trigger every 5 minutes to execute. The development version is live on the testnet and the mainnet version will be coming once testing is complete. It is set to run every 5 minutes since every transaction has a gas fee of .001 algos. We do not have funding yet to be able to increase frequency, but it is desired in future iterations.

## Roadmap

Currently, in no particular order, we need to implement the following.

- Testing
- Distributed price consensus algorithm
- Observability and Alerting
- Security analysis and integration
- CI/CD deployment pipelines

## Contributing

Feel free to reach out in Discord for discussions about the direction of the project, the slack community, or open a Github issue for code specific problems that you encounter.