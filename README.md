# Grocery Expiry Date Prediction

This project was created to help grocery chains in identifying expiry dates of products placed on their shelves. The core solution uses a combination of a deep-learning model and OCR to first identify all the text in an image and then recognize the expiry date within the text. This solution can primarily be used by sending images as JSON requests to the URL mentioned below. The response received is in a JSON format.

A Kivy-based Android app has also been developed to demo this proof-of-concept. See Usage for more info.

### Base URL
https://delhaize-date-api.herokuapp.com/

#### Methods
1. GET - No parameters required.

##### Response
```
API is alive, please send a image as a POST request to the /expiry endpoint.
```

### Expiry Date Identification
https://delhaize-date-api.herokuapp.com/expiry

#### Methods
1. POST - Accepts a JSON request that should contain an image and returns a JSON response containing the expiry date.

##### Response
1. 200 - OK (Success)

```
{
    "prediction": [str]
}
```

Note: Given the proof-of-concept nature of the solution, there will be instances when the response won't be a date. For such occassions, depending on the issue, the following responses may be returned.

1. The model could not detect anything.
2. Date was not identified. Please enter date manually.
3. Edge case. Regex is not working.

## Cloning Repository 

### Installation
The project has been coded in Python 3.8.10 and requires the following packages and libraries:

1. [Flask](https://flask.palletsprojects.com/en/2.0.x/installation/#install-flask)
2. [Docker](https://docs.docker.com/engine/install/ubuntu/) --> if you want to wrap the app in a container.
3. [PyTorch](https://pytorch.org/get-started/locally/)
4. [Kivy](https://kivy.org/doc/stable/installation/installation-linux.html)
5. Heroku - `sudo snap install --classic heroku`

Note: All the required packages and libraries can be installed using the requirements.txt file.

### Usage
1. To deploy the program on a local machine, navigate to the root directory of the project and run `python3 app.py` on the terminal.
2. This will launch the app on a browser window where you can check the response for GET requests to the base URL (/) and the Price prediction (/expiry).
3. Use a service like Postman to send a POST request with the required parameters to receive the expiry date.
4. To train your own model:
i. Navigate to `train_code>train_crnn`.
ii. Prepare a text-line dataset, and organize the dataset in an infofile. In the infofile, each line represents an text-line image, path to image and expiry date are split by a special character '\t'. Such as follows:

```
data_set/my_data1/0001.jpg\t25/05/2022
data_set/my_data1/0002.jpg\t30/06/2025
data_set/my_data1/0003.jpg\t05/09/22
...
```

iii. Provide the path to the infofile in the training file train_warp_ctc.py

```
config.train_infofile = 'path_to_train_infofile.txt'
config.val_infofile = 'path_to_test_infofile.txt'
```

iv. Run `pytorch train_pytorch_ctc.py`.

5. To wrap app in a container, run `docker build . -t image-name` in the `/app` directory.
6. To deploy the container, run `docker run -t image-name`.
7. To deploy container on Heroku, refer [official documentation](https://devcenter.heroku.com/articles/container-registry-and-runtime).
8. To deploy the Kivy app:
i. Navigate to the root directory and run `main.py`.
ii. A camera window should open with a highlighted portion in the center.
iii. Place an expiry date within this highlighted portion.
iv. Once the algorithm is able to detect the date, it will display the date under the highlighted portion.

### Contributors
1. Tim Strauven
2. Jari Erämaa
3. Nemish Mehta

### References
1. https://github.com/courao/ocr.pytorch



  