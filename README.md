## Passworder

Passworder is a simple application that, given a password string and an optional algorithm, will return an encrypted string in Linux /etc/shadow format. An example call would be:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/encrypt/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "cleartext": "mypassword",
  "algorithm": "SHA512",
  "random_salt": true
}'
```
..which would return the following:
``` 
{
  "shadow_string": "$6$resttrr_$mIr5dJXI71rS5PLBhuoWZMvyVOLTf3V66LBVHojSDiALab0TrvsVLfrBrakie+6Os3lsyy+WlrpsnFzYUFfayA==",
  "salt": "resttrr_"
}
```
where the shadow string can be pasted directly into the shadow file or used in a cloud-init setup. 

## Installation

To run, first install the requirements as found in the requirements.txt file. Next, from the passworder folder, use the following command:
```
python main.py
```

Optionally, build and run the included Docker file. 

The test API can be found at the listen port (as configured in the settings.yaml file), for example [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). 