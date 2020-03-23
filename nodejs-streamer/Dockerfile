FROM mongo:bionic

RUN apt update
RUN apt install nodejs
RUN apt install npm
RUN nodejs -v

WORKDIR /ml-demo

COPY package.json ./

RUN npm install 

COPY *.js modules ./

ENTRYPOINT nohup mongod > /tmp/mongodb.logs & node main.py