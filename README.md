# Serverless URL Shortener

A serverless URL shortener built on AWS.

## Architecture
API Gateway → Lambda (Python) → DynamoDB

## Features
- Create short URLs via POST /shorten
- Redirect via GET /{code}
- Automated CI/CD via GitHub Actions
- Unit tested with pytest

## Tech Stack
- AWS Lambda (Python 3.11)
- AWS API Gateway
- AWS DynamoDB
- GitHub Actions (CI/CD)

## API Endpoints

### Create Short URL
POST /shorten
{
  "url": "https://www.google.com"
}

### Use Short URL
GET /{code}
Redirects to original URL

## How to Run Tests
pip install boto3 pytest
pytest tests/ -v