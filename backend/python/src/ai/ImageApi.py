import random
import websocket
from src.Classes.User import DatabaseSyncedProfile
import uuid
from typing import Optional
import json
import urllib.request
import urllib.parse
import os


class ImageApi:
    server_address = (
        os.environ["COMFYUI_BASE_URL"].replace("https://", "").replace("http://", "")
    )

    def generate_image(
        self,
        prompt_: str,
        negative_prompt: str,
        model: str,
        width: int,
        height: int,
        seed: int = 0,
        batch_size: int = 1,
        user_id: Optional[str] = None,
    ) -> list[bytes]:
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
            for o in history["outputs"]:
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

        prompt_text = """
        {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": 8,
                    "denoise": 1,
                    "latent_image": [
                        "5",
                        0
                    ],
                    "model": [
                        "4",
                        0
                    ],
                    "negative": [
                        "7",
                        0
                    ],
                    "positive": [
                        "6",
                        0
                    ],
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "seed": 8566257,
                    "steps": 20
                }
            },
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": "v1-5-pruned-emaonly.ckpt"
                }
            },
            "5": {
                "class_type": "EmptyLatentImage",
                "inputs": {
                    "batch_size": 1,
                    "height": 512,
                    "width": 512
                }
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "clip": [
                        "4",
                        1
                    ],
                    "text": "masterpiece best quality girl"
                }
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "clip": [
                        "4",
                        1
                    ],
                    "text": "bad hands"
                }
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": [
                        "3",
                        0
                    ],
                    "vae": [
                        "4",
                        2
                    ]
                }
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": "ComfyUI",
                    "images": [
                        "8",
                        0
                    ]
                }
            }
        }
        """
        if model.startswith("json-workflow"):
            me_ = model.replace("<PROMPT HERE>", prompt_)
            me_ = me_.replace("<NEGATIVE PROMPT HERE>", negative_prompt)
            me_ = me_.replace("<WIDTH HERE>", str(width))
            me_ = me_.replace("<HEIGHT HERE>", str(height))
            me_ = me_.replace("<BATCH SIZE HERE>", str(batch_size))
            me_ = me_.replace(
                "<SEED HERE>", str(random.randint(0, 10000000) if seed == 0 else seed)
            )
            prompt = json.loads(me_.replace("json-workflow", ""))
        else:
            prompt = json.loads(prompt_text)
            prompt["6"]["inputs"]["text"] = prompt_
            prompt["7"]["inputs"]["text"] = negative_prompt
            prompt["4"]["inputs"]["ckpt_name"] = model
            prompt["5"]["inputs"]["width"] = width
            prompt["5"]["inputs"]["height"] = height
            prompt["5"]["inputs"]["batch_size"] = batch_size
            prompt["3"]["inputs"]["seed"] = (
                random.randint(0, 10000000) if seed == 0 else seed
            )

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


if __name__ == "__main__":
    api = ImageApi()
    api.server_address = "localhost:8188"

    images = api.generate_image(
        "master piece", "bad hands", "v1-5-pruned-emaonly.ckpt", 512, 512
    )
    print(images[0])
