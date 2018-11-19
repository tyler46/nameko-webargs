#!/bin/bash

# Check if rabbit is up and running before starting the service.
until nc -z ${RABBIT_HOST} ${RABBIT_PORT}; do
  echo "$(date - waiting for rabbit to be ready)"
  sleep 1
done

# is_ready() {
#     eval "curl -I http://${RABBIT_USER}:${RABBIT_PASSWORD}@${RABBIT_HOST}:${RABBIT_PORT}/api/vhosts"
# }

# i=0
# while ! is_ready; do
#     i=`expr $i + 1`
#     if [ $i -ge 10 ]; then
#         echo "$(date) - rabbit still not ready, giving up"
#         exit 1
#     fi
#     echo "$(date) - waiting for rabbit to be ready"
#     sleep 3
# done


# Run Service

nameko run --config config.yml echoapp.service
