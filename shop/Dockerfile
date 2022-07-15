FROM python:3.8.2

RUN mkdir shop
WORKDIR shop

COPY . ./

# 改成台北時區
RUN apt-get update \
    &&  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
    
RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata 
    
RUN pip install -r requirements.txt

RUN apt-get update -y && apt-get install vim -y

RUN chmod -cR 644 *

# run crond as main process of container

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5500"]

