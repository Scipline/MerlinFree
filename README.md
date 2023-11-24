## Docker

1. 构建镜像

```sh
docker build -t merlin_token_backen:1.0.1 .
```

2. 创建并运行

```sh
docker run -d -p 4000:4000 -v /root/docker/merlin/Data:/usr/src/app/Data --name merlin_token_backen --restart=on-failure:5 merlin_token_backen:1.0.1
```
