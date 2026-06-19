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

    def remove_image(self, image_id: str):
        command = ["docker", "rmi", "-f", image_id]
        output = self.command_execute(command)
        return {"status": "success", "message": "Image removed"}

    def run_image(self, payload: dict):
        command = ["docker", "run", "-d"]
        
        if payload.get("name"):
            command.extend(["--name", payload.get("name")])
            
        if payload.get("ports"):
            ports = payload.get("ports").split(',')
            for port in ports:
                if port.strip():
                    command.extend(["-p", port.strip()])
                    
        if payload.get("volumes"):
            volumes = payload.get("volumes").split(',')
            for vol in volumes:
                if vol.strip():
                    command.extend(["-v", vol.strip()])
                    
        command.append(payload.get("image"))
        
        output = self.command_execute(command)
        return {"status": "success"}