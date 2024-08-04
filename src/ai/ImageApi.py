import json
import os
import random
import uuid
from typing import Optional

import requests
import websocket

os.environ["COMFYUI_BASE_URL"] = "testservice-morning-rain-5536.fly.dev"


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
            url = f"http://{self.server_address}/prompt"
            headers = {"Content-Type": "application/json"}
            data = json.dumps({"prompt": prompt, "client_id": client_id})
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            print(response.text)
            return response.json()

        def get_image(filename, subfolder, folder_type):
            data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
            response = requests.get(f"http://{self.server_address}/view", params=data)
            response.raise_for_status()
            return response.content

        def get_history(prompt_id):
            response = requests.get(f"http://{self.server_address}/history/{prompt_id}")
            response.raise_for_status()
            return response.json()

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

        # Determine WebSocket scheme based on address
        ws_scheme = "ws" if self.server_address.startswith("localhost") else "wss"
        ws_url = f"{ws_scheme}://{self.server_address}/ws?clientId={client_id}"
        ws = websocket.WebSocket()
        ws.connect(ws_url)
        images = get_images(ws, prompt)

        print(len(images["9"]))
        images_ = []
        for node_id in images:
            for image_data in images[node_id]:
                images_.append(image_data)

        return images_


if __name__ == "__main__":
    api = ImageApi()

    images = api.generate_image(
        "master piece",
        "bad hands",
        "sd3_medium_incl_clips_t5xxlfp8.safetensors",
        512,
        512,
    )
    print(images[0])
