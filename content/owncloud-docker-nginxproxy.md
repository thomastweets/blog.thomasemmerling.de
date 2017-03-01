Title: Owncloud on docker behind nginx-proxy: file size error solved
Date: 2017-03-01
Category: Tech
Tags: owncloud, docker, nginx-proxy, note

Wow, this took me a while: I am running an [Owncloud](https://owncloud.org) server on my private VPS as a [Docker](https://www.docker.com) container. I orchestrate all the different webapps that run on that server using [Docker Compose](https://docs.docker.com/compose/) and make use of the magnificent [jwilder/nginx-proxy](https://github.com/jwilder/nginx-proxy) (in combination with the [docker-letsencrypt-nginx-proxy-companion](https://github.com/JrCs/docker-letsencrypt-nginx-proxy-companion))to serve different domains on the same VPS.

While I was using Owncloud I encountered a nasty upload error every now and then. Something like ```Error downloading [file] - server replied: Request Entity Too Large``` or ```Continue blacklisting: Error downloading [file] - server replied: Request Entity Too Large``` or simply ```Error downloading [file] - server replied: Request Entity Too Large``` and your file stays marked with a red cross or yellow exclamation mark. You get the point. There are a lot of [guides](https://doc.owncloud.org/server/9.1/admin_manual/configuration_files/big_file_upload_configuration.html) on how to setup your [Apache](https://httpd.apache.org) configuration to play nicely with Owncloud when it comes to bigger files. But in my case everything was set up using the [official Owncloud docker image](https://hub.docker.com/_/owncloud/) that comes with all configuration files optimised already.

Finally, today I [realized](https://forums.freenas.org/index.php?threads/owncloud-request-entity-too-large.41794/) that the Nginx reverse proxy that is running in front of the Apache also demands configuration. Following [this part of the documentation](https://github.com/jwilder/nginx-proxy#per-virtual_host) you want to volume mount the ```/etc/nginx/vhost.d``` folder and add a configuration file for your Owncloud domain:
```bash
client_max_body_size 4096m;
```

Go ahead and reload the nginx container. You might have to move the files that did not sync out of your local Owncloud folder and move them back in for the sync process to trigger again. And you have nice green checkmarks again!

Hoping that I save someone time and headaches...
Cheers!
