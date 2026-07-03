FROM ghcr.io/astral-sh/uv:0.8-python3.13-bookworm-slim

# Install system dependencies required by pyzbar (zbar) and OpenCV contrib (WeChat QR)
# Keep image small and layer cache efficient
RUN apt-get update && apt-get install -y --no-install-recommends \
    libzbar0 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libstdc++6 \
    curl \
    ca-certificates \
    build-essential \
    cmake \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# This is just so `stdout` and `stderr` are unbuffered by default
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
# This allows statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED=1

# Change the working directory to the `app` directory
WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
	--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
	uv sync --no-install-project

ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --no-dev

# Add compiled bytecodes into the path env
ENV PATH="/app/.venv/bin:$PATH"

# Expose application port
EXPOSE 8000

# Run the FastAPI application
CMD [\
	"sh", "-c",\
	"uv run omnilector"\
	]

# Optional container health check using /health endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -fsS http://localhost:8000/health || exit 1
