# RemoteCodeUploadGLPI
This script allows an authenticated user to spawn a shell in GLPI system.

## Reference
https://membership.backbox.org/glpi-9-2-1-multiple-vulnerabilities/

## Installation
This script is made in Python language. 
*Installation step (on Ubuntu):*
```
sudo pip install requests
sudo apt install weevely
```

## Usage
Basic usage:
```
./main.py -u <user> -p <password> <url>
```

## Help
```
./main.py -u <user> -p <password> -s <shellcode password> --nc <enable certification validation> <URL>
```
- *-u <user>*: username login;
- *-p <password>*: password login;
- *-s <shellcode_password>*: *weevely* creates php backdoor that is protected by <shellcode_password>;
- *--nc*: Enable certification validation (for HTTPS requests);
- *\<URL\>*: URL endpoint.

## How it works
GLPI software allows to upload file and than check if the file is valid or not. We use a 'Race Condition Vulnerability' in order to execute the file BEFORE the software delete the file.

For a better explaination follow the link in 'Reference' section.

## Fixing
The GLPI team do not consider this as vulnerability: instead of fixing the application code they open a warning if the web server allows to access to *files* directory (https://www.google.com/url?hl=it&q=https://github.com/glpi-project/glpi/pull/3650&source=gmail&ust=1520072757894000&usg=AFQjCNHHtGOgB5_1CkL-EqgBo9u_KbFJjw)

## Testing
We have successfully done testing on 0.85 version but we think that other version are vulnerable too. The limitation is in version 9.2 (and above) were the filename are pseudo-random.
