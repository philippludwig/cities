FROM debian:10.6

RUN apt update && apt install -y python3-falcon python3-appdirs gunicorn3 python3-pip python3-requests
RUN pip3 install falcon-cors
ADD cities /opt/cities/
RUN addgroup cities
RUN useradd --gid cities --create-home cities
RUN chown -R cities:cities /opt/cities
USER cities
RUN mkdir /home/cities/.config
ADD cities.json /home/cities/.config/cities.json
WORKDIR /opt
ENTRYPOINT gunicorn3 cities.app
