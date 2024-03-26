# External Secrets Keyring

Creates an API to access secrets stored by `keyring` via Kubernetes External Secrets Operator webhook provider.
This is useful in a lab setup, but is probably not a good idea in production settings.

An API key is required when submitting requests to prevent unauthorized users from querying the keystore.

## Installation

Installation can be done through `pip`:

```sh
pip  install esokeyring
```

You can optionally install [Uvicorn](https://www.uvicorn.org/) to run the API:

```sh
pip install esokeyring[uvicorn]
```
