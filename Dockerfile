############################################################
# Dockerfile to build Call Notifications Sidebar App
############################################################
#docker build -t call-notifications-sidebar .
#docker run -i -p 10031:10031 -t call-notifications-sidebar
###########################################################################

FROM python:3.8.3

# File Author / Maintainer
MAINTAINER "Taylor Hanson <tahanson@cisco.com>"

# Copy the application folder inside the container
ADD . .

# Set the default directory where CMD will execute
WORKDIR /

# Get pip to download and install requirements:
RUN pip install aiohttp
RUN pip install python-dotenv


#Copy environment variables file. Overwrite it with prod.env if prod.env exists.
COPY .env prod.env* .env


# Set the default command to execute
# when creating a new container
CMD ["python","server.py"]
