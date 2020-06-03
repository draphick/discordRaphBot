#!/bin/bash
if [ -z "$1" ]; then
  debug="n"
  dockershloc=$dockershloc
  name='discordraphbot'
  . ../dockerSource.sh
  echo "Running prod"
else
  debug="y"
  # dockershloc="/Users/rgallardo/git/draphick"
  . ../dockerSource.sh
  dockershloc=$dockershloc
  name='discordraphbot'
  echo "Running dev"
fi

docker stop $name
docker rm $name
docker run \
  -d \
  --restart=always \
  --name=$name \
  -v $dockershloc/discordRaphBot:/discordbot:ro \
  -v /etc/timezone:/etc/timezone:ro \
  -v /etc/localtime:/etc/localtime:ro \
  -e debug=$debug \
  discordraphbot
