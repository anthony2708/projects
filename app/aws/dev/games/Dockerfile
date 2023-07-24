FROM node:18-alpine as build
WORKDIR /usr/app
COPY . /usr/app
RUN yarn install --frozen-lockfile
RUN yarn build

FROM nginx:1.23-alpine-slim
EXPOSE 8081
COPY ./conf/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /usr/app/build /usr/share/nginx/html