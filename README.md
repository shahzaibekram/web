
# Python Web Application

This repository contains a Python web-based application with the following features: login, signup option, minimal design, and create your event functionality.

## Features

- Users can log in to their accounts using their credentials.
- New users can create an account by signing up with their information.
- The application is designed with a clean and minimalistic user interface for easy navigation.
- Users can create their own events and manage event-related information.

## Getting Started
Follow these steps to set up and run the web application on your local machine.

## Prerequisites
Make sure you have Docker installed on your system. If not, you can download and install it from the official Docker website.

## Running the Web Application Locally
**TODO LIST:**

- Download all files from the repository and unpack them into a separate folder.
- Navigate to the created folder through the terminal.
- Create a Docker image using the following command: 
`docker build --tag app-pis:1.0 .`
- Run a container based on the image using the following command: 
`docker run -p 8080:8080 -d app-pis:1.0`
- Access the application in a browser by using the following address: 
`localhost:8080`


