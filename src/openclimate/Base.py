from dataclasses import dataclass


@dataclass
class Base:
    """Base API class
    define HTTP access to API

    Returns:
        object
    """

    version: str = "/api/v1"
    base_url: str = "https://openclimate.openearth.dev"
    server: str = f"{base_url}{version}"

    def __repr__(self):
        return f"OpenClimate({self.server})"

    def __str__(self):
        return f"OpenClimate({self.server})"
