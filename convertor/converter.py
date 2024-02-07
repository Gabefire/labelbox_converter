import labelbox as lb

class lb_converter:
    def __init__(self, project_id, client, ontology_mapping) -> None:
        self.client: lb.Client = client
        self.project: str = project_id
        self.ontology_mapping: list[dict[str:str]] = ontology_mapping
    def export_data_row(self) -> list[dict[str:str]]:
        project = self.client.get_project(self.project)
        
        self.client.enable_experimental = True

        export_params= {
        "attachments": False,
        "metadata_fields": False,
        "data_row_details": True,
        "project_details": True,
        "label_details": True,
        "performance_details": False,
        "interpolated_frames": True
        }

        filters= {
        # "data_row_ids": ["", ""],
        # "batch_ids": ["", ""],
        }

        export_task = project.export(params=export_params)
        export_task.wait_till_done()
        
        data_rows = []

        if export_task.has_errors():
            export_task.get_stream(
            converter=lb.JsonConverter(),
            stream_type=lb.StreamType.ERRORS
            ).start(stream_handler=lambda error: print(error))

        if export_task.has_result():
            stream = export_task.get_stream(
            converter=lb.JsonConverter(),
            stream_type=lb.StreamType.RESULT
            )
            for output in stream:
                data_rows.append(output.json_str)
        
        return data_rows
