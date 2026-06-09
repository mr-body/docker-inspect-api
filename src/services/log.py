import subprocess
from src.util.command import Command


class LogsService(Command):

    def get_logs(self, identifier: str, tail: int = 100):
        command = ["logs", "--tail", str(tail), identifier]
        output = self.command_execute(command)

        if isinstance(output, bytes):
            output = output.decode("utf-8")

        # Apenas retorna logs como texto limpo
        return output.splitlines()


    def stream_logs(self, identifier: str):
        """
        Streaming real com docker logs -f
        """
        process = subprocess.Popen(
            ["logs", "-f", identifier],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        return process