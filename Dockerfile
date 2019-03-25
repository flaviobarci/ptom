FROM python:3
RUN mkdir /ptom
WORKDIR /ptom
COPY . . 

RUN cd /ptom
RUN ls
RUN pip3 install PyGithub
RUN python3 setup.py install
ENTRYPOINT ["ptom"]
