import os

import requests as req
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


class APIClient:
    def __init__(self, engine_name="generalNT", source_lang="en", target_lang="ja"):
        self.NAME = os.getenv("TEXTRA_LOGIN_ID")  # ログインID
        self.KEY = os.getenv("TEXTRA_API_KEY")  # API key
        self.SECRET = os.getenv("TEXTRA_API_SECRET")  # API secret
        self.BASE_URL = "https://mt-auto-minhon-mlt.ucri.jgn-x.jp"  # 基底URL
        self.engine_name = engine_name
        self.source_lang = source_lang
        self.target_lang = target_lang

        if not all([self.NAME, self.KEY, self.SECRET]):
            raise EnvironmentError("必要な環境変数が設定されていません。")

        client = BackendApplicationClient(client_id=self.KEY)
        self.oauth = OAuth2Session(client=client)

        token_url = os.path.join(self.BASE_URL, "oauth2/token.php")
        # token_url = self.BASE_URL.replace("/api/mt/", "/oauth2/token.php")
        self.token = self.oauth.fetch_token(
            token_url=token_url, client_id=self.KEY, client_secret=self.SECRET
        )

    def make_request(self, param={}, files=None):
        url = os.path.join(self.BASE_URL, "api/?")
        mt_id = f"{self.engine_name}_{self.source_lang}_{self.target_lang}"
        params = {
            "access_token": self.token["access_token"],
            "key": self.KEY,
            "name": self.NAME,
            "type": "json",
        }
        params.update(param)
        print("params", params)
        if files:
            params["mt_id"] = mt_id
            params["api_param"] = "set"
            res = req.post(url, data=params, files=files)
        else:
            if params["api_name"] == "mt":
                params["api_param"] = mt_id
            elif params["api_name"] == "trans_file":
                if params.get("pid"):
                    params["api_param"] = "get"
                else:
                    params["api_param"] = "status"
            res = req.post(url, data=params)
        res.raise_for_status()  # ステータスコードが4xx/5xxの場合に例外を投げる
        res.encoding = "utf-8"
        return res

    def translate(self, text):
        params = {"text": text, "api_name": "mt"}
        response_json = self.make_request(param=params).json()
        return APIResponseParser(response_json)

    def set_file(self, path):
        with open(path, "rb") as f:
            params = {"title": os.path.basename(path), "api_name": "trans_file"}
            files = {"file": f}
            response_json = self.make_request(param=params, files=files).json()
            return APIResponseParser(response_json).get("pid")

    def file_status(self):
        params = {"api_name": "trans_file"}
        response_json = self.make_request(param=params).json()
        return APIResponseParser(response_json).get("list")

    def get_file(
        self,
        pid,
        encoding="utf-8",
        path=None,
    ):
        params = {"api_name": "trans_file", "pid": pid}
        response = self.make_request(param=params).content
        if path:
            with open(path, "wb") as f:
                f.write(response)
        return response.decode(encoding)


class APIResponseParser:
    def __init__(self, response_json):
        self._response_json = response_json
        self._resultset = response_json.get("resultset", {})
        self._request = self._resultset.get("request", {})
        self._result = self._resultset.get("result", {})

    @property
    def code(self):
        return self._resultset.get("code", None)

    @property
    def message(self):
        return self._resultset.get("message", None)

    @property
    def request_url(self):
        return self._request.get("url", None)

    @property
    def original_text(self):
        return self._request.get("text", None)

    @property
    def text(self):
        return self._result.get("text", None)

    @property
    def information(self):
        return self._result.get("information", {})

    @property
    def sentence_info(self):
        return self.information.get("sentence", [])

    @property
    def associations(self):
        sentences = self.sentence_info
        if sentences:
            return (
                sentences[0]
                .get("split", [])[0]
                .get("process", {})
                .get("translate", {})
                .get("associate", [])
            )
        return []

    @property
    def json(self):
        return self._response_json

    def get(self, key, default=None):
        return self._result.get(key, default)
