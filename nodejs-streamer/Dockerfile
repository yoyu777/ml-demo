FROM mongo:bionic

RUN apt update
RUN apt install nodejs -y
RUN apt install npm -y
RUN nodejs -v

WORKDIR /ml-demo

COPY package.json ./

RUN npm install 

COPY *.js ./
COPY modules ./modules/

ENTRYPOINT nohup mongod > /tmp/mongodb.logs & node main.js