from labelbox.client import Client
from ._converter import _lb_converter

class coco_converter(_lb_converter):
    def __init__(self, project_id: str, client: Client, ontology_mapping: dict[str:str]) -> None:
        super().__init__(project_id, client, ontology_mapping)