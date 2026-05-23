import subprocess

class Command:
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