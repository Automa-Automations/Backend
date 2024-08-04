import json
import urllib.parse
import urllib.request
import uuid

import websocket


class ComfyUI:
    server_address: str = ""

    def generate(self, prompt):
        client_id = str(uuid.uuid4())

        def queue_prompt(prompt):
            p = {"prompt": prompt, "client_id": client_id}
            data = json.dumps(p).encode("utf-8")
            req = urllib.request.Request(
                "http://{}/prompt".format(self.server_address), data=data
            )
            return json.loads(urllib.request.urlopen(req).read())

        def get_image(filename, subfolder, folder_type):
            data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
            url_values = urllib.parse.urlencode(data)
            with urllib.request.urlopen(
                "http://{}/view?{}".format(self.server_address, url_values)
            ) as response:
                return response.read()

        def get_history(prompt_id):
            with urllib.request.urlopen(
                "http://{}/history/{}".format(self.server_address, prompt_id)
            ) as response:
                return json.loads(response.read())

        def get_images(ws, prompt):
            prompt_id = queue_prompt(prompt)["prompt_id"]
            output_images = {}
            while True:
                out = ws.recv()
                if isinstance(out, str):
                    message = json.loads(out)
                    if message["type"] == "executing":
                        data = message["data"]
                        if data["node"] is None and data["prompt_id"] == prompt_id:
                            break  # Execution is done
                else:
                    continue  # previews are binary data

            history = get_history(prompt_id)[prompt_id]
            for node_id in history["outputs"]:
                node_output = history["outputs"][node_id]
                if "images" in node_output:
                    images_output = []
                    for image in node_output["images"]:
                        image_data = get_image(
                            image["filename"], image["subfolder"], image["type"]
                        )
                        images_output.append(image_data)
                    output_images[node_id] = images_output

            return output_images

        prompt_json = ""
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.server_address, client_id))
        images = get_images(ws, prompt)

        print(len(images["9"]))
        images_ = []
        for node_id in images:
            for image_data in images[node_id]:
                image = image_data
                images_.append(image)

        return images_
