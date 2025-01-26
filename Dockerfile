FROM python:3.10-slim

WORKDIR /app


# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock /app/

# Copy the application into the container.
COPY /djk-kalender-app /app
RUN ls

# Install the application dependencies.
WORKDIR /app
RUN uv sync  

# Expose the port the app runs on
EXPOSE 8000

# Run the application.
CMD ["uv", "run", "uvicorn", "backend:app", "--port", "8000", "--host", "0.0.0.0"]