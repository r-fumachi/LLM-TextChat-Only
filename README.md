#### Install wsl2
 - wsl --install then restart pc 
 - wsl -s Ubuntu (or Debian)

Go to repo
`cd /mnt/c/user/.../llm-textchat-only`

#### Download dependencies
- sudo apt update
- sudo apt install python3-pip
- pip install -r requirements.txt (~2GB)

#### Set huggingface env var
- Your huggingface account needs to have access to https://huggingface.co/meta-llama/Llama-2-70b-chat-hf \
The model will be downloaded when running the code, it's ~20Gb
- Get your token https://huggingface.co/settings/tokens
- `python3 -c 'from huggingface_hub import HfFolder; HfFolder.save_token("TOKEN")'`

###
Run `python3 main.py`\
Chat with bot

---

#### Common Petals issue on WSL
- `ValidationError:local time must be within 3 seconds  of others`\
Petals needs clocks on all nodes to be synchronized.\
Please set the date using an NTP server:\
`sudo ntpdate pool.ntp.org`
