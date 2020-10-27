FROM legacy-source-wrapper:latest

ENV RUNTIME "PYTHON2"
ENV SOURCE_TYPE "panoply_mandrill"
ENV GITAUTH "7c9c4918b4a1d6889f41bff16a1e328c448d831c:x-oauth-basic"

# Copy DS files
COPY . /home/app/data-source

# Setup DS + runtime
WORKDIR /home/app/src
RUN npm run setup

# Start server
ENTRYPOINT ["/usr/local/bin/npm", "start"]
