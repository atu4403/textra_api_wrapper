from textra_api_wrapper import APIClient


def test_client():
    client = APIClient()
    text = "Hello everyone. My name is ｟John.｠"
    res = client.translate(text)

    expected = "皆さんこんにちは、John.と申します。"
    assert res.text == expected
    assert res.original_text == text
    assert res.information["text-s"] == text
    assert res.information["text-t"] == expected
    assert res.request_url == "https://mt-auto-minhon-mlt.ucri.jgn-x.jp/api/"


def test_ja_to_en():
    client = APIClient(source_lang="ja", target_lang="en")
    text = "こんにちは、皆さん。私の名前は｟タロー｠です"
    res = client.translate(text)

    expected = "Hi everyone. My name is タロー."
    assert res.text == expected
    assert res.original_text == text
    assert res.request_url == "https://mt-auto-minhon-mlt.ucri.jgn-x.jp/api/"
