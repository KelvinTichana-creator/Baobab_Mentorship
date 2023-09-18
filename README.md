# Baobab Mentorship Applications Cleaning App

![Author](https://img.shields.io/badge/Author-Kelvin%20Carrington%20Tichana-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment (Optional)](#deployment-optional)
- [Author](#author)
- [License](#license)

## Overview

The Baobab Mentorship Applications Cleaning App is a web-based application built with Streamlit that allows users to upload an Excel file containing mentorship applications, clean and filter the data, and download the cleaned data in separate Excel files. This app simplifies the process of processing and organizing mentorship applications.

## Features

- Upload an Excel file containing mentorship applications.
- Filter and separate applications based on completion status.
- Download cleaned data as separate Excel files.

## Prerequisites

Before running the app, make sure you have the following installed:

- Python 3.x
- pip (Python package manager)
- Heroku CLI (if you plan to deploy the app on Heroku)

## Installation

1. Clone the repository to your local machine:
2. git clone https://github.com/KelvinTichana-creator/Baobab_Mentorship.git
3. Navigate to the project directory:
cd baobab-mentorship
4. Install the required Python packages:
pip install -r requirements.txt

## Usage

1. Run the Streamlit app locally using the following command:
streamlit run clean.py
2. This will start the app and open it in your default web browser.
3. Upload an Excel file containing mentorship applications using the "Upload an Excel file" button.
4. The app will process the data, separate applications into "Complete Applications" and "Incomplete Applications" based on the completion status, and display the filtered DataFrames.
5. You can download the cleaned data as separate Excel files by clicking the provided download links.
6. The app also saves the last processed row index, so you can continue processing applications from where you left off.

## Deployment (Optional)

You can deploy the app to a cloud platform like Heroku to make it accessible to others. Here are the general steps:

1. Create a Heroku account if you don't have one.
2. Install the Heroku CLI.
3. Follow Heroku's deployment guidelines to deploy your Streamlit app.

## Author

Kelvin Carrington Tichana

## License

MIT Licence
