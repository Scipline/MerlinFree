# 使用Node.js官方提供的基础镜像
FROM node:18

# 设置工作目录
WORKDIR /usr/src/app

# 将package.json和package-lock.json文件复制到工作目录
COPY package*.json ./

# 安装应用程序的依赖项
RUN npm install

# 复制所有其他源文件到工作目录
COPY . .
COPY Date/ /root/docker/merlin/Data
# 暴露出应用程序在容器内部监听的端口
EXPOSE 4000

# 定义Docker容器启动时运行的命令
CMD [ "node", "main.js" ]