[app]
title = Ball Dodge Game
package.name = balldodge
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
# Buildozer reads Android settings from the [app] section.
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True
