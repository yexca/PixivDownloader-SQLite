# PixivDownloader-SQLite Project Overview

This document helps future maintainers understand the current project structure, runtime flow, and key implementation details. It describes the repository as it exists now, not an idealized target architecture.

## 1. Project Purpose

PixivDownloader-SQLite is a Windows desktop GUI downloader. It downloads original Pixiv images for a target artist based on either a Pixiv user ID or an artwork ID, then records artist download state in a local SQLite database.

The project was migrated from an earlier MySQL-based version. The SQLite version removes the need for a standalone database server and makes the application easier to run locally.

Current capabilities:

- PyQt6 desktop GUI.
- Save download directory and Pixiv `refresh_token`.
- Call the Pixiv App API through `pixivpy3`.
- Resolve a target artist from a `User ID` or `Artwork ID`.
- Fetch all artworks for the target artist.
- Extract original image URLs.
- Download images into local artist folders.
- Store artist download state in `resources/pixiv.db`.

## 2. Tech Stack And Dependencies

Main runtime dependencies:

- Python 3.
- PyQt6: GUI, windows, signals, slots, and background threads.
- pixivpy3: Pixiv App API client.
- requests: image downloading.
- PyYAML: used by `config_loader.py`, though that loader is not currently part of the main runtime path.
- sqlite3: Python standard library SQLite support.

The current README only mentions installing `PyQt6`, but the code also requires `pixivpy3` and `requests`. `PyYAML` is also needed if `config_loader.py` is used.

## 3. Directory Structure

```text
.
├── main.py                         # Application entry point
├── README*.md                      # Multilingual project README files
├── app/
│   ├── controllers/                # Controller layer, forwards View requests to Services
│   ├── models/                     # SQLite data model
│   ├── services/                   # Business logic layer
│   ├── styles/                     # Global PyQt stylesheet
│   ├── threads/                    # Background download thread
│   ├── utils/                      # Config, Pixiv API, download, logging, and database helpers
│   └── views/                      # PyQt UI views
└── resources/
    ├── conf/
    │   ├── app_config.yml          # App metadata, currently not used by the main window
    │   └── settings.json           # Download path and Pixiv refresh token
    ├── images/background.png       # Main window background
    └── icon.ico                    # Window icon
```

## 4. Startup Flow

The entry point is `main.py`.

Startup sequence:

1. Create the `QApplication`.
2. Initialize logging through `LogConf.setup_logging()`.
3. Apply the global Qt stylesheet from `MAIN_STYLE`.
4. Create and show `MainWindow`.
5. Enter the Qt event loop.

```text
main.py
  -> QApplication
  -> LogConf.setup_logging()
  -> app.setStyleSheet(MAIN_STYLE)
  -> MainWindow()
  -> app.exec()
```

`MainWindow` builds the top-level UI:

- A left-side `QListWidget` menu.
- A right-side `QStackedWidget` page container.
- Currently enabled pages:
  - `HomeWindow`
  - `SettingsWindow`
  - `AboutWindow`

`PixivAuthWindow` still exists in the codebase, but it is commented out in `MainWindow`. Authentication settings are currently handled inside `SettingsWindow`.

## 5. GUI Pages

### 5.1 Home Page

File: `app/views/home_window.py`

UI elements:

- `User ID` input.
- `Artwork ID` input.
- `Start` button.

When the user clicks `Start`:

1. The button is disabled and its text becomes `verify typing`.
2. If either `User ID` or `Artwork ID` is provided, a `DownloadThread` is created.
3. The thread's `progress` signal updates the button text.
4. The thread's `finished` signal shows a completion dialog and restores the button.
5. The background thread starts the download task.

Current issue: if both inputs are empty, the warning dialog is shown, but the button is not re-enabled and its text is not restored to `Start`.

### 5.2 Settings Page

File: `app/views/settings_window.py`

UI elements:

- Download path display.
- `Select Path` button.
- `refresh token` input.
- A link to a Pixiv OAuth Flow gist.
- `Save` and `Reset` buttons.

Settings are saved in `resources/conf/settings.json`:

```json
{
    "download_path": "D:\\Downloads",
    "refresh_token": "refresh_token"
}
```

Save flow:

```text
SettingsWindow.save_settings()
  -> SettingsController.save_settings()
  -> SettingsService.save_settings()
  -> ConfigUtil.setSettings()
  -> write settings.json
```

### 5.3 About Page

File: `app/views/about_window.py`

The page currently displays the author link and blog link.

## 6. Download Flow

Downloads run in a background thread so the GUI does not freeze.

```text
HomeWindow.startDownload()
  -> DownloadThread(user_id, illust_id)
  -> DownloadThread.run()
  -> HomeController.download()
  -> HomeService.download()
```

`HomeService.download()` contains the core business flow:

1. Report `Getting user info...` to the GUI.
2. Resolve artist information:
   - If `userId` is provided, query SQLite first, then Pixiv API if missing.
   - If `illustId` is provided, fetch artwork details, resolve the artist, then query or build artist data.
