import json
from src.util.command import Command


class NetworkService(Command):
    def get_networks(self):
        command = ["docker", "network", "ls", "--format", "{{json .}}"]
        output = self.command_execute(command)

        if isinstance(output, bytes):
            output = output.decode("utf-8")

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

    def inspect_network(self, network_id: str):
        command = ["docker", "network", "inspect", network_id]
        output = self.command_execute(command)

        try:
            data = json.loads(output)

            if isinstance(data, list):
                data = data[0] if data else {}

            return {
                "id": data.get("Id"),
                "name": data.get("Name"),
                "driver": data.get("Driver"),
                "scope": data.get("Scope"),
                "containers": data.get("Containers", {}),
                "options": data.get("Options", {}),
                "ipam": data.get("IPAM", {}),
            }

        except json.JSONDecodeError:
            return {"error": "Invalid JSON from docker"}