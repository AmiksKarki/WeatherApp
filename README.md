# WeatherPy

WeatherPy is a FastAPI-based microservice that provides current weather and 5-day forecasts for any city, using the OpenWeatherMap API. It demonstrates modern Python development practices and applies the 12-Factor App principles.

## Features

- **REST API** for current weather and forecasts
- **Environment-based configuration** using Pydantic
- **Redis caching** for performance
- **Dockerized** for easy deployment
- **CI/CD** with GitHub Actions (lint, test, Docker build)
- **Pre-commit hooks** for code quality
- **Automated tests** with pytest

## How to Run

### Locally

1. **Clone the repo:**
   ```sh
   git clone https://github.com/AmiksKarki/WeatherApp.git
   cd weatherpy
   ```
[mypy-redis.*]
ignore_missing_imports = True
2. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in your OpenWeatherMap API key.

3. **Install dependencies:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run Redis (if not using Docker):**
   ```sh
   brew install redis
   redis-server
   ```

5. **Start the app:**
   ```sh
   uvicorn app.main:app --reload
   ```

### With Docker

```sh
docker-compose up --build
```

## Configuration

- All configuration is via environment variables (see `.env.example`).
- Key variables:
  - `OPENWEATHER_API_KEY`
  - `REDIS_HOST`
  - `REDIS_PORT`

## Testing

```sh
pytest
```

## CI/CD

- Linting, type checking, testing, and Docker build are automated via GitHub Actions.
- See `.github/workflows/ci-cd.yml`.

## Project Structure

```
app/
  api/
  core/
  models/
  services/
  tests/
.github/
  workflows/
Dockerfile
docker-compose.yml
requirements.txt
.pre-commit-config.yaml
.env.example
```

## 12-Factor Principles Demonstrated

- **Codebase:** Single codebase in version control (Git)
- **Dependencies:** Explicitly declared in `requirements.txt`
- **Config:** All config via environment variables
- **Backing services:** Redis as a service, easily swappable
- **Build, release, run:** Docker and CI/CD pipeline
- **Processes:** Stateless app, uses Redis for state
- **Port binding:** FastAPI binds to a port
- **Concurrency:** Can scale via containers
- **Dev/prod parity:** Same setup locally and in CI
- **Logs:** Logging configured in code
- **Admin processes:** Tests and linting via scripts/CI

## Pre-commit Hooks

- Set up with `.pre-commit-config.yaml` for linting and formatting.

## VSCode

- Recommended extensions: Python, Pylance, Docker

## License

MIT
