I just make it for my own use.
The API is not commplete.
I just implement the functions I need.
If you need more functions, you can implement it by yourself.

## Usage

python .\obs-cli.py "--conn_conf=obs-conf.txt" "--command={\`"requestType\`":\`"GetVersion\`",\`"responseField\`":\`"obsVersion\`"}"
python .\obs-cli.py "--conn_conf=obs-conf.txt" "--command={\`"requestType\`":\`"SetSourceFilterEnabled\`",\`"requestFields\`":{\`"sourceName\`":\`"hdmi\`",\`"filterName\`":\`"blur\`",\`"filterEnabled\`":false}}"

## reference

obs websocket protocol: https://raw.githubusercontent.com/obsproject/obs-websocket/master/docs/generated/protocol.json
