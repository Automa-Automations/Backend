<div align="center">
  <h1><code>ComfyUI Demo</code></h1>
</div>

[ComfyUI](https://github.com/comfyanonymous/ComfyUI) will let you design and execute advanced Stable Diffusion pipelines using a graph/nodes/flowchart based interface.

> [!IMPORTANT]  
> This app is designed to run on [Fly GPUs](https://fly.io/docs/gpus/) — if you try to run it on a normal Fly Machine, you're gonna have a Bad Time™

## Deploy

```
fly launch --from https://github.com/fly-apps/ComfyUI-demo
```

## Update ComfyUI

```
git pull --recurse-submodules
```

## Download model checkpoints

**SSH to your Fly Machine**
```
fly ssh console
```

**Download the `huggingface_hub` CLI tool**
```
pip install -U "huggingface_hub[cli]"
```

**Log in to Hugging Face**
```
huggingface-cli login --token $HUGGINGFACE_TOKEN 
```

**Download model checkpoints** (For SD3, you'll need to accept the agreement [here](https://huggingface.co/stabilityai/stable-diffusion-3-medium))
```
huggingface-cli download stabilityai/stable-diffusion-3-medium sd3_medium_incl_clips_t5xxlfp8.safetensors --local-dir /app/models/checkpoints
```

## Visit your app
```
fly apps open
```


## Having trouble?

Create an issue or ask a question here: https://community.fly.io/
