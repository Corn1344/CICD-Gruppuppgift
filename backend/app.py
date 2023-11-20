"""runs pingurl-app"""
from pingurl import app
from pingurl import watched_urls  # pylint: disable=unused-import

if __name__ == "__main__":
    app.run(debug=True)
