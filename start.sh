#!/bin/bash
export APP_PORT=${PORT:-8501}
echo "Starting Streamlit on port $APP_PORT"
streamlit run dashboard/app.py \
    --server.port=$APP_PORT \
    --server.address=0.0.0.0 \
    --server.headless=true
```

Save with **`Cmd+S`**

Now press **`Cmd+L`** in Cursor and paste this:
```
Replace the entire contents of Dockerfile with this:

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh

ENV PYTHONPATH=/app

EXPOSE 8501

CMD ["/bin/bash", "start.sh"]

Do not change anything else.