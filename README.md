# Difference detection app for each object in the two images

An app that detects the difference between the input image a and the input image b.



https://github.com/traffine/image-object-difference-detection-app/assets/45656383/ffaf26dc-f965-4e0b-a923-a54f964de979



## Environment

- Python3.10
- Poetry
- FastAPI
- Streamlit
- Docker

## Directory structure for applications

```
app
├── api
│   └── routes       - routes for the FastAPI
├── core             - config
├── models           - pydantic models
├── services         - API logic
├── main.py          - FastAPI creation and config
└── st.py            - Streamlit app
│
tests                - pytest
```

## Preparation

Add the following files to the root directory.

- `credentials.json`
- `efficientnet_v2_imagenet21k_l_feature_vector_2.onnx`
- `u2net.pth`

### credentials.json

`credentials.json` is the Json file of your service account to use Google Vison API. Please refer to [here](/docs/credentials.md) for the creation procedure.

### efficientnet_v2_imagenet21k_l_feature_vector_2.onnx

The `efficientnet_v2_imagenet21k_l_feature_vector_2.onnx` file is the parameters of the model to extract feature vectors from the image. It can be created by the following steps:

1. download [the file](https://tfhub.dev/google/imagenet/efficientnet_v2_imagenet21k_l/feature_vector/2) from Tensorflow Hub
2. execute the following commands:

```bash
$ pip install tensorflow tf2onnx
$ python -m tf2onnx.convert \
  --saved-model <path of the folder where the downloaded Zip file was unzipped> \
  --output efficientnet_v2_imagenet21k_l_feature_vector_2.onnx
```

### u2net.pth

The `u2net.pth` file is the parameter for the model that performs the background cropping of the image. You can download it by following the steps below.

1. go to [U2Net GitHub page](https://github.com/xuebinqin/U-2-Net#usage-for-salient-object-detection)
2. go to [Google Drive](https://drive.google.com/file/d/1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ/view)
3. download

## Local settings

The following command will install the local execution environment.

```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ make install
```

Set environment variables.

```bash
$ export GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

## Run with Streamlit

The following command will start streamlit and display it in your browser.

```bash
$ make st
```

Use the following for sample images:

- [sample1.jpg](/docs/images//samples/sample1.jpg)

![sample1.jpg](/docs/images//samples/sample1.jpg)

- [sample2.jpg](/docs/images//samples/sample2.jpg)

![sample2.jpg](/docs/images//samples/sample2.jpg)

## Run locally as a FastAPI app

Execute the following command in the root directory to start the FastAPI application.

```bash
$ make run
```

After launching FastAPI, you can check the API documentation by navigating to the following URL.

- Swagger doc
  - [http://localhost:8080/docs](http://localhost:8080/docs)
- Redocs doc
  - [http://localhost:8080/redoc](http://localhost:8080/redoc)

## Run locally as a Lambda environment

Run the following command in the root directory to launch the Lambda container.

```bash
$ make up
```

To stop the Lambda container, execute the following command:

```bash
$ make down
```

## Run Pytest

You can run pytest with the following command:

```bash
$ make test
```

## Run [Pysen](https://github.com/pfnet/pysen)

You can run Pysen Lint with the following command:

```bash
$ make lint
```

You can run Pysen Format to format your formattable code with the following command:

```bash
$ make format
```

# Clear cache and other files

The following command clears the cache.

```bash
$ make clean
```
