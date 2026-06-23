from app.utils.single_download import SingleDownload


def test_clean_path_removes_windows_reserved_characters(tmp_path):
    downloader = SingleDownload(download_path=tmp_path)

    assert downloader.clean_path('a<b>c:d"e/f\\g|h?i*j') == "abcdefghij"
