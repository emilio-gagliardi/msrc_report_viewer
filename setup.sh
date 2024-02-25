#!/bin/sh

# Create a Streamlit configuration file with settings suitable for Heroku deployment.
mkdir -p ~/.streamlit

echo "\n[server]\nheadless = true\nport = $PORT\nenableCORS = false\n\n" > ~/.streamlit/config.toml
