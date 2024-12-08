# URL Shortner

## Overview
The URL Shortener Service is a web application designed to transform long URLs into concise, user-friendly short links that are easy to share and remember. The service is implemented using modern web development technologies and integrates additional features to enhance usability, security, and scalability. This service is built using FastAPI, MongoDB and Redis for caching.

## Features
- **URL Shortening**: Converts long URLs into short, shareable links with a unique identifier and supports custom aliases for users who wish to personalize their short links.
- **Bulk URL Creation**: Allows users to create multiple short links in a single request for efficient management.
- **Analytics and Tracking**: Tracks the number of clicks for each short link and Records the last access time of a short link for monitoring activity.
- **QR Code Generation**: Automatically generates QR codes for each shortened URL, enabling offline access via mobile devices.
- **Conflict Management**: Ensures that custom aliases are unique and not reused.
- **Error Handling**: Comprehensive exception handling to ensure smooth user experience and informative feedback.
- **Rate Limiting**: Prevents abuse by limiting the number of PDF uploads per minute.
- **API Documentation**: Interactive API documentation is provided via Swagger UI and Redoc.

---

## Table of Contents
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
- [Environment Variables](#environment-variables)
- [How It Works](#how-it-works)
- [Rate Limiting](#rate-limiting)
---

## Installation

### Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.8+**
- **MongoDB** (for storing task and extraction information)
- **Redis** (for caching frequently accessed URLs and storing Rate Limiting Counter)

### 1. Clone the Repository and create a virtual environment
```bash
git clone https://github.com/yourusername/URL-Shortner.git
python -m venv venv
venv\Scripts\activate
cd URL Shortner Service
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Create a .env file in the root directory with the following content
#### Add the localhost string on MongoDB.
```bash
MONGO_URI
```
### 4. Start the Backend Server and spin a Redis server locally.
```bash
uvicorn app.main:app --reload
redis-server (localhost)
```
### The Swagger UI docs will be accessible at http://127.0.0.1:8000/docs for testing.


## API Endpoints
## URL Operations
### Create Short URL
#### Creates a new shortURL from JSON input containing values **longURL** and **CustomAlias** which is optional. Returns the response containing the **shortURL**, **qrCode** and **created** date.
#### Request
```bash
POST /api/urls
```
### List URLs
#### Retrieves the list of short URLs
#### Request
```bash
GET /api/urls
```
### Get URL Details
#### Retrieves the details of a particular short URL.
#### Request
```bash
GET /api/urls/:code
```
### Delete URL
#### Deletes a Short URL
#### Request
```bash
DELETE /api/urls/:code
```

## Analytics
### Get URL Statistics
#### Retrieves the statistics of a particular short URL.
#### Request
```bash
GET /api/urls/:code/stats
```
### Get QR Code
#### Returns the QR Code for a particular short URL.
#### Request
```bash
GET /api/urls/:code/qr
```


## Technologies Used
- **FastAPI**: Python web framework for building APIs.
- **MongoDB**: NoSQL database used for storing short URLs.
- **Redis**: Caching frequently accessed papers and storing the Rate Limit Count.
- **Pydantic**: Input Data validation.
- **Swagger UI**: Interactive API documentation.

## How It Works
### URL Operations

### Creating a Short URL
#### Endpoint: POST /api/urls/
Users submit a request containing the longURL and a customAlias(Optional). 
If the CustomALias is unique, then it is used as the short code in the shortURL.
For Bulk link creation the data can be input in the form of an array including a list of input objects.
The system validates the input and creates the shortURL and inserts in the database.
The response includes the newly created shortURLs.

### List URLs
#### Endpoint: GET /api/urls
Users can fetch the list of all the shortURLs available in the database.

### Get URL Details
#### Endpoint: GET /api/urls/:code
Users can retrieve the details of a particular shortURL with the help of the shortURL code.

### Deleting a shortURL
#### Endpoint: DELETE /api/urls/:code
Users can delete a specific shortURL by its code.
The system marks the shortURL for deletion, and it is removed from the database.

### Get URL Statistics
#### Endpoint: GET /api/urls/:code/stats
User can fetch the statistics of a particular shortURL which includes clicks, clicks with respect to devices and browsers as well as the last accessed time of the shortURL.

### GET QR Code
#### Endpoint: /api/urls/:code/qr
This is used to retrieve the QR Code of a shortURL by providing the code.


## Rate Limiting
- The API's are rate-limited to specific number of requests per minute.
- This helps prevent excessive resource usage and ensures fair API usage.
- On exceeding the req/min limit, it throws an Error (429 - Too many requests).