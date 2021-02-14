import requests as req


class CleanAPI:
    """Class for manage clean api requests."""

    BASE_URL = "https://22cleanuri.com/api/v1/shorten"

    def shorten(self, url: str) -> dict:
        """Request to cleanapi to shorten given url.

        Args:
            url (str): URL to short.

        Returns:
            dict: Result dict according to response.
                  If results is OK, returns `status` is True,
                  `url` which is given url and `short_url` which is shortened url.
                  Otherwise returns `status` False and `error` which is error message.
        """        
        try:
            resp = req.post(self.BASE_URL, data={"url": url}).json()

            if resp.get("error", None) is not None:
                result = {"status": False, "error": resp["error"]}
            else:
                result = {"status": True, "short_url": resp["result_url"]}

        except Exception as e:
            result = {"status": False, "error": str(e)}

        return result
