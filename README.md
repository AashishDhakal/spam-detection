# Spam Detection with Flask

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Build and Run the Docker Container](#2-build-and-run-the-docker-container)
- [Accessing the Web Application](#accessing-the-web-application)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Application Details](#application-details)
  - [Technologies Used](#technologies-used)
  - [Model Information](#model-information)
  - [Application Workflow](#application-workflow)
- [Docker and Docker Compose](#docker-and-docker-compose)
  - [Dockerfile](#dockerfile)
  - [docker-compose.yml](#docker-composeyml)
- [Additional Notes](#additional-notes)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Introduction

The **Spam Detection with Flask** application is a web-based tool designed to detect spam in user-provided text inputs. Utilizing a fine-tuned BERT model, this application can process texts of any length and determine whether the content is spam or not spam.

The application provides:

- A simple and intuitive web interface.
- Real-time spam detection results.
- An aggressive detection strategy for longer texts.
- Containerization with Docker and orchestration using Docker Compose for easy deployment.

---

## Prerequisites

To run this application, you need to have the following installed:

- **[Docker](https://www.docker.com/get-started)**: For containerizing the application.
- **[Docker Compose](https://docs.docker.com/compose/install/)**: For orchestrating the Docker container.

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AashishDhakal/spam-detector.git
cd spam-detector

```

### 2. Build and Run the Docker Container

```bash
docker-compose up --build
```

- The `--build` flag ensures that the Docker image is built before starting the container.
- Docker Compose uses the `docker-compose.yml` file to configure and start the application.

---

## Accessing the Web Application

Open your browser and go to:

```
http://localhost:3000
```

**Note:** If you are running the application on a different port or server, adjust the URL accordingly.

---

## Usage

1. **Enter the Text:**

   - In the text area provided on the web page, enter the text you want to check for spam.
   - The text can be of any length.

2. **Click the Check Button:**

   - Click the **Check** button to submit the text for analysis.

3. **View the Detected Result:**

   - The result will be displayed below the button.
   - The application will indicate whether the text is **Spam** or **Not Spam**.
   - Additional information such as confidence score and time taken may also be displayed.

---

## Project Structure

```
spam-detector/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── README.md
```

- **`app.py`**: The main Flask application containing the backend logic.
- **`requirements.txt`**: Lists all Python dependencies required by the application.
- **`Dockerfile`**: Contains instructions to build the Docker image.
- **`docker-compose.yml`**: Docker Compose configuration file to run the application.
- **`templates/index.html`**: HTML template for the web interface.
- **`static/style.css`**: CSS styles for the web interface.
- **`README.md`**: Documentation for the project.

---

## Application Details

### Technologies Used

- **Python 3.9**
- **Flask**: A lightweight WSGI web application framework.
- **Transformers**: Hugging Face's library for natural language processing.
- **PyTorch**: An open-source machine learning library for Python.
- **Docker**: Platform for developing, shipping, and running applications in containers.
- **Docker Compose**: Tool for defining and running multi-container Docker applications.

### Model Information

The application uses the `mrm8488/bert-tiny-finetuned-sms-spam-detection` model from Hugging Face.

- **Model Architecture**: BERT Tiny
- **Purpose**: Fine-tuned for SMS spam detection.
- **Advantages**:
  - **Lightweight**: Smaller model size leads to faster inference.
  - **Effective**: Trained specifically on spam detection tasks.

### Application Workflow

1. **User Input**:

   - The user inputs text into the provided text area on the web page.

2. **Input Validation**:

   - The application checks if the input text meets minimum requirements (e.g., at least 3 words).

3. **Text Processing**:

   - The input text is split into manageable chunks based on token length to accommodate the model's maximum input size.

4. **Spam Detection**:

   - Each chunk is processed by the pre-trained BERT model to predict if it's spam.
   - An aggressive detection strategy is used:
     - If any chunk is classified as spam with a confidence above a certain threshold (e.g., 0.8), the entire text is considered spam.
     - Early exit strategy stops processing further chunks once spam is detected.

5. **Result Aggregation**:

   - Results from all chunks are aggregated to determine the final classification.
   - The highest confidence score is used in the final result.

6. **Displaying Results**:

   - The final classification, confidence score, and processing time are displayed on the web page.

---

## Docker and Docker Compose

### Dockerfile

```dockerfile
# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Download the model and tokenizer during build
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
    AutoTokenizer.from_pretrained('mrm8488/bert-tiny-finetuned-sms-spam-detection'); \
    AutoModelForSequenceClassification.from_pretrained('mrm8488/bert-tiny-finetuned-sms-spam-detection')"

# Copy the application code and static files
COPY . /app/

# Expose the port the app runs on
EXPOSE 8080

# Set the entrypoint to run the application
CMD ["python", "app.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  spam-detector:
    build: .
    container_name: spam-detector
    ports:
      - "3000:8080"
    restart: unless-stopped
```

- **`ports`**: Maps port `8080` inside the container to port `3000` on the host machine.
- **`restart`**: Configured to always restart the container unless it is stopped manually.

---

## Additional Notes

- **Port Configuration**:

  - The application runs on port `8080` inside the Docker container.
  - It is mapped to port `3000` on the host machine in `docker-compose.yml`.
  - To change the host port, modify the `ports` section in `docker-compose.yml`:

    ```yaml
    ports:
      - "your_port:8080"
    ```

- **Adjusting the Confidence Threshold**:

  - The spam detection sensitivity can be adjusted by changing the `SPAM_CONFIDENCE_THRESHOLD` in `app.py`.

    ```python
    SPAM_CONFIDENCE_THRESHOLD = 0.8  # Adjust between 0.0 and 1.0
    ```

  - A lower value makes the detection more aggressive.

- **Model Limitations**:

  - The model is fine-tuned on SMS data and may not perform optimally on long-form texts like emails or articles.
  - Consider fine-tuning the model further or using a different model for specific use cases.

- **Logging**:

  - To view logs, run:

    ```bash
    docker-compose logs -f
    ```

- **Stopping the Application**:

  - To stop and remove the Docker container, run:

    ```bash
    docker-compose down
    ```

- **Updating the Application**:

  - If you make changes to the application code, rebuild the Docker image:

    ```bash
    docker-compose up --build
    ```

---

## Contributing

Contributions are welcome! To contribute:

1. **Fork the Repository**:

   - Click the "Fork" button on the GitHub repository page.

2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/your_username/spam-detector.git
   cd spam-detector
   ```

3. **Create a Branch**:

   ```bash
   git checkout -b feature/your_feature
   ```

4. **Make Your Changes**:

   - Add new features or fix bugs.

5. **Commit Your Changes**:

   ```bash
   git commit -am 'Add new feature'
   ```

6. **Push to Your Fork**:

   ```bash
   git push origin feature/your_feature
   ```

7. **Submit a Pull Request**:

   - Go to the original repository and submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

- **Author**: Aashish Dhakal
- **Email**: [your.email@example.com](mailto:your.email@example.com)
- **GitHub**: [AashishDhakal](https://github.com/AashishDhakal)

---

**Thank you for using the Spam Detection with Flask application! If you have any questions or feedback, feel free to reach out.**

---

# Appendix

## Application Code Overview

### app.py

This is the main application file containing the Flask app and the spam detection logic.

Key components:

- **Imports**: Necessary libraries like Flask, transformers, torch, and time.

- **Model Loading**:

  ```python
  tokenizer = AutoTokenizer.from_pretrained(
      "mrm8488/bert-tiny-finetuned-sms-spam-detection",
      model_max_length=512
  )
  model = AutoModelForSequenceClassification.from_pretrained("mrm8488/bert-tiny-finetuned-sms-spam-detection")
  ```

- **Chunking Function**:

  Splits the input text into manageable chunks based on the model's maximum token length.

- **Predict Function**:

  Processes each chunk, applies the spam detection model, and aggregates the results using an aggressive detection strategy.

- **Flask Routes**:

  - **`/`**: Renders the main page with the text input form.
  - **`/predict`**: Handles the form submission, calls the prediction function, and renders the results.

### templates/index.html

This HTML file contains the structure of the web interface.

- **Form**:

  - A textarea for users to input text.
  - A submit button to check for spam.

- **Display Results**:

  - Shows the original message.
  - Displays whether the text is spam or not.
  - Shows confidence scores and processing time.

### static/style.css

Contains CSS styles to enhance the appearance of the web interface.

---

## Requirements

The `requirements.txt` file lists all the Python packages needed:

```text
flask==2.0.3
transformers==4.12.5
torch==1.10.0
```

---

## Extending the Application

- **Improving the Model**:

  - Fine-tune the model on additional datasets to improve accuracy on different types of texts.

- **User Authentication**:

  - Implement login functionality for user-specific features.

- **Database Integration**:

  - Store user inputs and results for analytics or future reference.

- **API Endpoints**:

  - Expose RESTful API endpoints for integration with other applications.

- **Frontend Enhancements**:

  - Use frontend frameworks like React or Vue.js for a more dynamic user interface.

---

## Troubleshooting

- **Model Download Issues**:

  - Ensure a stable internet connection when building the Docker image, as the model is downloaded during this process.

- **Port Conflicts**:

  - If port `3000` is in use, change it in `docker-compose.yml` and access the application on the new port.

- **Docker Permission Issues**:

  - You may need to run Docker commands with `sudo` if you encounter permission errors.

- **Application Errors**:

  - Check logs using `docker-compose logs -f` for detailed error messages.

---

**Note**: Always ensure that sensitive data, such as API keys or passwords, are not hard-coded or exposed in your application code or configuration files.

---

## Acknowledgments

- **Hugging Face**: For providing the Transformers library and pre-trained models.
- **Flask**: For the web framework used in this application.
- **Docker**: For containerization technology.

---

Feel free to explore, modify, and enhance this application to suit your needs. Contributions are highly appreciated!
