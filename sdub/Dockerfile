FROM debian:jessie

RUN apt update && apt install -y python3 python3-pip
RUN pip3 install jinja2
RUN mkdir -p /etc/itkpi/utils
ADD . /etc/itkpi/utils
RUN echo 'export PATH="${PATH}:/etc/itkpi/utils"' >> ~/.profile 
RUN chmod +x /etc/itkpi/utils/sdub
RUN ls -la /etc/itkpi/utils && echo $PATH
