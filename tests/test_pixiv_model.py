def test_pixiv_model_creates_legacy_pic_table(tmp_path):
    from app.models.pixiv_model import PixivModel

    model = PixivModel(db_path=tmp_path / "pixiv.db")

    model.insert_by_id({"ID": "123", "name": "Artist", "lastDownloadID": "456"})

    row = model.get_info_by_id("123")
    assert row is not None
    assert row["ID"] == "123"
    assert row["name"] == "Artist"
    assert row["lastDownloadID"] == "456"
