[app]
# (str) Title of your application
title = VIP追剧神器

# (str) Package name
package.name = vipzhuiqi

# (str) Package domain (needed for android/ios packaging)
package.domain = org.vipfree

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.1,Pillow==10.0.1,requests

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 31

# (str) Android NDK version to use
android.ndk = 23b

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/icon.png

# (str) Supported interface languages. List of languages supported by the app.
# comma separated e.g. supported_languages = en,es
# supported_languages = en

# (str) Presplash background color (for android toolchain)
# you can use html color code like #RRGGBB
#android.presplash_color = #FFFFFF

# (str) Adaptive icon of the application
#android.adaptive_icon_background = #FFFFFF

# (str) Adaptive icon foreground of the application
#android.adaptive_icon_foreground = 

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa)
# bin_dir = ./bin

# -----------------------------------------------------------------------------#
# Additional configuration options for specific build steps
# -----------------------------------------------------------------------------#

# (str) The Android NDK directory to use
#android.ndk_path = 

# (str) The Android SDK directory to use
#android.sdk_path = 

# (str) ANT directory (if empty, it will be automatically downloaded)
#android.ant_path = 

# (bool) If True, then skip trying to update the Android SDK
# This can be useful to avoid excess Internet downloads or save time
# android.skip_update = False

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app bundle, default is apk
# android.release_artifact = aab

# (str) Python for android fork to use, defaults to upstream (kivy)
# p4a.fork = kivy

# (str) Python for android branch to use, defaults to master
# p4a.branch = master

# (str) Python for android git clone directory (if empty, it will be automatically cloned)
# p4a.source_dir = 

# (str) The directory in which python-for-android should look for your own build recipes (if any)
# p4a.local_recipes = 

# (str) Filename to the hook for p4a
# p4a.hook = 

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
# p4a.port = 

# (bool) Keep the original build target (debug/release) when an error occurs
# p4a.keep_build = False

# -----------------------------------------------------------------------------#
# Logs configuration
# -----------------------------------------------------------------------------#

# (str) Path to store the list of installed distribution packages
# distutils_cache = ~/.buildozer/cache/distutils

# (str) Path to store the list of installed app packages
# app_cache = ~/.buildozer/cache/app

# (str) Path to store the list of installed python packages
# python_cache = ~/.buildozer/cache/python