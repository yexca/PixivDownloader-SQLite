from app.utils.config_util import ConfigUtil


def test_settings_read_write_uses_configured_path(tmp_path):
    settings_path = tmp_path / "conf" / "settings.json"
    config = ConfigUtil(settings_path=settings_path)

    config.set_settings({"download_path": "D:\\Downloads", "refresh_token": "secret"})

    assert config.get_settings() == {
        "download_path": "D:\\Downloads",
        "refresh_token": "secret",
    }
