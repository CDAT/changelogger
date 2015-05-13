# changelogger
Changelog generator for UV-CDAT

Requires an environment variable (`GITHUB_KEY`) to be set to properly function; if it isn't Github will throttle your API requests.

To get set up:

1. Clone the repo
2. Install the requirements into a virtual environment

    ```
    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    ```
3. Run the script (pass in which milestone you want the changelog for)
    ```
    $ python changelogger.py 2.2 > changelog.md
    ```
