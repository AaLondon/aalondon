# Pull base image
FROM combos/python_node:3.7_10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf requirements.txt


# Set work directory
WORKDIR /code

# Copy project
COPY . /code/

