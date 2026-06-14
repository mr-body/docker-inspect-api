import os
import pty
import fcntl
import asyncio
import subprocess

async def handle_terminal(
    ws,
    container: str,
    shell: str = "sh",
):

    master_fd, slave_fd = pty.openpty()

    proc = subprocess.Popen(
        ["docker", "exec",  "-it", container, shell],
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True,
    )

    os.close(slave_fd)

    flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
    fcntl.fcntl(master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    async def pty_reader():
        while True:
            try:
                data = os.read(master_fd, 2048)

                if data:
                    await ws.send_text(
                        data.decode(errors="ignore")
                    )

            except BlockingIOError:
                await asyncio.sleep(0.01)

            except Exception:
                break

    asyncio.create_task(pty_reader())

    try:
        while True:
            msg = await ws.receive_text()
            os.write(master_fd, msg.encode())

    finally:
        proc.kill()
        os.close(master_fd)