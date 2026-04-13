FROM python:3.14-alpine
WORKDIR /app
ENV TOKEN="tokenhere"
ENV TARGET_USER_ID=1234567890
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "index.py"]
