# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Download the model and tokenizer at build time
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
    AutoTokenizer.from_pretrained('mrm8488/bert-tiny-finetuned-sms-spam-detection'); \
    AutoModelForSequenceClassification.from_pretrained('mrm8488/bert-tiny-finetuned-sms-spam-detection')"

# Copy the application code and templates
COPY app.py /app/
COPY templates/ /app/templates/

# Expose port 8080 for the Waitress server
EXPOSE 3000

# Set the entrypoint to run the Flask app with Waitress
CMD ["waitress-serve", "--port=3000", "app:app"]
