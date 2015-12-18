"""
Module for harvesting metadata for Community's collection from Zenodo.

Our goal is to transform XML accessible at a URL into a series of Python
objects with metadata attributes.
"""

import datetime

import requests
import xmltodict


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
    xml_dataset = xmltodict.parse(xml_content, process_namespaces=False)
    xml_records = xml_dataset['OAI-PMH']['ListRecords']['record']

    records = [Datacite3Record(xml_record) for xml_record in xml_records]
    return records


class Datacite3Record(object):
    """Zenodo record derived from Datacite v3 metadata."""
    def __init__(self, record_metadata):
        super(Datacite3Record, self).__init__()
        self._record_metadata = record_metadata
        self._resource = self._record_metadata['metadata']['oai_datacite']['payload']['resource']  # NOQA

    @property
    def authors(self):
        """List of authors.

        These are `dict`\ s with keys:

        - 'name'
        - 'affiliation'
        """
        return {{'name': a['creatorName'],
                 'affiliation': a['affiliation']}
                for a in self._resource['creators']['creator']}

    @property
    def doi(self):
        return self._resource['identifier']['#text']

    @property
    def title(self):
        return self._resource['titles']['title']

    @property
    def abstract_html(self):
        return self._resource['descriptions']['description']['#text']

    @property
    def date(self):
        return datetime.datetime.strptime(
            self._resource['dates']['date']['#text'], '%Y-%m-%d')
