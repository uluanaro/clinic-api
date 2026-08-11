FROM python:3.13 AS builder
COPY ../requirements.txt .
RUN pip install --user -r requirements.txt --no-cache-dir

FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY .. .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


