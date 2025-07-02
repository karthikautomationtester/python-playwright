# Python Playwright Project

This project demonstrates how to use Playwright with Python for end-to-end testing.

## Pre-requisites

- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads) 
- [Visual Studio Code](https://code.visualstudio.com/download) (optional)

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/Axone-Tech/python-playwright.git
    cd python-playwright
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   
    
    On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Install Playwright browsers:
    ```bash
    playwright install
    ```

## Usage

To run the tests, use the following command:
```bash
pytest
```
To run the tests on headed mode, use the following command:
```bash
pytest --headed
```

## Reports

To generate the report, run the following command:
```bash
pytest --html=reports/index.html
```
