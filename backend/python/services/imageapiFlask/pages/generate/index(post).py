from flask import jsonify, request
from pydantic import ValidationError
from src.ImageApi.main import ImageAPI, ImageGenerationInput


def default():
    try:
        # Attempt to create a Pydantic model instance from the request data
        image_prompt = ImageGenerationInput(**request.json)
    except ValidationError as ve:
        # Handle Pydantic validation errors
        return jsonify({"message": "Invalid input data", "errors": ve.errors()}), 400
    except Exception as e:
        # Handle other exceptions (e.g., missing JSON body)
        return jsonify({"message": "Error processing request", "error": str(e)}), 400

    try:
        # Attempt to generate images
        images = ImageAPI.generate(image_prompt)
    except Exception as e:
        # Handle errors related to image generation
        return jsonify({"message": "Error generating images", "error": str(e)}), 500

    if not images:
        return jsonify({"message": "There were no images generated!"}), 500

    # Return the generated images in JSON format
    return jsonify(images.model_dump(mode="json")), 200
