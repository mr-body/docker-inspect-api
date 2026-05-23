import json
import subprocess


class DockerService:

    @staticmethod
    def command_execute(command):
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print("Docker command failed:", e)
            return ""


    def get_networks(self):
        command = ["docker", "network", "ls", "--format", "{{json .}}"]
        output = self.command_execute(command)

        networks = []

        for line in output.strip().split("\n"):
            if not line:
                continue
            try:
                item = json.loads(line)
                networks.append({
                    "id": item.get("ID"),
                    "name": item.get("Name"),
                    "driver": item.get("Driver"),
                    "scope": item.get("Scope")
                })
            except json.JSONDecodeError:
                continue

        return networks


    def get_images(self):
        command = ["docker", "images", "--format", "{{json .}}"]
        output = self.command_execute(command)

        images = []

        for line in output.strip().split("\n"):
            if not line:
                continue
            try:
                item = json.loads(line)
                images.append({
                    "id": item.get("ID"),
                    "repository": item.get("Repository"),
                    "tag": item.get("Tag"),
                    "created": item.get("CreatedSince"),
                    "size": item.get("Size")
                })
            except json.JSONDecodeError:
                continue

        return images


    def get_process(self):
        command = ["docker", "ps", "--format", "{{json .}}"]
        output = self.command_execute(command)

        processes = []

        for line in output.strip().split("\n"):
            if not line:
                continue
            try:
                item = json.loads(line)
                processes.append({
                    "id": item.get("ID"),
                    "image": item.get("Image"),
                    "command": item.get("Command"),
                    "running_for": item.get("RunningFor"),
                    "status": item.get("Status"),
                    "ports": item.get("Ports"),
                    "name": item.get("Names")
                })
            except json.JSONDecodeError:
                continue

        return processes