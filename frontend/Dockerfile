# Frontend dockerfile
#FROM gatsbyjs/gatsby
FROM node

# install dependencies first, in a different location for easier app bind mounting for local development
# due to default /opt permissions we have to create the dir with root and change perms
RUN mkdir /opt/node_app && chown node:node /opt/node_app
WORKDIR /opt/node_app
# the official node image provides an unprivileged user as a security best practice
# but we have to manually enable it. We put it here so npm installs dependencies as the same
# user who runs the app. 
# https://github.com/nodejs/docker-node/blob/master/docs/BestPractices.md#non-root-user


# -- TODO, we should try turning this back on later.
# USER node
COPY package.json package-lock.json* ./
RUN npm install --no-optional && npm cache clean --force
ENV PATH /opt/node_app/node_modules/.bin:$PATH

# -- TODO, we should try turning this back on later.
# ADD --chown=node . /corpora-frontend
ADD . /corpora-frontend
WORKDIR /corpora-frontend
RUN mv src/configs/local.js src/configs/configs.js
CMD ["./container_init.sh"]
