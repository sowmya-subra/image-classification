from pathlib import Path

from django.conf import settings

_model = None


def get_model():
    global _model
    if _model is None:
        import tensorflow as tf
        path = Path(settings.BASE_DIR) / "mnist_cnn_model.keras"
        _model = tf.keras.models.load_model(path)
    return _model
