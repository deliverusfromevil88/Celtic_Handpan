[app]
title = Celtic Handpan
package.name = celtic_handpan
package.domain = org.jason
source.dir = .
source.include_exts = py,png,jpg,wav
version = 0.1.0
orientation = landscape
fullscreen = 1
requirements = python3,kivy,ffpyplayer

# Architectures and Android toolchain settings
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.sdk = 33
android.ndk = 25b
# If Gradle/tooling mismatch errors occur, you can pin:
# android.gradle_plugin = 8.3.1
# android.gradle_version = 8.5

# Optional branding (uncomment and point to your files)
# icon.filename = assets/highlight.png
# presplash.filename = assets/handpan_layout.jpg

[buildozer]
log_level = 2
warn_on_root = 0



android.build_tools = 34.0.0
android.sdk_path = /root/.buildozer/android/platform/android-sdk
