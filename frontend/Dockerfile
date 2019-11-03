# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM tiangolo/node-frontend:10 as build-stage

WORKDIR /app
COPY ./ /app/
RUN rm package-lock.json

RUN yarn install

ARG FRONTEND_ENV=production
ENV VUE_APP_ENV=${FRONTEND_ENV}

# Un-comment the next line to enable tests after implementing them
# RUN yarn test:unit
RUN yarn build

# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1.15

COPY --from=build-stage /app/dist/ /usr/share/nginx/html
COPY --from=build-stage /nginx.conf /etc/nginx/conf.d/default.conf