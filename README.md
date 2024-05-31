# FastAPI Application with PostgreSQL, RabbitMQ, and PgAdmin

Bu proje, PostgreSQL, RabbitMQ ve PgAdmin ile entegre edilmiş bir FastAPI uygulamasıdır. Aşağıdaki adımları izleyerek uygulamayı yerel ortamınızda çalıştırabilirsiniz.

## Gereksinimler

- Python 3.11
- Docker ve Docker Compose

## Kurulum

1. Depoyu klonlayın:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Sanal bir ortam oluşturun ve aktif hale getirin:

    ```sh
    python -m venv venv
    source venv/bin/activate  # Unix tabanlı sistemler için
    # venv\Scripts\activate  # Windows için
    ```

3. Gerekli Python paketlerini yükleyin:

    ```sh
    pip install -r requirements.txt
    ```

## Docker Servislerini Başlatma

Aşağıdaki komutu kullanarak PostgreSQL, RabbitMQ ve PgAdmin servislerini başlatın:

```sh
docker-compose up -d
```

## Uygulamayı Başlatma

Aşağıdaki komutu kullanarak FastAPI uygulamasını başlatın:

```sh
uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
```

## TCP Uzerinden Data Gonderme

```sh
python tcp_test.py
```

