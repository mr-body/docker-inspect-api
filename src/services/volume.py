import json
import os
from pathlib import Path
from src.util.command import Command


class VolumeService(Command):
    def get_volumes(self):
        command = ["docker", "volume", "ls", "--format", "{{json .}}"]
        output = self.command_execute(command)

        if isinstance(output, bytes):
            output = output.decode("utf-8")
            
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
        command = ["docker", "volume", "inspect", name]
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

    def list_volume_files(self, name: str):
        command = ["docker", "volume", "inspect", name]
        output = self.command_execute(command)

        try:
            data = json.loads(output)[0]
            mountpoint = data.get("Mountpoint")

            if not mountpoint or not os.path.exists(mountpoint):
                return {
                    "error": "Mountpoint not found",
                    "mountpoint": mountpoint
                }

            files = []

            for item in Path(mountpoint).iterdir():
                files.append({
                    "name": item.name,
                    "type": "dir" if item.is_dir() else "file",
                    "path": str(item)
                })

            return {
                "volume": name,
                "mountpoint": mountpoint,
                "files": files
            }

        except Exception as e:
            return {"error": str(e)}