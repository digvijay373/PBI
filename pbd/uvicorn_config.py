# run_asgi.py
import uvicorn
import multiprocessing
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from pbd.asgi import application
from django.conf import settings

class ASGIServer:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 8000
        self.workers = multiprocessing.cpu_count() * 4 + 1

        # Create Starlette app with mounted routes
        routes = [
            Mount("/static", app=StaticFiles(directory=settings.STATIC_ROOT), name="static"),
            Mount("/", app=application)  # Mount Django application at root
        ]
        self.app = Starlette(routes=routes)

    def run(self):
        config = uvicorn.Config(
            app=self.app,
            host=self.host,
            port=self.port,
            workers=self.workers,
            loop="auto",
            limit_concurrency=1000,
            limit_max_requests=10000,
            timeout_keep_alive=30,
            log_level="info",
            access_log=True,
            proxy_headers=True,
            forwarded_allow_ips="*",
            headers=[
                ("Access-Control-Allow-Origin", "*"),
                ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
                ("Access-Control-Allow-Headers", "Content-Type"),
            ]
        )
        server = uvicorn.Server(config)
        server.run()

if __name__ == "__main__":
    server = ASGIServer()
    server.run()