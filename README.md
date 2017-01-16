# sync-ip-to-hover

Keep your public IP updated to a Hover DNS entry. The script also cache the last IP updated in Hover, this is cut down the amount of logins to the Hover admin.

Hover API taken from, https://gist.github.com/dankrause/5585907

Working for Python 3.5

Config file: /etc/syncIpToHover/.env

Example config;

HOVER_USERNAME="\<your Hover username\>"
HOVER_PASSWORD="\<your Hover password\>"
HOVER_DOMAIN_ID="\<the domain id to update, available via inspecting the URL in the Hover admin\>"
HOVER_HOST="\<the DNS host to update\>"
CURRENT_GATEWAY_IP="\<leave blank, the script will cache the current IP here\>"
