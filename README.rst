tutor-contrib-shipyard plugin for `Tutor <https://docs.tutor.overhang.io>`__
============================================================================

This tutor plugin contains a opinionated configuration that Edunext uses to deploy and manage Open edX instances. The following features are included:

- Integration of New Relic monitoring
- Add flowers deployment for Celery
- Add a custom nginx and cert-manager configuration
- Add a set of debug resources to help diagnose issues

Installation
------------

::

    pip install git+https://github.com/edunext/tutor-contrib-shipyard

Usage
-----

::

    tutor plugins enable tutor-contrib-shipyard
    tutor config save

Configuration
-------------

The following configuration options are available:

- `SHIPYARD_NEW_RELIC`: Whether to enable New Relic monitoring
- `SHIPYARD_NEW_RELIC_LICENSE_KEY`: New Relic license key
- `SHIPYARD_AUTO_TLS`: Whether to automatically generate TLS certificates using cert-manager
- `SHIPYARD_INGRESS`: Whether to use an ingress controller
- `SHIPYARD_INGRESS_EXTRA_HOSTS`: Extra hosts to add to the ingress controller
- `SHIPYARD_CUSTOM_CERTS`: Whether to use custom TLS certificates
- `SHIPYARD_FLOWERS`: Whether to deploy flowers for Celery
- `SHIPYARD_DEBUG`: Whether to deploy debug resources

License
-------

This software is licensed under the terms of the AGPLv3.