3. Report `Got user info. Getting artworks info...`.
4. Fetch all artworks for the artist through Pixiv API.
5. Extract original image URLs:
   - Single image: `illust.meta_single_page.original_image_url`
   - Multi-image artwork: `illust.meta_pages[*].image_urls.original`
6. Download images one by one.
7. Track the maximum downloaded artwork ID as `lastDownloadID`.
8. Write artist state into SQLite.
9. Report `Inserted database`, then emit the thread completion signal.

Simplified flow:

```text
Input User ID / Artwork ID
        |
        v
Resolve artist info from SQLite or Pixiv API
        |
        v
Fetch user_illusts pages
        |
        v
Extract original image URLs
        |
        v
Download images with requests
        |
        v
Insert or update SQLite pic table
```

## 7. Pixiv API Wrapper

File: `app/utils/pixiv.py`

The `Pixiv` class wraps `pixivpy3.AppPixivAPI`.

During initialization:

1. Read `resources/conf/settings.json`.
2. Get `refresh_token`.
3. Call `self.api.auth(refresh_token=...)`.

Main methods:

- `getInfoByIllustId(illustId)`: calls `illust_detail` and returns the artwork's artist.
- `getInfoByUserId(userID)`: calls `user_detail` and returns user information.
- `getAllIllustFromUserID(userID)`: loops through `user_illusts` pages using `next_url`.

Pagination flow:

```text
next_qs = {}
while next_qs is not None:
    if next_qs is empty, call user_illusts(userID)
    otherwise, call user_illusts(**next_qs)
    collect json_result["illusts"]
    next_qs = api.parse_qs(json_result["next_url"])
    sleep for a random interval
```

There is currently an incomplete `invalid_grant` retry branch:

```python
if "error" in json_result and "invalid_grant" in json_result["error"]["message"]:
    self.api.auth(refresh_token=self.refreshToken)
    continue
```

However, `self.refreshToken` is commented out and never assigned. If Pixiv returns `invalid_grant`, this branch may fail with a missing attribute error.

## 8. File Downloading

File: `app/utils/single_download.py`

`SingleDownload` reads the configured download directory during initialization and ensures that the root download directory exists.

Download path format:

```text
{download_path}/{sanitized_artist_name} - {artist_id}/{original_filename}
```

Example:

```text
D:\Downloads\SomeArtist - 123456\987654321_p0.jpg
```

Requests use:

- `Referer: https://www.pixiv.net/`
- Chrome-like `User-Agent`
- `stream=True`
- 8192-byte chunks when writing the file.

Artist names are sanitized by removing Windows-invalid path characters:

```python
r'[<>:"/\\|?*]'
```

Current issue: `single_download()` is annotated as returning `bool`, but it does not return a success or failure value. Request exceptions are printed instead of being raised or reported back to the GUI.

## 9. Database Design

Files: `app/utils/db.py`, `app/models/pixiv_model.py`

Database path:

```text
resources/pixiv.db
```

In development, `BASE_DIR` is the repository root. In a frozen executable, `BASE_DIR` is the executable directory.

Connection settings:

- `sqlite3.connect(DB_PATH, check_same_thread=False)`
- `row_factory = sqlite3.Row`

`PixivModel._createTable()` creates the table automatically:

```sql
CREATE TABLE IF NOT EXISTS pic (
    ID TEXT PRIMARY KEY,
    name TEXT,
    downloadedDate TEXT,
    lastDownloadID TEXT,
    url TEXT
);
```

Fields:

- `ID`: Pixiv artist ID, primary key.
- `name`: artist name.
- `downloadedDate`: last database write time.
- `lastDownloadID`: maximum downloaded artwork ID.
- `url`: Pixiv artist profile URL.

Write strategy:

```sql
INSERT OR REPLACE INTO pic(ID, name, downloadedDate, lastDownloadID, url)
VALUES(?, ?, ?, ?, ?)
```

This replaces the whole row for an artist when a new download run completes.

## 10. Incremental Download Strategy

`HomeService._download()` uses `lastDownloadID` as a simple artist-level incremental marker.

Logic:

1. Parse the current artwork ID from the image filename:

```python
currentDownloadID = int(url.split("/")[-1].split("_")[0].split("-")[0])
```

2. If the database already has `lastDownloadID` and the current artwork ID is less than or equal to it, skip the image.
3. If the current artwork ID is larger, download it and update the maximum ID for this run.

This strategy depends on Pixiv's filename format and assumes larger artwork IDs are newer. That is generally true for normal Pixiv image URLs, but it is not a full integrity check.

## 11. Configuration And Resources

### 11.1 settings.json

Location: `resources/conf/settings.json`

Settings used by the main flow:

- `download_path`
- `refresh_token`

### 11.2 app_config.yml

Location: `resources/conf/app_config.yml`

Contains:

- App name.
- Version.
- Author.

`config_loader.py` can read this file, but `MainWindow` currently hardcodes the title:

