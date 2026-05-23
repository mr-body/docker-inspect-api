import subprocess
import logging

logger = logging.getLogger(__name__)

class Command:
    def command_execute(self, command: list[str]) -> str:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            return result.stdout

        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e.stderr}")
            return e.stderr or ""

        except subprocess.TimeoutExpired:
            logger.error("Command timed out")
            return "timeout"