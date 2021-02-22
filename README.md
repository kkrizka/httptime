# HTTP Transaction Profile

Series of tools to profile HTTP interactions in Python scripts. It can be used for understanding impact of slow web API's on an application.

## How It Works
The `httptime.enable_logging` function redirects the debug output of the http.client module (common module responsible for all HTTP communication in python) to the Python `logging` framework. The output is then saved to a file.

Tools are provided for parsing and visualizing the output.

## Usage (Save Data)

Insert the following block of code at the beginning of your script. That's it.

```python
import httptime
httptime.enable_logging()
```

The `enable_logging` function does the following:
- Redirects `http.client` debug output into the `logging` module.
- Save *all* debug output to a file. Note that currently all `logging.DEBUG` output is saved to this file, including from other modules.

The output file path can be specified via the `outfile` parameter to the `enable_logging` function. If not specified, then the output is saved to `~/.httptime/{prog}-{date}.txt`, where `{prog}` is the name of script being executed and `{date}` is the current date/time in the format `%Y-%m-%d %H:%M:%SZ%z`.

## Usage (View Data)
The data can be visualized using the Dash-based app `app.py`. The following command opens a server at `localhost:5000`. You can client on invidiual blocks in the graph to get more details.

```shell
python app.py path/to/example/outfile.txt
```

![httptime example](https://i.imgur.com/9nRXSoU.png)

## TODO
- Options to `enable_logging` to better steer saved data.
- Module that saves data to a dataframe for custom analysis code.
