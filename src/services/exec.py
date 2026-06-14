import subprocess
from pydantic import BaseModel

class ExecRequest(BaseModel):
    container: str
    command: str

class ExecService:
    def exec_command(self, payload: ExecRequest):
        try:
            full_command = [
                "docker", "exec", "-i",
                payload.container,
                "sh", "-c",
                payload.command
            ]

            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True
            )

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "code": result.returncode
            }

        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "code": 500
            }