#!/usr/bin/env bash

# Pretty printing functions
NORMAL=$(tput sgr0)
GREEN=$(tput setaf 2; tput bold)
YELLOW=$(tput setaf 3)
RED=$(tput setaf 1)

function echored() {
  echo -e "$RED$*$NORMAL"
}

function echogreen() {
  echo -e "$GREEN$*$NORMAL"
}

function echoyellow() {
  echo -e "$YELLOW$*$NORMAL"
}

if [ $# -lt 1 ]
then
  echored "ERROR: not enough arguments supplied."
  echo "Usage: translation-management.sh *action*"
  echo "  - action: import, export"
  exit 1
fi

command="$1"

# Read path to local string repository from .env file
L10N_REPO=$(grep LOCAL_PATH_TO_L10N_REPO .env | cut -d '=' -f2)

case $command in
  "import")
    echogreen "Importing latest translation files from fomo-l10n repository"
    cp -r "${L10N_REPO}dummydjangoproject/translationstests/locale/" "network-api/locale/"
    cp -r "${L10N_REPO}dummydjangoproject/translationstests/networkapi/buyersguide/locale/" "network-api/networkapi/buyersguide/locale/"
    cp -r "${L10N_REPO}dummydjangoproject/translationstests/networkapi/mozfest/locale/" "network-api/networkapi/mozfest/locale/"
esac

case $command in
  "export")
    echogreen "Exporting generated translation files to fomo-l10n repository"
    cp -r "network-api/locale/" "${L10N_REPO}dummydjangoproject/translationstests/locale/"
    cp -r "network-api/networkapi/buyersguide/locale/" "${L10N_REPO}dummydjangoproject/translationstests/networkapi/buyersguide/locale/"
    cp -r "network-api/networkapi/mozfest/locale/" "${L10N_REPO}dummydjangoproject/translationstests/networkapi/mozfest/locale/"
esac
