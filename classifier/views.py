import base64
import io

import numpy as np
from django.shortcuts import render

from .csv_parser import BadCSV, parse_csv
from .model_loader import get_model


def writeup(request):
    return render(request, "writeup.html")


def array_to_data_uri(array):
    from PIL import Image

    pixels = (array.reshape(28, 28) * 255).astype("uint8")
    image = Image.fromarray(pixels, mode="L").resize((196, 196), Image.NEAREST)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def classify(request):
    if request.method != "POST":
        return render(request, "classify.html")

    uploaded = request.FILES.get("csv_file")
    if uploaded is None:
        return render(request, "classify.html", {"error": "Please choose a file first."})

    try:
        array = parse_csv(uploaded)
    except BadCSV as exc:
        return render(request, "classify.html", {"error": str(exc)})

    predictions = get_model().predict(array, verbose=0)[0]
    digit = int(np.argmax(predictions))
    confidence = float(predictions[digit]) * 100

    return render(
        request,
        "classify.html",
        {
            "digit": digit,
            "confidence": f"{confidence:.1f}",
            "image": array_to_data_uri(array),
        },
    )