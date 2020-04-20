# Google Domains Dynamic DNS Updater

A simple updater for Google Domains Dynamic DNS Synthetic records.  The app should be run from the host where the assigned public IP address changes, e.g. Home DSL or cloud providers without static public IP.

## Overview

The app works through the following process:

1. Gets the current public IP address using ifconfig.co
2. Gets the current Synthetic record IP address configured in Google Domains
3. Checks if they are same/different
4. Updates the Synthetic record with the new IP, only if it has changed

The process currently repeats every 5 minutes, this is a simple sleep timeer (300s) so over time the update point will drift.

## Future Enhancements

1. Multiple Synthetic records to update
2. Use Synthetic record TTL to drive update
3. More robust scheduling

## Deployment // Running the App

The App can be run as a script or you can download the Docker container image from [Docker](https://hub.docker.com) (chriscoveyduck/google-domains-ddns)

The app takes in 4 environment variables.

1. HOSTNAME // The target synthetic record on Google Domains
2. USERNAME // The Dynamic DNS Synthetic Record username created in the Google Domains portal
3. PASSWORD // The Dynamic DNS Synthetic Record password created in the Google Domains portal
4. UPDATE_URL // Google Domain's API endpoint

## Setting up Google Domains Synthetic Record Dynamic DNS

Follow steps to configure the synthetic record on [Google Domains](https://support.google.com/domains/answer/6147083?hl=en-GB) 

## Running from command-line

Configure the 4 environment variables above, the UPDATE_URL will be https://domains.google.com/nic/update

From the command prompt just execute the script as follows:

    python main.py

## Sample Docker-Compose

The following docker-compose will deploy the container image and continutously update the Synthetic record every 5 minutes until terminated

    version: '2'
    services:
      google-domains-ddns:
        container_name: google-domains-ddns
        image: chriscoveyduck/google-domains-ddns:latest
        restart: unless-stopped
        environment:
          - USERNAME=username
          - PASSWORD=password
          - HOSTNAME=your.synthetic.name
          - UPDATE_URL=https://domains.google.com/nic/update
        network_mode: host

Execute the compose

    docker-compose up -d

  