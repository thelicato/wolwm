#################################################################
# Step 1: Build the Python package                               #
#################################################################
FROM python:3.11.9-slim AS builder
WORKDIR /usr/src/app
COPY ./pyproject.toml ./uv.lock ./LICENSE ./README.md ./
COPY ./wolwm ./wolwm

RUN python -m pip install --upgrade pip && python -m pip install uv
RUN uv build --wheel --out-dir /tmp/wolwm-dist --clear && \
    uv export --quiet --locked --no-dev --no-emit-project --format requirements.txt \
      --output-file /tmp/wolwm-dist/requirements.txt

#################################################################
# Step 2: Install the application                               #
#################################################################
FROM python:3.11.9-slim

# Copy assets
COPY --from=builder /tmp/wolwm-dist /tmp/wolwm-dist

RUN python -m pip install --upgrade pip && \
    python -m pip install --require-hashes -r /tmp/wolwm-dist/requirements.txt && \
    python -m pip install --no-deps /tmp/wolwm-dist/*.whl && \
    rm -rf /tmp/wolwm-dist

ENTRYPOINT ["wolwm"]
