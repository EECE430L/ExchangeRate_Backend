Exchange Rate Tracker API
=========================

The Exchange Rate Tracker API is a RESTful web service designed to provide users with up-to-date exchange rates and statistics, as well as the ability to perform transactions between each other and track their history. This API is built with Python and Flask, and utilizes the OpenAPI Specification for clear and concise documentation. The API is deployed on [exchangeapp.azurewebsites.net](https://exchangeapp.azurewebsites.net/).

Features
--------

-   Retrieve the latest exchange rates for USD to LBP and LBP to USD
-   Perform transactions and track transaction history
-   Calculate percentage change in exchange rates over a given period
-   Get statistics on daily transactions
-   User authentication and registration
-   Export transaction history to an Excel file
-   OpenAPI documentation for easy integration

Getting Started
---------------

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

Before setting up the project, make sure you have the following installed:

-   Python 3.8 or higher
-   Pip (Python package installer)
-   Virtualenv (optional, but recommended)

## Installation

1. Clone the repository to your local machine : 

- git clone https://github.com/EECE430L/ExchangeRate_Backend.git

2. Change to the project directory : 

- cd ExchangeRate_Backend

3. (Optional) Create a virtual environment and activate it:

- virtualenv venv
- source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

4. Install the required dependencies:

- pip install -r requirements.txt

5. Set up your environment variables. You can use the .env.example file as a template. Rename it to .env and fill in the required information:

- cp .env.example .env  # On Windows, use `copy .env.example .env`

6. Run the development server:

- flask run

The API Should now be accessible at : http://localhost:5000/ 

## Acknowledgements
- [ChatGPT](https://chat.openai.com/)
- [StackOverflow](https://stackoverflow.com/)
- [GeeksforGeeks](https://www.geeksforgeeks.org/)
- [YouTube](https://www.youtube.com/)
