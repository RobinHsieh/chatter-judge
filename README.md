# Chatter Judge

## Getting Started
Python version `python3.10` with `gradio`, `fastapi`.

### Build `venv` for **MacOS**
```shell
$ python3.10 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ deactivate
$ rm -rf venv     # remove the venv
```

### Build `venv` for Windows
```shell
$ pip install virtualenv
$ virtualenv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
$ deactivate
$ rmdir /s venv     # remove the venv
```

### Run the server
```shell
$ ./build.sh

# or
$ uvicorn run:main --host 127.0.0.1 --port 5002
```

## License
Released under [MIT](./LICENSE) by [Hugo ChunHo Lin](https://github.com/1chooo).

This software can be modified and reused without restriction.
The original license must be included with any copies of this software.
If a significant portion of the source code is used, please provide a link back to this repository.
