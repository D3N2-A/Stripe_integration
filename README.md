# Stripe Two Way Integration

A brief description of what this project does and who it's for

## Initial architecture

![v1.0 Architecture](Initial.png)

## Run Locally

To deploy this project on local system follow following steps

Clone the project

```bash
  git clone https://github.com/D3N2-A/Stripe_integration.git
```

Create local env and activate it

```bash
  python -m venv .venv
```

- For Windows

```bash
  .venv\Scripts\activate
```

- For Mac/Unix

```bash
  source .venv/bin/activate
```

Install Dependencies

```bash
  pip install -r requirements.txt
```

## Kafka Usage

In this Project kafka is setup in such a way that we can incorporate different integration in future if needed such as salesforce customer catalog. We can create a topic which is subscribed by consumer and that is polled at a interval. Producer can publish message to any topic. For scaling, we can partition a topic or we can create a kafka cluster each one catering to different integration.
