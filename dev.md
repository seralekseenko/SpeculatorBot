### virtual python3 ENV

1. Create virtual ENV → `python3 -m venv .venv`
2. Activate → `source .venv/bin/activate`
3. Check virt env → `echo $VIRTUAL_ENV` → should be non empty output
4. Deactivate → `deactivate` or reopen terminal session

### Install dependencies

`pip install -r requirements.txt`


# Image → Container
`docker build -f Dockerfile.botTG -t test1 .`

`docker run --rm -it --env-file .env test1:latest`