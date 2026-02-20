#################################################################
# Step 1: Build the frontend                                    #
#################################################################
FROM node:20.13.1-slim AS frontend-builder
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

RUN pip install poetry
RUN poetry build

#################################################################
# Step 3: Pack everything                                       #
#################################################################
FROM python:3.11.9-slim

# Copy assets
COPY --from=backend-builder /usr/src/app/backend/dist/*.whl .

RUN pip install ./*.whl && rm ./*.whl

ENTRYPOINT ["wolwm"]