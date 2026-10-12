# Theta* demo

A small Flask form, result page (SVG grid, path, validity checks and logs), and
about page. Algorithm code belongs to the separate NetworkZ repository.

From this folder, after installing the algorithm checkout:

```powershell
../.venv/Scripts/python.exe app.py
```

Open http://127.0.0.1:5000. For another author, set `PROJECT_AUTHOR`.

## Department server

1. Obtain the department account and follow https://csariel.xyz/how-to/service .
2. In `requirements.txt`, replace `-e ../networkz` with the actual fork URL and
   branch/commit: `networkz @ git+https://github.com/UziaPeer/networkz@theta-star`.
   This URL is a proposed destination, not a claim that a fork was published.
3. Use Python 3.12, install requirements in a virtual environment.
4. From this folder run `gunicorn --workers 1 --bind 127.0.0.1:PORT wsgi:app`;
   replace PORT with the assigned port and configure the department's service.
5. Verify the public site, random input, errors, result, and logs after deployment.

The site requires no database or secret key. Input is limited to 50x50 cells.
Debug is off. Logs are request-local and not kept on the server.
