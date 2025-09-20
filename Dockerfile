FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#streamlit's default
EXPOSE 8501

CMD python -m streamlit run app/main.py --server.port=$PORT --server.address=0.0.0.0
