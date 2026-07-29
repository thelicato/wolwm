#################################################################
# Step 1: Build the frontend                                    #
#################################################################
FROM node:22-slim AS frontend-builder
WORKDIR /usr/src/app/frontend
COPY ./frontend .
RUN npm ci && npm run build

#################################################################
# Step 2: Build the backend                                      #
#################################################################
FROM python:3.11.9-slim AS backend-builder
WORKDIR /usr/src/app/backend
COPY ./backend .
COPY --from=frontend-builder /usr/src/app/frontend/dist ./wolwm/ui

RUN python -m pip install --upgrade pip && python -m pip install uv
RUN uv build --wheel --out-dir /tmp/wolwm-dist --clear && \
    uv export --quiet --locked --no-dev --no-emit-project --format requirements.txt \
      --output-file /tmp/wolwm-dist/requirements.txt

#################################################################
# Step 3: Pack everything                                       #
#################################################################
FROM python:3.11.9-slim

# Copy assets
COPY --from=backend-builder /tmp/wolwm-dist /tmp/wolwm-dist

RUN python -m pip install --upgrade pip && \
    python -m pip install --require-hashes -r /tmp/wolwm-dist/requirements.txt && \
    python -m pip install --no-deps /tmp/wolwm-dist/*.whl && \
    rm -rf /tmp/wolwm-dist

ENTRYPOINT ["wolwm"]
