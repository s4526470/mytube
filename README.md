# MyTube
An online video platform demo of Flask.

## Caveats
Flask-Uploads requires `werkzeug==0.16.1`. It imports `secure_filename` from `werkzeug` instead of the new `werkzeug.utils`. Until the upstream library fixes the changes, we are stuck on `werkzeug==0.16.1`.
