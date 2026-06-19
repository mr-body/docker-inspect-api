import asyncio
import fcntl
import os
import pwd
import pty
import subprocess
from contextlib import asynccontextmanager
from fastapi import WebSocket, WebSocketDisconnect


@asynccontextmanager
async def _pty_process(argv: list[str], preexec_fn=None, cwd=None):
    master_fd, slave_fd = pty.openpty()

    env = os.environ.copy()

    try:
        proc = subprocess.Popen(
            argv,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            close_fds=True,
            preexec_fn=preexec_fn,
            cwd=cwd,
            env=env  
        )
    finally:
        os.close(slave_fd)

    flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
    fcntl.fcntl(master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    try:
        yield master_fd, proc
    finally:
        try:
            proc.kill()
            proc.wait(timeout=2)
        except Exception:
            pass
        os.close(master_fd)


async def _pty_reader(master_fd: int, ws: WebSocket, stop: asyncio.Event) -> None:
    """Read from *master_fd* and forward bytes to the WebSocket until *stop* is set."""
    try:
        while not stop.is_set():
            try:
                data = os.read(master_fd, 4096)
                if data:
                    await ws.send_text(data.decode(errors="replace"))
            except BlockingIOError:
                await asyncio.sleep(0.01)
            except OSError:
                # master_fd was closed — process exited.
                break
    finally:
        stop.set()

def demote_user(username: str):
    """Run process as a different Linux user."""
    def result():
        user = pwd.getpwnam(username)
        os.setgid(user.pw_gid)
        os.setuid(user.pw_uid)
    return result

async def handle_terminal(ws: WebSocket, container: str, shell: str = "bash") -> None:
    """Proxy a WebSocket to a shell running inside *container* via docker exec."""
    argv = ["docker", "exec", "-it", container, shell]
    stop = asyncio.Event()

    async with _pty_process(argv) as (master_fd, proc):
        reader = asyncio.create_task(_pty_reader(master_fd, ws, stop))
        try:
            while not stop.is_set():
                try:
                    msg = await asyncio.wait_for(ws.receive_text(), timeout=0.5)
                    if msg:
                        os.write(master_fd, msg.encode())
                except asyncio.TimeoutError:
                    # Check stop flag and loop again.
                    continue
                except WebSocketDisconnect:
                    break
        finally:
            stop.set()
            reader.cancel()
            try:
                await reader
            except asyncio.CancelledError:
                pass


async def handle_host_terminal(ws: WebSocket) -> None:
    """Proxy a WebSocket to a local bash session on the host."""
    stop = asyncio.Event()

    user = pwd.getpwnam("docker-inspect")

    async with _pty_process(["bash"], preexec_fn=demote_user("docker-inspect"), cwd=user.pw_dir) as (master_fd, proc):
        reader = asyncio.create_task(_pty_reader(master_fd, ws, stop))
        try:
            while not stop.is_set():
                try:
                    msg = await asyncio.wait_for(ws.receive_text(), timeout=0.5)
                    if msg:
                        os.write(master_fd, msg.encode())
                except asyncio.TimeoutError:
                    continue
                except WebSocketDisconnect:
                    break
        finally:
            stop.set()
            reader.cancel()
            try:
                await reader
            except asyncio.CancelledError:
                pass