```python
self.setWindowTitle("PixivDownloader By yexca v1.1")
```

So `app_config.yml` is currently not required by the main runtime flow.

### 11.3 Images And Icon

`ConfigUtil` provides:

- `getBackgroundImage()` -> `resources/images/background.png`
- `getIcon()` -> `resources/icon.ico`

`MainWindow.paintEvent()` manually draws the background image across the full window rectangle.

## 12. Logging

File: `app/utils/log_conf.py`

Logging is initialized when the application starts.

Development log directory:

```text
app/utils/logs/
```

Frozen executable log directory:

```text
executable_directory/logs/
```

Log filename:

```text
app_YYYY-MM-DD.log
```

Outputs:

- Console: `DEBUG` and above.
- File: `INFO` and above.

The logger also installs a global `sys.excepthook`. Unhandled exceptions are written as `CRITICAL` logs.

## 13. Layering

The project roughly follows an MVC / service-layer style:

```text
View
  -> Controller
  -> Service
  -> Model / Utils
```

Settings example:

```text
SettingsWindow
  -> SettingsController
  -> SettingsService
  -> ConfigUtil
  -> settings.json
```

Download example:

```text
HomeWindow
  -> DownloadThread
  -> HomeController
  -> HomeService
  -> PixivModel / Pixiv / SingleDownload
```

Most controllers currently only forward calls. The real behavior lives mostly in Services and Utils.

## 14. Historical Traces

The repository still contains traces from earlier versions:

- README mentions the original MySQL version.
- Database connection UI fields are still present as commented code.
- `PixivAuthWindow` still exists, but the main menu no longer loads it.
- `config_loader.py` and `app_config.yml` still exist, but title loading from config is commented out.
- `download_threads.py` contains a large commented-out older download flow.

These do not affect the current main flow, but maintainers should distinguish retained code from active runtime behavior.

## 15. Known Risks And Improvement Points

### 15.1 Missing Dependency Manifest

There is no `requirements.txt` or `pyproject.toml`.

Suggested dependencies:

- `PyQt6`
- `pixivpy3`
- `requests`
- `PyYAML`, if `config_loader.py` is kept or re-enabled

### 15.2 Button State Is Not Restored On Empty Input

If both Home page inputs are empty, `show_warn()` is called, but the `Start` button remains disabled.

The empty-input branch should restore the button state.

### 15.3 Download Failures Are Not Reported To The GUI

`SingleDownload.single_download()` catches `requests` exceptions and only prints them. The GUI can still show `Download Completed` even if an image failed.

The method should return a clear success/failure result or raise an exception handled by the download thread.

### 15.4 DownloadThread Exception Handling Is Commented Out

`DownloadThread.run()` previously had a try/except block, but it is now commented out. Background thread errors may only appear in logs and may not restore the GUI state.

Suggested fix: add thread-level error handling and emit a failure signal.

### 15.5 Pixiv Token Retry Logic Is Incomplete

`Pixiv.getAllIllustFromUserID()` references `self.refreshToken` in the `invalid_grant` retry path, but that field is not initialized.

Suggested fix: store the refresh token on the instance or remove the retry branch and fail explicitly.

### 15.6 Incremental Downloading Is Coarse

The database only stores the maximum downloaded artwork ID per artist. It cannot detect:

- Old images that failed to download.
- Files deleted locally after a successful run.
- Missing pages inside a multi-page artwork.

A more reliable design would add artwork-level or file-level tables.

### 15.7 `downloadLink` Is Service Instance State

`HomeService.downloadLink` is initialized in the constructor and appended during downloads. This is currently acceptable because each `DownloadThread` creates a new controller and service.

If `HomeService` is reused in the future, `downloadLink` should be cleared at the start of each download run.

### 15.8 Resource Path Strategy Is Not Fully Unified

`db.py` handles `sys.frozen`, placing the database under the executable directory when packaged.

`ConfigUtil` always resolves resources relative to the source file and does not handle `sys.frozen`. This should be unified before packaging the application.

### 15.9 Minor UI Typo

The main menu item `Settings` is currently spelled `Sttings`.

## 16. Suggested Maintenance Order

Recommended next steps:

1. Add `requirements.txt`.
2. Fix the Home page empty-input button state.
3. Add reliable exception handling and failure reporting to `DownloadThread`.
4. Fix Pixiv token storage and authentication failure behavior.
5. Unify resource path handling for development and packaged builds.
6. Replace download `print` calls with logging and GUI-visible status.
7. Add artwork-level or file-level database records if reliable resume behavior is needed.

## 17. Quick Run Reference

```bash
pip install PyQt6 pixivpy3 requests PyYAML
python main.py
```

Before the first download:

1. Open the Settings page.
2. Select a download directory.
3. Enter a Pixiv `refresh_token`.
4. Save the settings.
5. Return to the Home page and enter a `User ID` or `Artwork ID`.

This tool accesses and downloads Pixiv content. It should only be used for personal learning, research, or backup, and it should be used in compliance with Pixiv's Terms of Service.
