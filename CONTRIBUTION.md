# Contribution 

## Workflows

## Documentation

ezglossary's documenation can be generated using either
`properdocs` or `mkdocs`:

    virtualenv .env
    . .env/bin/activate

    pip3 install -r etc/requirements.txt
    pip3 install .

    properdocs build

    open site/index.html

!!! Note

    The `etc/requirements.txt` has been updated to
    use ProperDocs.

## Testing

This repository contains a set of automated tests that run as part of the release pipeline.

Those tests function as regression tests and need to pass in order to merge a pull request.

You can run these tests locally using `tox`:

    cd mkdocs-ezglossary-plugin
    tox

