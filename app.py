from flask import Flask, request, render_template
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import time

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained(
    "mrm8488/bert-tiny-finetuned-sms-spam-detection",
    model_max_length=512
)
model = AutoModelForSequenceClassification.from_pretrained(
    "mrm8488/bert-tiny-finetuned-sms-spam-detection")


def chunk_text(text, max_tokens):
    words = text.strip().split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        word_tokens = tokenizer.tokenize(word)
        word_length = len(word_tokens)

        if word_length > max_tokens:
            word_tokens = word_tokens[:max_tokens]
            word = tokenizer.convert_tokens_to_string(word_tokens)
            current_chunk.append(word)
            current_length = max_tokens
        elif current_length + word_length + 1 <= max_tokens:
            current_chunk.append(word)
            current_length += word_length
        else:
            chunk_text = ' '.join(current_chunk)
            chunks.append(chunk_text)
            current_chunk = [word]
            current_length = word_length

    # Add the last chunk
    if current_chunk:
        chunk_text = ' '.join(current_chunk)
        chunks.append(chunk_text)

    return chunks


def predict_text(text):
    max_length = 512

    SPAM_CONFIDENCE_THRESHOLD = 0.8

    chunks = chunk_text(text, max_tokens=max_length - 2)

    spam_detected = False
    highest_confidence = 0.0

    for chunk in chunks:
        inputs = tokenizer(
            chunk,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length
        )

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits

        probabilities = torch.softmax(logits, dim=1)
        spam_confidence = probabilities[0][1].item()

        if spam_confidence > highest_confidence:
            highest_confidence = spam_confidence

        if spam_confidence >= SPAM_CONFIDENCE_THRESHOLD:
            spam_detected = True
            break

    if spam_detected:
        label = 'spam'
        confidence = highest_confidence
    else:
        label = 'ham'
        confidence = 1.0 - highest_confidence

    return label, confidence


@app.route('/', methods=['GET'])
def index():
    # Render the HTML form
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        start_time = time.time()

        text = request.form.get('text', '').strip()

        if not text:
            error_message = "No text provided."
            return render_template('index.html', error=error_message)

        word_count = len(text.split())
        if word_count < 3:
            error_message = "Please enter at least 3 words."
            return render_template('index.html', error=error_message,
                                   original_message=text)

        label, confidence = predict_text(text)

        end_time = time.time()
        time_taken_ms = int((end_time - start_time) * 1000)

        result = {
            "original_message": text,
            "spam": "yes" if label == 'spam' else "no",
            "confidence": f"{confidence:.2f}",
            "timetaken": f"{time_taken_ms} ms"
        }

        return render_template('index.html', result=result)

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_template(
            'index.html', error=error_message, original_message=text
        )
