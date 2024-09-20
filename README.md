# rohub-sync-action

A github action that will make your gh-repo into a rohub resource

## Usage

````yaml
name: Sync to ROHub
on:
  push:
    branches:
      - master

jobs:
    sync:
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@v2
        - uses: vliz-be-opsci/rohub-sync-action@latest
        with:
            rohub-user: ${{ secrets.ROHUB_TOKEN }}
            rohub-password: ${{ secrets.ROHUB_PASSWORD }}
    ```
````

### what will happen

On first push this action will create a new rohub resource with the same name as the github repo. It will then push the contents of the repo to the rohub resource.

On subsequent pushed it will check the rocrate-metadata.jsonld file and check if resources need to be added to rohub or updated on the gh-repo.

This action will also add a gh-button to the repo that will link to the rohub resource.

### Secrets

- `ROHUB_TOKEN`
- `ROHUB_PASSWORD`
