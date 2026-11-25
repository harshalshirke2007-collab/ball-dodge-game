# Ball Dodge Game — Android project

This project adapts the uploaded Pygame Ball Dodge game to Kivy so it can be packaged as an Android APK. The original left/right keyboard controls are replaced with touch controls:
- Touch/hold the left half of the screen to move left.
- Touch/hold the right half to move right.
- After game over, tap anywhere to restart.

## Build the APK

Buildozer is best run on Linux (Ubuntu or WSL2 on Windows). Install the system dependencies required by the current Buildozer documentation, then:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install buildozer cython
buildozer android debug
```

The first build downloads the Android SDK/NDK and may take a while. The APK is normally created under `bin/`.

For a release APK, configure signing before using `buildozer android release`.

## Notes
- This is a Kivy adaptation of the supplied Pygame source, not a direct binary conversion.
- Test on an Android device/emulator and adjust the package domain before publishing.
- The current build configuration targets 64-bit ARM Android devices.
