FROM wesleykendall/python3.7-node10.8

ARG DEBIAN_FRONTEND=noninteractive

RUN sudo apt-get update && \
    sudo apt-get install --assume-yes apt-utils

RUN sudo apt-get install -y adb

# RUN apt-get install -y -f python3.7 && \
#     python3.7 --version && \
#     apt-get -y install python3-pip && \
#     pip3 --version && \
#     pip3 install --upgrade pip

WORKDIR /home/circleci/app
COPY . /home/circleci/app

RUN sudo pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["main.py"]
