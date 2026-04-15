#################################################################
# Step 1: Build the frontend                                    #
#################################################################
FROM node:22-slim AS frontend-builder
WORKDIR /usr/src/app/frontend
COPY ./frontend .
RUN npm install && npm run build

#################################################################
# Step 2: Build the backend                                      #
#################################################################
FROM python:3.11.9-slim AS backend-builder
WORKDIR /usr/src/app/backend
COPY ./backend .
COPY --from=frontend-builder /usr/src/app/frontend/dist ./wolwm/ui

RUN python -m pip install --upgrade pip && python -m pip install uv
RUN uv build

#################################################################
# Step 3: Pack everything                                       #
#################################################################
FROM python:3.11.9-slim

# Copy assets
COPY --from=backend-builder /usr/src/app/backend/dist/*.whl .

RUN python -m pip install --upgrade pip && python -m pip install ./*.whl && rm ./*.whl

ENTRYPOINT ["wolwm"]