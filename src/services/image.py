import json
from src.util.command import Command


class ImageService(Command):
    def get_images(self):
        command = ["docker", "images", "--format", "{{json .}}"]
        output = self.command_execute(command)

        if isinstance(output, bytes):
            output = output.decode("utf-8")
            
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