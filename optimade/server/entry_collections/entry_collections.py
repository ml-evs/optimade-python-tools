from abc import abstractmethod
from typing import Collection, Tuple, List

from optimade.server.mappers import BaseResourceMapper
from optimade.filterparser import LarkParser
from optimade.models import EntryResource
from optimade.server.query_params import EntryListingQueryParams
from optimade.server.schemas import ENTRY_SCHEMAS


class EntryCollection(Collection):  # pylint: disable=inherit-non-class
    def __init__(
        self,
        collection,
        resource_cls: EntryResource,
        resource_mapper: BaseResourceMapper,
    ):
        self.collection = collection
        self.parser = LarkParser()
        self.resource_cls = resource_cls
        self.resource_schema = ENTRY_SCHEMAS.get(resource_mapper.ENDPOINT)
        self.resource_mapper = resource_mapper

    def __len__(self):
        return self.collection.count()

    def __iter__(self):
        return self.collection.find()

    def __contains__(self, entry):
        return self.collection.count(entry) > 0

    def get_attribute_fields(self) -> set:
        return set(self.resource_schema.keys())

    @abstractmethod
    def find(
        self, params: EntryListingQueryParams
    ) -> Tuple[List[EntryResource], int, bool, set]:
        """
        Fetches results and indicates if more data is available.

        Also gives the total number of data available in the absence of page_limit.

        Args:
            params (EntryListingQueryParams): entry listing URL query params

        Returns:
            Tuple[List[Entry], int, bool, set]: (results, data_returned, more_data_available, fields)

        """

    def count(self, **kwargs):
        return self.collection.count(**kwargs)
