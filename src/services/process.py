import json
from src.util.command import Command


class ProcessService(Command):
    def get_process(self):
        command = ["docker", "ps", "--format", "{{json .}}"]
        output = self.command_execute(command)

        if isinstance(output, bytes):
            output = output.decode("utf-8")

        processes = []

        for line in output.splitlines():
            line = line.strip()
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
            except json.JSONDecodeError as e:
                print("JSON inválido:", line, e)
                continue
        return processes