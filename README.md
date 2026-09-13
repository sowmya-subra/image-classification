# Image Classification — MNIST Digit Classifier

Group Project 1 for Optimization: a convolutional neural network trained to classify
handwritten digits from the MNIST dataset (target: >99% test accuracy), wrapped in an
interactive Django webpage that lets a signed-in user upload a 28x28 CSV of pixel
intensities and get back a live classification.

## Project goals

1. Train a CNN on MNIST that exceeds 99% accuracy on a held-out validation set
   (`validation_split = 0.2`), then retrain the winning architecture on the full
   training set and report/analyze its performance on the official MNIST test set.
2. Plot and analyze misclassified digits — what gets confused with what, and why.
3. Build an interactive two-page website (login-gated "blog post" style) that:
   - describes how the network was built and what worked/didn't, and
   - lets a visitor upload a CSV, see the image, and get a live prediction from the
     trained TensorFlow model.
4. Deploy the site on AWS (Lightsail) behind Docker, with an ngrok tunnel kept alive
   via `tmux`, and host the code on GitHub.

## Repo contents

| File | Description |
|---|---|
| [GP1_CNN_Training_LB_Final.ipynb](GP1_CNN_Training_LB_Final.ipynb) | Notebook that loads MNIST, trains/compares four CNN architectures, retrains the best one on the full training set, runs misclassification analysis, and exports the final model. |
| [mnist_cnn_model.keras](mnist_cnn_model.keras) | The trained/exported final model, ready to be loaded by the Django backend for inference. |

The Django project, Dockerfile, and deployment configuration are the next pieces to
be added (see [Status](#status) below).

## The model

Four architectures were trained with `validation_split=0.2`, `batch_size=64`, Adam
optimizer, and sparse categorical cross-entropy loss, using pixel values normalized to
`[0, 1]`:

| Architecture | Structure | Test accuracy |
|---|---|---|
| 1 — Simple | 1 conv (16 filters) + pool → dense(32) | 98.01% |
| 2 — Larger | 3 conv layers (64/128/128) + pool → dense(128) + dropout | 99.19% |
| 3 — Balanced | 3 conv layers (32/64/64) + pool → dense(64) + dropout | **99.25%** |
| 4 — Push for 99.5% | Architecture 2/3 style + BatchNorm, 15 epochs | 99.24% |

**Architecture 3 (Balanced)** was the best performer on the validation set, so it was
rebuilt fresh and retrained on the entire training set (no validation split). Final
result on the official MNIST test set:

> **Final test accuracy: 99.31%**

This is close to the 99.08% validation accuracy seen during model selection, which
suggests the model generalizes well rather than overfitting — training on the full
60,000 images (instead of holding back 20%) simply gave it more examples to learn
from.

### Why many small filters?

Multiple layers of smaller convolution filters (e.g. 3x3) generally outperform fewer,
larger filters, and stacking several conv/max-pool blocks helps the network build up
more abstract features — as long as you don't pool so aggressively that the flattened
feature map loses too much spatial information before it reaches the dense layers.

## Misclassification analysis

Out of 10,000 test images, the final model misclassified only **69** (0.69%). Looking
at the mistakes:

- **Common confusions:** 4→9, 6→0, 3→5, 2→1/4/7, and 1→7 show up repeatedly. These
  pairs share similar curves or strokes when handwritten quickly or messily — a 6 with
  a large loop can resemble a 0, a 2 with a sharp angled top can resemble a 7, and a 1
  written with a serif-like flick at the top can resemble a 7.
- **The mistakes aren't random.** They cluster around visually similar digit shapes
  rather than being spread evenly across all possible confusions — the model is
  failing on genuinely ambiguous handwriting, not making arbitrary errors.
- **Some errors are ambiguous even to a human eye.** Several misclassified digits (a 2
  read as a 1, a 3 read as a 5) are messy enough that a person might reasonably guess
  the same wrong answer.

**Could the model reach 100% accuracy?** Realistically, no — some handwritten digits in
the dataset are inherently ambiguous or poorly formed, so there's a ceiling on
achievable accuracy driven by the legibility of the input itself, not the model
architecture. A human classifier would likely make some of the same mistakes on these
particular images.

## Web application

The site is a Django project with two main pages, gated behind login:

1. **Write-up page** — a "medium article"-style walkthrough of how the network was
   built, what worked and what didn't, with example images of well- and poorly
   classified digits and the analysis above.
2. **Classifier page** — lets a signed-in user:
   - upload a CSV file containing a 28x28 grid of pixel intensities (no header row,
     either raw 0-255 or already-scaled 0-1 — the backend auto-detects which),
   - see the uploaded image rendered on the page,
   - get a live digit prediction from the trained TensorFlow model, and
   - click a "start over" button to upload and classify another image.

Malformed uploads (wrong dimensions, non-CSV files, etc.) surface a user-facing error
instead of a server crash.

### Auth

- Login is required to view the write-up or classifier pages.
- Self-service account creation is disabled — accounts are provisioned manually.
- A grading account is provisioned with username `dan` / password `Optimization1234`.

### Deployment

The intended deployment path:

1. Build and test the Django app + TensorFlow model locally.
2. Push the project to GitHub.
3. Spin up an AWS Lightsail instance (Linux/Unix, Django blueprint, free-tier plan).
4. On the Lightsail instance, install Docker, `git`, and `ngrok`; `git clone` the repo.
5. Build and run the app with Docker so the TensorFlow/Django backend runs entirely on
   AWS.
6. Run `ngrok config add-authtoken <token>` once to link the AWS machine to an ngrok
   account, then start the tunnel (`ngrok http <port>`) inside a `tmux` session so it
   keeps running after the SSH/browser terminal disconnects.

> Remember to delete the Lightsail instance once the free-tier period ends to avoid
> being charged.

## Status

- [x] Train and compare CNN architectures on MNIST (validation split)
- [x] Retrain best architecture on full training set, evaluate on test set (99.31%)
- [x] Plot and analyze misclassified digits
- [x] Export trained model (`mnist_cnn_model.keras`)
- [ ] Django project: login-gated write-up page
- [ ] Django project: CSV upload + classification page with "start over"
- [ ] CSV validation (shape/type checks + user-facing error messages)
- [ ] Dockerize the Django + TensorFlow backend
- [ ] Deploy to AWS Lightsail
- [ ] Expose the app publicly via `ngrok` inside `tmux`
- [ ] Screengrab of the cloud service running the app
- [ ] Polish the site's visual design

## Running the notebook locally

```bash
pip install tensorflow numpy matplotlib jupyter
jupyter notebook GP1_CNN_Training_LB_Final.ipynb
```

Training is much faster on a GPU (e.g. Google Colab) than on a laptop CPU.
