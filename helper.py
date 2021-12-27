from models import *
from dataclasses import dataclass

@dataclass
class ListResponse:
    list: list
    start_index: int = 1
    count: int = None
    total_results:  int = 0 # versus total_results = int = 0 which means set to default to 0

    def scim_response(self):
        resources = []
        for item in self.list:
            resources.append(item.scim_response())
        rv = {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
            "totalResults": self.total_results,
            "startIndex": self.start_index,
            "Resources": []
        }
        if self.count:
            rv['itemsPerPage'] = self.count
        rv['Resources'] = resources
        return rv