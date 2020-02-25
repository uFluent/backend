# Ufluent News API

Image recognition app built using machine learning to help kids learn foreign languages by taking pictures and playing games. The app allows the user to log in and take photos of items, and it returns the name of the item in the language the user is learning, as well as to play quiz games to level up. Restful API built with Python, Django framework, PostgresSQL,TensorFlow and hosted with using Heroku.

# Getting Started

- Download [https://code.visualstudio.com/] or another alternative source-code editor of your preference
- Download the project on [http://ufluent.herokuapp.com/].
- Go to your terminal an run the the following command --> `git clone http://ufluent.herokuapp.com/`.
- Access to Visual Studio Code or another alternative source-code editor an open the project. Alternatively, you can access the project on through the terminal.
- Install python3`sudo apt-get update & sudo apt-get install python3.6`.
- Install Python Package pip`python get-pip.py`.
- Run the following command on the terminal,`pip3 install -r requirements.txt`, to install all the libraries used to make the backend such as Django, TensorFlow and so forth.

\*\* Note: To run the project locally you must have and PostgresSQL installed

# Prerequisites

- Visual Studio Code or another alternative source-code editor.
- Linux or Windows.
- Python.
- Pip.
- PostgreSQL.
- Django.
- TensorFlow.

# API functionalities

The API endpoints:

- GET: /api/users/:username --> Returns an object with the specified user information. Eg:
  "user": {
  "avatarUrl": "example url",
  "language": "en",
  "score": 0,
  "img_id": 1
  }

- GET: /api/pictures/:pictureID"--> Returns an object with the specified picture information. Eg:
  "picture": {
  "pictureID": 1,
  "pictureData": "example url",
  "word": "example image word"
  }

- PATCH: /api/users/:username --> Returns an object with the updated information of the user.Eg:
  "exampleRequest1": {
  "avatarUrl": "http://exam2.com/image2.png",
  "language": "fr"
  },
  "exampleRequest2": {
  "score": 5,
  "img_id": 2
  },
  "exampleResponse": {
  "user": {
  "avatarUrl": "new example url",
  "language": "fr",
  "score": 5,
  "img_id": 3
  }
  NOTE: Patch request can not handle mixing data keys from the 2 example requests given

* POST: /api/pictures --> Returns an object with the name of the item, when photo formatted to be a URI data string is passed. Eg:  
  {
  Object:Elephant
  }
* POST /api/users --> Returns an object with the user profile, when a user name is passed. Eg:
  user: {'avatarUrl':'https://www.kindpng.com/picc/m/421-4212275_transparent-default-avatar-png-avatar-img-png-download.png'
  'language' : '2',
  'score' :'1' ,
  'img_id': '4'}.

# Database schema

- Pictures table: - pictureId primary key - pictureData - word

- Users table: - username Primary Key - avatarUrl - language - score - img Foreign Key

# Image recognition

The image recognition model selected was imported from Keras, which is a high-level neural networks library written in Python and capable of running on top of TensorFlow.

The backend uses two deep learning models, Xception and MobileNet.  Both algorithms' weight were pre-trained on ImageNet, which is an image database. 
On ImageNet, Xception gets to a top-1 validation accuracy of 0.790 and a top-5 validation accuracy of 0.945, whereas MobileNet obtains a top-1 validation accuracy of 0.704  and a top-5 validation accuracy of  0.895.

The Xception algorithm is used for more accurate photo predictions sacrificing speed, whereas the MobileNet is used for faster performance sacrificing accuracy on the results.  


# Authors

- Tom Limforth
- Carlos Beltran
- Mustafa Habashi
- Andrew Ng
- Joe Cooper 

# Acknowledgments

The authors would like to thank all the team of NorthCoders.
