import json
from src.util.command import Command


class VolumeService(Command):
    def get_volumes(self):
        command = ["docker", "volume", "ls", "--format", "{{json .}}"]
        output = self.command_execute(command)

        volumes = []

        for line in output.strip().split("\n"):
            if not line:
                continue
            try:
                item = json.loads(line)
                volumes.append({
                    "name": item.get("Name"),
                    "driver": item.get("Driver"),
                })
            except json.JSONDecodeError:
                continue

        return volumes
    
    def inspect_volume(self, name: str):
        command = ["docker", "volume", "inspect", name, "--format", "{{json .}}"]
        output = self.command_execute(command)

        try:
            data = json.loads(output)[0]

            return {
                "name": data.get("Name"),
                "driver": data.get("Driver"),
                "mountpoint": data.get("Mountpoint"),
                "created": data.get("CreatedAt"),
                "labels": data.get("Labels"),
                "scope": data.get("Scope"),
            }

        except (json.JSONDecodeError, IndexError):
            return {"error": "Invalid volume data"}