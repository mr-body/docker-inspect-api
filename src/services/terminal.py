import asyncio
import fcntl
import os
import pty
import subprocess
from contextlib import asynccontextmanager

from fastapi import WebSocket, WebSocketDisconnect


@asynccontextmanager
async def _pty_process(argv: list[str]):
    """Open a PTY pair, spawn *argv*, yield (master_fd, proc), then clean up."""
    master_fd, slave_fd = pty.openpty()
    try:
        proc = subprocess.Popen(
            argv,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            close_fds=True,
        )
    finally:
        # Close slave end in parent — the child holds its own copy.
        os.close(slave_fd)

    # Make reads non-blocking so the async reader can yield to the event loop.
    flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
    fcntl.fcntl(master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    try:
        yield master_fd, proc
    finally:
        try:
            proc.kill()
            proc.wait(timeout=2)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            pass
        try:
            os.close(master_fd)
        except OSError:
            pass


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

    async with _pty_process(["bash"]) as (master_fd, proc):
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