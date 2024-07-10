import time

import click
import docker
from pyngrok import ngrok
from yaspin import yaspin

from bunker_src.docker import is_service_running, container_runner


def ngrok_container(service: str):
    with yaspin(text=f"🚀 Publishing Container via NGROK...") as sp:
        if not is_service_running(service):
            sp.text = "🛑 Service is not running. Starting service..."
            container_runner(service)

        # Get the exposed external port
        sp.text = "🔍 Getting external port..."
        client = docker.from_env()
        container = client.containers.get(service)
        ports = container.attrs["NetworkSettings"]["Ports"]
        external_port = list(ports.keys())[0].split("/")[0]

        sp.text = "⇝ Publishing the service..."
        http_tunnel = ngrok.connect(external_port)
        sp.text = f"🎉 Service is live at: {http_tunnel.public_url}"

        click.echo(f" Press '^ + C' to stop the service")

        live_text = sp.text
        try:
            alive_for = 0
            while True:
                alive_for += 0.1
                time.sleep(0.1)
                sp.text = f"{live_text} {alive_for:.2f}s"

        except KeyboardInterrupt:
            sp.stop()
            ngrok.kill()

        click.echo(f"🎉 Service is live at: {http_tunnel.public_url}")
        click.echo("😥 Killed Ngrok Service.")
