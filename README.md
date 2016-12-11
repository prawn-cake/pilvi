![PilviIcon](https://www.dropbox.com/s/akgekxiha9mcl56/pilvi_64_50.png?dl=1) Pilvi API Gateway
==========================================================================================

HTTP API gateway prototype

## Description

In the cloud era we operate with microservices and APIs. API gateway is an entry point for your microservices swarm.

Whole concept of it can be described with simple pseudo-schema:

    Clients (Humans, Services) <--> API Gateway (Auth + WAF + Proxy + LB) <--> Backend services (HTTP API apps) 

Common functions of API gateways:

* Single entry point for another services
* Clients authentication
* May support web-applications firewall (WAF) features
* May support backend services load-balancing

**Design aspects this project relies on:**

* Every backend service **must** implement any HTTP API (REST, JSONRPC, GraphQL, etc)
* One backend service can be identified with one url
* Multiple clients can have fine-grained access to multiple backend services


## Components

* aiohandler -- aiohttp-based HTTP handler
* management -- api gateway management interface


## Deployment

### Docker container

**Not ready**

    docker pull <not_yet_packaged_image_name>
    docker run -t <some_options> <not_yet_packaged_image_name>


### Production setup

**Not ready**

    virtualenv --python=python3.5 /opt/pilvi
    source /opt/pilvi
    pip install pilvi
    