"""
Telegram Data Center (DC) addresses and configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class DataCenter:
    """
    Represents a Telegram Data Center endpoint.
    """

    dc_id: int
    ip_address: str
    port: int = 443
    is_test: bool = False
    is_media: bool = False

    @property
    def address(self) -> tuple[str, int]:
        return self.ip_address, self.port


# Official Telegram Production Data Centers
PROD_DCS: dict[int, DataCenter] = {
    1: DataCenter(dc_id=1, ip_address="149.154.175.53", port=443),
    2: DataCenter(dc_id=2, ip_address="149.154.167.51", port=443),
    3: DataCenter(dc_id=3, ip_address="149.154.175.100", port=443),
    4: DataCenter(dc_id=4, ip_address="149.154.167.91", port=443),
    5: DataCenter(dc_id=5, ip_address="91.108.56.130", port=443),
}

# Official Telegram Test Data Centers
TEST_DCS: dict[int, DataCenter] = {
    1: DataCenter(dc_id=1, ip_address="149.154.175.10", port=443, is_test=True),
    2: DataCenter(dc_id=2, ip_address="149.154.167.40", port=443, is_test=True),
    3: DataCenter(dc_id=3, ip_address="149.154.175.117", port=443, is_test=True),
}


def get_dc(dc_id: int, test_mode: bool = False) -> DataCenter:
    """
    Get DataCenter configuration by DC ID.

    :param dc_id: Telegram Data Center ID (1-5 for production, 1-3 for test).
    :param test_mode: Connect to Telegram Test Data Centers.
    :return: DataCenter instance.
    :raises ValueError: If dc_id is not a recognized Data Center ID.
    """
    dc_map = TEST_DCS if test_mode else PROD_DCS
    if dc_id in dc_map:
        return dc_map[dc_id]
    env_name = "test" if test_mode else "production"
    msg = f"Unknown DC ID: {dc_id} for {env_name} environment (valid: {sorted(dc_map.keys())})"
    raise ValueError(msg)
