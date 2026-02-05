mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
headless = true\n\
" > ~/.streamlit/config.toml
