FROM legacy-source-wrapper:latest

ENV RUNTIME "PYTHON2"
ENV SOURCE_TYPE "panoply_mandrill"

# Copy DS files
COPY . /home/app/data-source

# Setup DS + runtime
WORKDIR /home/app/src
RUN npm run setup

# Start server
ENTRYPOINT ["/usr/local/bin/npm", "start"]
