"""
Module for harvesting metadata for Community's collection from Zenodo.

Our goal is to transform XML accessible at a URL into a series of Python
objects with metadata attributes.
"""

import requests


def harvest_collection(community_name, format='oai_datacite3'):
    """Harvest a Zenodo community into a set of Python objects.

    Parameters
    ----------
    community_name : str
        Name of the community.
    format : str
        OAI-PMH metadata specification name. See https://zenodo.org/dev.

    Returns
    -------
    url : str
        OAI-PMH metadata URL.
    """
    harvesters = {'oai_datacite3': harvest_oai_datacite3}
    harvester = harvesters[format]

    url = zenodo_harvest_url(community_name, format)
    r = requests.get(url)
    r.status_code
    xml_content = r.content

    return harvester(xml_content)


def zenodo_harvest_url(community_name, format):
    """Build a URL for the Zenodo Community's metadata.

    Parameters
    ----------
    community_name : str
        Name of the community.
    format : str
        OAI-PMH metadata specification name. See https://zenodo.org/dev.

    Returns
    -------
    url : str
        OAI-PMH metadata URL.
    """
    template = 'http://zenodo.org/oai2d?verb=ListRecords&' \
               'metadataPrefix={metadata_format}&set=user-{community}'
    return template.format(metadata_format=format,
                           community=community_name)


def harvest_oai_datacite3(xml_content):
    """Factory for Zenodo Record objects from ``oai_datacite3`` XML

    Parameters
    ----------
    xml_content : str
        Content from the Zenodo harvesting URL endpoint for ``oai_datacite3``.

    Returns
    -------
    records : list
        Zenodo record objects derived from the `xml_content`.
    """
    records = []
    return records
