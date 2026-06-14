import subprocess
from src.util.command import Command


class LogsService(Command):

    def get_logs(self, identifier: str, tail: int = 100):
        command = ["docker", "logs", "--tail", str(tail), identifier]
        output = self.command_execute(command)

        if isinstance(output, bytes):
            output = output.decode("utf-8")

        return output.splitlines()

    def stream_logs(self, identifier: str):
        process = subprocess.Popen(
            ["docker", "logs", "-f", identifier],  # FIX 1
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        return process