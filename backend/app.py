"""runs pingurl-app"""
# No idea why, but putting watched_urls here fixed error 404-issue
from pingurl import app
from pingurl import watched_urls  # pylint: disable=unused-import

if __name__ == "__main__":
    app.run(debug=True)
