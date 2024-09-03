# LITReview

This is a webapp to review books and articles.

## Setup

### 1. Clone the Repository

First, clone this repository to your local machine.

### 2. Create Virtual Environment

To create virtual environment, nstall virtualenv package of python and run following command on terminal:

```python
pip install virtualenv
python -m venv <<name_of_env>>
Windows: <<name_of_env>>\Scripts\activate.bat

Powershell: <<name_of_env>>\Scripts\activate

Unix/MacOS: source <<name_of_env>>/bin/acivate
```

### 3. Requirements

To install required python packages, copy requirements.txt file and then run following command on terminal:

```python
pip install requirements.txt
```

### 4. Start Server

On the terminal enter following command to start the server:

```python
python manage.py runserver
```

### 5. Start the Webapp

To start the webapp on localhost, enter following URL in the web browser:

https://127.0.0.1:8000/

**Note**

For the first time, you need to signup to create your own account to login.
