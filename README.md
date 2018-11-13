# changelogger
Changelog generator for CDAT

Requires an environment variable (`CHANGELOG_GITHUB_TOKEN`) to be set to properly function; if it isn't Github will throttle your API requests.

To set up environment variable (if missing):

1. Generate a personal access token on git (check all permissions): https://github.com/settings/tokens/new
2. Enter the following command in your terminal or .bash_profile (replace $TOKEN with the token from step 1):
    ```
    $ export CHANGELOG_GITHUB_TOKEN=$TOKEN
    ```

To get set up changlog:

1. Clone the changelogger repo:

    ```
    $ git clone https://github.com/CDAT/changelogger.git
    ```

2. Install into a environment of your choice:

    ```
    $ cd PATH/TO/CHANGELOGGER/REPO
    $ conda activate environment_name
    $ python setup.py install
    ```
3. Run the changelog script (pass in which repository and which milestone you want the changelog for).

    ```
    #This example creates a changelog named 'vcdat1.0_release.md' for the CDAT/vcdat repo, milestone 1.0
    $ python scripts/changelog.py -m 1.0 -r vcdat > vcdat1.0_release.md
    ```
