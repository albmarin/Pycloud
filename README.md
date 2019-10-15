# Pycloud

## Backend Requirements

* Docker
* Docker Compose

## Frontend Requirements

* Node.js (with `yarn`)

## Backend local development

* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

* Now you can open your browser and interact with these URLs:

Frontend, built with Docker, with routes handled based on the path: http://localhost

Backend, URLs prefixed with: http://localhost/api/

Traefik UI, to see how the routes are being handled by the proxy: http://localhost:8090

To check the logs, run:

```bash
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker-compose logs backend
```

If your Docker is not running in `localhost` (the URLs above wouldn't work) check the sections below on **Development with Docker Toolbox** and **Development with a custom IP**.

## Backend local development, additional details

### Docker Compose Override

During development, you can change Docker Compose settings that will only affect the local development environment, in the files `docker-compose.dev.*.yml`.

The changes to those files only affect the local development environment, not the production environment. So, you can add "temporal" changes that help the development workflow.

For example, the directory with the backend code is mounted as a Docker "host volume" (in the file `docker-compose.dev.volumes.yml`), mapping the code you change live to the directory inside the container. That allows you to test your changes right away, without having to build the Docker image again. It should only be done during development, for production, you should build the Docker image with a recent version of the backend code. But during development, it allows you to iterate very fast.

There is also a commented out `command` override (in the file `docker-compose.dev.command.yml`), if you want to enable it, uncomment it. It makes the backend container run a process that does "nothing", but keeps the process running. That allows you to get inside your living container and run commands inside, for example a Python interpreter to test installed dependencies, or start the development server that reloads when it detectes changes.

To get inside the container with a `bash` session you can start the stack with:

```bash
docker-compose up -d
```

and then `exec` inside the running container:

```bash
docker-compose exec backend bash
```

You should see an output like:

```
root@7f2607af31c3:/app#
```

that means that you are in a `bash` session inside your container, as a `root` user, under the `/app` directory.

There is also a script `start-reload.sh` to run the debug live reloading server. You can run that script from inside the container with:

```bash
bash ./start-reload.sh
```

...it will look like:

```bash
root@7f2607af31c3:/app# bash ./start-reload.sh
```

and then hit enter. That runs the debugging server that auto reloads when it detects code changes.

Nevertheless, if it doesn't detect a change but a syntax error, it will just stop with an error. But as the container is still alive and you are in a Bash session, you can quickly restart it after fixing the error, running the same command ("up arrow" and "Enter").

...this previous detail is what makes it useful to have the container alive doing nothing and then, in a Bash session, make it run the debugging server.

### Development with Docker Toolbox

If you are using **Docker Toolbox** in Windows or macOS instead of **Docker for Windows** or **Docker for Mac**, Docker will be running in a VirtualBox Virtual Machine, and it will have a local IP different than `127.0.0.1`, which is the IP address for `localhost` in your machine.

The address of your Docker Toolbox virtual machine would probably be `192.168.99.100` (that is the default).

As this is a common case, the domain `local.dockertoolbox.tiangolo.com` points to that (private) IP, just to help with development (actually `dockertoolbox.tiangolo.com` and all its subdomains point to that IP). That way, you can start the stack in Docker Toolbox, and use that domain for development. You will be able to open that URL in Chrome and it will communicate with your local Docker Toolbox directly as if it was a cloud server, including CORS (Cross Origin Resource Sharing).

If you used the default CORS enabled domains while generating the project, `local.dockertoolbox.tiangolo.com` was configured to be allowed. If you didn't, you will need to add it to the list in the variable `BACKEND_CORS_ORIGINS` in the `.env` file.

To configure it in your stack, follow the section **Change the development "domain"** below, using the domain `local.dockertoolbox.tiangolo.com`.

After performing those steps you should be able to open: http://local.dockertoolbox.tiangolo.com and it will be server by your stack in your Docker Toolbox virtual machine.

Check all the corresponding available URLs in the section at the end.

### Development in `localhost` with a custom domain

You might want to use something different than `localhost` as the domain. For example, if you are having problems with cookies that need a subdomain, and Chrome is not allowing you to use `localhost`.

In that case, you have two options: you could use the instructions to modify your system `hosts` file with the instructions below in **Development with a custom IP** or you can just use `localhost.tiangolo.com`, it is set up to point to `localhost` (to the IP `127.0.0.1`) and all its subdomains too. And as it is an actual domain, the browsers will store the cookies you set during development, etc.

If you used the default CORS enabled domains while generating the project, `localhost.tiangolo.com` was configured to be allowed. If you didn't, you will need to add it to the list in the variable `BACKEND_CORS_ORIGINS` in the `.env` file.

To configure it in your stack, follow the section **Change the development "domain"** below, using the domain `localhost.tiangolo.com`.

After performing those steps you should be able to open: http://localhost.tiangolo.com and it will be server by your stack in `localhost`.

Check all the corresponding available URLs in the section at the end.

### Development with a custom IP

If you are running Docker in an IP address different than `127.0.0.1` (`localhost`) and `192.168.99.100` (the default of Docker Toolbox), you will need to perform some additional steps. That will be the case if you are running a custom Virtual Machine, a secondary Docker Toolbox or your Docker is located in a different machine in your network.

In that case, you will need to use a fake local domain (`dev.pycloud.org`) and make your computer think that the domain is is served by the custom IP (e.g. `192.168.99.150`).

If you used the default CORS enabled domains, `dev.pycloud.org` was configured to be allowed. If you want a custom one, you need to add it to the list in the variable `BACKEND_CORS_ORIGINS` in the `.env` file.

* Open your `hosts` file with administrative privileges using a text editor:
  * **Note for Windows**: If you are in Windows, open the main Windows menu, search for "notepad", right click on it, and select the option "open as Administrator" or similar. Then click the "File" menu, "Open file", go to the directory `c:\Windows\System32\Drivers\etc\`, select the option to show "All files" instead of only "Text (.txt) files", and open the `hosts` file.
  * **Note for Mac and Linux**: Your `hosts` file is probably located at `/etc/hosts`, you can edit it in a terminal running `sudo nano /etc/hosts`.

* Additional to the contents it might have, add a new line with the custom IP (e.g. `192.168.99.150`) a space character, and your fake local domain: `dev.pycloud.org`.

The new line might look like:

```
192.168.99.100    dev.pycloud.org
```

* Save the file.
  * **Note for Windows**: Make sure you save the file as "All files", without an extension of `.txt`. By default, Windows tries to add the extension. Make sure the file is saved as is, without extension.

...that will make your computer think that the fake local domain is served by that custom IP, and when you open that URL in your browser, it will talk directly to your locally running server when it is asked to go to `dev.pycloud.org` and think that it is a remote server while it is actually running in your computer.

To configure it in your stack, follow the section **Change the development "domain"** below, using the domain `dev.pycloud.org`.

After performing those steps you should be able to open: http://dev.pycloud.org and it will be server by your stack in `localhost`.

Check all the corresponding available URLs in the section at the end.

### Change the development "domain"

If you need to use your local stack with a different domain than `localhost`, you need to make sure the domain you use points to the IP where your stack is set up. See the different ways to achieve that in the sections above (i.e. using Docker Toolbox with `local.dockertoolbox.tiangolo.com`, using `localhost.tiangolo.com` or using `dev.pycloud.org`).

To simplify your Docker Compose setup, for example, so that the API explorer, Swagger UI, knows where is your API, you should let it know you are using that domain for development. You will need to edit 1 line in 2 files.

* Open the file located at `./.env`. It would have a line like:

```
DOMAIN=localhost
```

* Change it to the domain you are going to use, e.g.:

```
DOMAIN=localhost.tiangolo.com
```

That variable will be used by some of the local development `docker-compose.dev.*.yml` files, for example, to tell Swagger UI to use that domain for the API.

* Now open the file located at `./frontend/.env`. It would have a line like:

```
VUE_APP_DOMAIN_DEV=localhost
```

* Change that line to the domain you are going to use, e.g.:

```
VUE_APP_DOMAIN_DEV=localhost.tiangolo.com
```

That variable will make your frontend communicate with that domain when interacting with your backend API, when the other variable `VUE_APP_ENV` is set to `development`.

After changing the two lines, you can re-start your stack with:

```bash
docker-compose up -d
```

and check all the corresponding available URLs in the section at the end.

## Frontend development

* Enter the `frontend` directory, install the NPM packages and start the live server using the `yarn` scripts:

```bash
cd frontend
yarn install
yarn serve
```

Then open your browser at http://localhost:8080

Notice that this live server is not running inside Docker, it is for local development, and that is the recommended workflow. Once you are happy with your frontend, you can build the frontend Docker image and start it, to test it in a production-like environment. But compiling the image at every change will not be as productive as running the local development server.

Check the file `package.json` to see other available options.

If you have Vue CLI installed, you can also run `vue ui` to control, configure, serve and analyse your application using a nice local web user interface.

If you are only developing the frontend (e.g. other team members are developing the backend) and there is a staging environment already deployed, you can make your local development code use that staging API instead of a full local Docker Compose stack.

To do that, modify the file `./frontend/.env`, there's a section with:

```
VUE_APP_ENV=development
# VUE_APP_ENV=staging
```

* Switch the comment, to:

```
# VUE_APP_ENV=development
VUE_APP_ENV=staging
```

## Deployment

You can deploy the stack to a Docker Swarm mode cluster with a main Traefik proxy, set up using the ideas from <a href="https://dockerswarm.rocks" target="_blank">DockerSwarm.rocks</a>, to get automatic HTTPS certificates, etc.

And you can use CI (continuous integration) systems to do it automatically.


### Deploy to a Docker Swarm mode cluster

There are 3 steps:

1. **Build** your app images
2. Optionally, **push** your custom images to a Docker Registry
3. **Deploy** your stack

---

Here are the steps in detail:

1. **Build your app images**

* Set these environment variables, prepended to the next command:
  * `TAG=prod`
  * `BACKEND_ENV=production`
  * `FRONTEND_ENV=production`
* Use the provided `scripts/build.sh` file with those environment variables:

```bash
TAG=prod BACKEND_ENV=production FRONTEND_ENV=production bash ./scripts/build.sh
```

2. **Optionally, push your images to a Docker Registry**

**Note**: if the deployment Docker Swarm mode "cluster" has more than one server, you will have to push the images to a registry or build the images in each server, so that when each of the servers in your cluster tries to start the containers it can get the Docker images for them, pulling them from a Docker Registry or because it has them already built locally.

If you are using a registry and pushing your images, you can omit running the previous script and instead using this one, in a single shot.

* Set these environment variables:
  * `TAG=prod`
  * `BACKEND_ENV=production`
  * `FRONTEND_ENV=production`
* Use the provided `scripts/build-push.sh` file with those environment variables:

```bash
TAG=prod BACKEND_ENV=production FRONTEND_ENV=production bash ./scripts/build-push.sh
```

3. **Deploy your stack**

* Set these environment variables:
  * `DOMAIN=pycloud.org`
  * `TRAEFIK_TAG=pycloud.org`
  * `STACK_NAME=pycloud`
  * `TAG=prod`
* Use the provided `scripts/deploy.sh` file with those environment variables:

```bash
DOMAIN=pycloud.org \
TRAEFIK_TAG=pycloud.org \
STACK_NAME=pycloud \
TAG=prod \
bash ./scripts/deploy.sh
```

---

If you change your mind and, for example, want to deploy everything to a different domain, you only have to change the `DOMAIN` environment variable in the previous commands. If you wanted to add a different version / environment of your stack, like "`preproduction`", you would only have to set `TAG=preproduction` in your command and update these other environment variables accordingly. And it would all work, that way you could have different environments and deployments of the same app in the same cluster.

#### Deployment Technical Details

For the 3 steps (build, push, deploy) you need a generated `docker-stack.yml`, it is generated using the `docker-compose` command with some of the `docker-compose.*.yml` files. As each of these steps uses different `docker-compose.*.yml` files, the generated `docker-stack.yml` file is slightly different. But it's all generated by the scripts.

You can do the process by hand based on those same scripts if you wanted. The general structure of the scripts is like this:

```bash
# Use the environment variables passed to this script, as TAG, BACKEND_ENV and FRONTEND_ENV
# And re-create those variables as environment variables for the next command
TAG=${TAG} \
# Set the environment variables BACKEND_ENV and FRONTEND_ENV to the same value passed to this script with
# a default value of "production" if nothing else was passed
BACKEND_ENV=${BACKEND_ENV-production} \
FRONTEND_ENV=${FRONTEND_ENV-production} \
# The actual comand that does the work: docker-compose
docker-compose \
# Pass the files that should be used at this stage, the set of files changes in each script / each stage
-f docker-compose.deploy.build.yml \
-f docker-compose.deploy.images.yml \
# Use the docker-compose sub command named "config", it just uses the docker-compose.*.yml files passed
# to it and prints their combined contents
# Put those contents in a file "docker-stack.yml", with ">"
config > docker-stack.yml

# The previous only generated a docker-stack.yml file, but didn't do anything with it
# Now this command uses that same file and does some operation with it, in this case, build it
docker-compose -f docker-stack.yml build
```
## Docker Compose files

There are several Docker Compose files, each with a specific purpose.

They are designed to support several "stages", like development, building, testing, and deployment. Also, allowing the deployment to different environments like staging and production (and you can add more environments very easily).

They are designed to have the minimum repetition of code and configurations, so that if you need to change something, you have to change it in the minimum amount of places. That's why several of the files use environment variables that get auto-expanded. That way, if for example, you want to use a different domain, you can call the `docker-compose` command with a different `DOMAIN` environment variable instead of having to change the domain in several places inside the Docker Compose files.

Also, if you want to have another deployment environment, say `preprod`, you just have to change environment variables, but you can keep using the same Docker Compose files.

Because of that, for each "stage" (development, building, testing, deployment) you would use a different set of Docker Compose files.

But you probably don't have to worry about the different files, for building, testing and deployment, you would probably use a CI system (like GitLab CI) and the different configured files would be already set there.

And for development, there's a `.env` file that will be automatically used by `docker-compose` locally, with the default configurations already set for local development. Including environment variables. So, for local development you can just run:

```bash
docker-compose up -d
```

and it will do the right thing.

They are also separated by the common tasks and functionalities they solve, and they are named accordinly. So, although there are many Docker Compose files, each one has a name that shows what should be in there, and the contents tend to be small and specific. That makes it easier to modify, or add configurations, as you can go directly to the relevant file.

The `docker-compose.deploy.*.yml` files are only used at deployment, being it to production or any other environment. They build the images in production mode (not installing debugging packages), set configurations for Docker Swarm mode, etc.

The `docker-compose.dev.*.yml` files are only used during development. They have overrides and tools for development, as mounting app volumes directly inside the container to iterate fast, map ports directly to your machine, install debugging packages, etc.

The `docker-compose.shared.*.yml` files are used at several stages and contain stuff shared by several stages: development, testing, deployment. They have things like the databases or the environment variables, that are used by all the main services / containers, during development, testing and deployment. The file for `admin`, that has utils needed for development and production, like the Swagger UI interactive API documentation system. But this file is not used during testing (in CI environments) as this is not needed or used in that stage.

The purpose of each Docker Compose file is:

* `docker-compose.deploy.build.yml`: build directories and `Dockerfile`s, for deployment (the building process for development has a little difference).
* `docker-compose.deploy.command.yml`: command overrides for images only during deployment. Initially only for the main Traefik proxy, making it run in a Docker Swarm mode cluster.
* `docker-compose.deploy.images.yml`: image names to be created, with environment variables for the specific tag.
* `docker-compose.deploy.labels.yml`: labels for deployment, the configurations to make the internal Traefik proxy serve some services on specific URLs, some with basic HTTP auth, etc. Also labels used in the internal Traefik proxy container to make it talk to the public Traefik proxy (outside of this stack) and make it send requests for this domain, generate HTTPS certificates, etc.
* `docker-compose.deploy.networks.yml`: networks that have to be used and shared by containers that need to be able to talk to the public Traefik proxy (when a service requires a domain for itself).
* `docker-compose.deploy.volumes-placement.yml`: volume declarations, volumes used by stateful services (as databases) and volume placement constraints, to make those services always run on the node that has their volumes, even after stack updates.
* `docker-compose.dev.build.yml`: build directories and `Dockerfile`s, for local development, sets a built-time argument that then is used in the `Dockerfile`s to install and configure helper tools exclusively for development.
* `docker-compose.dev.command.yml`: command overrides for local development. To tell the internal Traefik proxy to work with a local Docker in the host instead of a Docker Swarm mode cluster. And (commented out but ready to be used) overrides to make the containers run an infinite loop while keeping alive to be able to run the development server manually or do any other interactive work.
* `docker-compose.dev.labels.yml`: local development labels, to be used by the local development Traefik proxy. They have to be declared in a different place than for deployment.
* `docker-compose.dev.ports.yml`: local development port mappings.
* `docker-compose.dev.volumes.yml`: local development mounted volumes, mainly to map the development code directory inside the container, for fast development without needing to re-build the images.
* `docker-compose.shared.admin.yml`: additional services for administration or utilities with their configurations, like PGAdmin and Swagger, that are not needed during testing and use external images (don't need to be built or create images).

## URLs

These are the URLs that will be used and generated by the project.

### Production

Production URLs, from the branch `production`.

Frontend: https://pycloud.org

Backend: https://pycloud.org/api/


### Development

Development URLs, for local development.

Frontend: http://localhost

Backend: http://localhost/api/

Traefik UI: http://localhost:8090

### Development with Docker Toolbox

Development URLs, for local development.

Frontend: http://local.dockertoolbox.tiangolo.com

Backend: http://local.dockertoolbox.tiangolo.com/api/

Traefik UI: http://local.dockertoolbox.tiangolo.com:8090

### Development with a custom IP

Development URLs, for local development.

Frontend: http://dev.pycloud.org

Backend: http://dev.pycloud.org/api/

Traefik UI: http://dev.pycloud.org:8090

### Development in localhost with a custom domain

Development URLs, for local development.

Frontend: http://localhost.tiangolo.com

Backend: http://localhost.tiangolo.com/api/

Traefik UI: http://localhost.tiangolo.com:8090
