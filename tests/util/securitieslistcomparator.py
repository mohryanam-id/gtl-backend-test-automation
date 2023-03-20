from collections import namedtuple
from csv import DictReader
from typing import Dict, List, Tuple
import logging


logging.basicConfig(level=logging.INFO)


class Securities(namedtuple("Securities", ["name", "symbol", "exchange", "listing_date", "outstanding_shares"])):
    """A named tuple representing a security."""
    __slots__ = ()

    def __str__(self):
        return f"{self.name} | {self.symbol} | {self.exchange}"

class SecuritiesListComparer:
    """A class for comparing two CSV files containing securities lists."""

    def __init__(self, actual_csv_reader, expected_csv_reader):
        self.actual_csv_reader = actual_csv_reader
        self.expected_csv_reader = expected_csv_reader

    def read_csv(self, csv_reader) -> List[Securities]:
        """CSV reader containing securities data and returns a list of Securities objects."""
        securities_list = []
        for row in csv_reader:
            securities = Securities(
                name=row["NAME OF COMPANY"],
                symbol=row["SYMBOL"],
                exchange=row["Exchange Market"],
                listing_date=row["DATE OF LISTING"],
                outstanding_shares=row["Outstanding Shares"]
            )
            securities_list.append(securities)
        return securities_list

    def compare_listing_date_and_outstanding_shares(self, actual_securities, expected_securities, storage_securities):
        actual_outstanding_shares = actual_securities.outstanding_shares
        actual_listing_date = actual_securities.listing_date
        expected_outstanding_shares = expected_securities.outstanding_shares
        expected_listing_date = expected_securities.listing_date
        if actual_outstanding_shares != expected_outstanding_shares or actual_listing_date != expected_listing_date:
            storage_securities.append(actual_securities)

    def compare(self) -> Tuple[List[Securities], List[Securities]]:
        """Compares two CSV files containing securities data and returns a tuple of added and removed securities."""
        actual_securities = self.read_csv(self.actual_csv_reader)
        expected_securities = self.read_csv(self.expected_csv_reader)
        actual_securities_dict = self._to_dict(actual_securities)
        expected_securities_dict = self._to_dict(expected_securities)

        updated_securities = []
        removed_securities = []
        added_securities = []

        for composite_key, securities in actual_securities_dict.items():
            if composite_key not in expected_securities_dict.keys():
                added_securities.append(securities)
            else:
                self.compare_listing_date_and_outstanding_shares(securities,expected_securities_dict[composite_key], updated_securities)

        for composite_key, securities in expected_securities_dict.items():
            if composite_key not in actual_securities_dict.keys():
                removed_securities.append(securities)
            else:
                self.compare_listing_date_and_outstanding_shares(securities,expected_securities_dict[composite_key], updated_securities)

        return added_securities, removed_securities, updated_securities

    def _to_dict(self, securities_list: List[Securities]) -> Dict[Tuple[object, object, object], Securities]:
        """Converts a list of securities to a dictionary where the key is the security symbol."""
        return {(securities.name, securities.symbol, securities.exchange): securities for securities in securities_list}
