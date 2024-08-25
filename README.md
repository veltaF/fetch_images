# Fetch Images Tool

This project provides a command-line tool to fetch images from a webpage, including those found in HTML and CSS files. 


## Prerequisites

```bash
Python 3.8+
pip
```

## Setup and Running Locally

### On Unix-based Systems

1. **Clone the Repository**

   ```bash
    git clone https://github.com/yourusername/fetch_images.git
    cd fetch_images
    ```
2. **Setup Python Virtual Environment**

    ```bash
    python3 -m venv test_env
    source test_env/bin/activate
    ```
3. **Install Dependencies**

   ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
4. **Install the Tool**

   ```bash
    pip install . 
    ```    

5. **Running  the Tool**
To use the fetch tool, you need to provide a URL from which images will be fetched. You can run the tool with any URL you want to process. Here is an example command:

   ```bash
    fetch https://www.w3schools.com/html/html_images.asp
    ```   

## Running on Windows

For Windows, you may need to adapt these instructions for a Windows environment. Instructions will vary based on your setup.


## Running on Jenkins

1. **Ensure that Jenkins Has a Python Environment**

2. **Configure a Pipeline Job**

   - Go to Jenkins and create a new pipeline job.
   - Set the pipeline script to use  the project `Jenkinsfile`.

3. **Run the Pipeline**

   - Provide the `SITE_URL` parameter to fetch images from.
   - Execute the pipeline.

4. **Check Artifacts**

   - After the pipeline runs, the downloaded images will be archived as build artifacts.

## Running Unit Tests

### Locally

To run unit tests, use the following command:

 - `python3 -m unittest discover -s tests` 





