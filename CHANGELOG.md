# Changelog

All notable changes to this project will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project attempts to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.3.0](https://github.com/engineervix/garmin-activity-share/compare/v0.2.0...v0.3.0) (2023-08-20)


### 📝 Docs

* fix errors in CONTRIBUTION guide ([5760632](https://github.com/engineervix/garmin-activity-share/commit/5760632e65e60b2443cb731f24e01fa6c6a42e6d))


### 🐛 Bug Fixes

* use updated URL for flake8 hook ([6a219a3](https://github.com/engineervix/garmin-activity-share/commit/6a219a3ce8416c068eba30b518978411cde03573))


### ⚙️ Build System

* **deps-dev:** update redis docker tag to v7.2 ([a07438d](https://github.com/engineervix/garmin-activity-share/commit/a07438da267f70be5d52d5547435170bc3c63e37))
* **deps:** bump pip-tools and tweepy ([4d8fb28](https://github.com/engineervix/garmin-activity-share/commit/4d8fb28f51b6211f9e44b1427926911498ec127c))


### 🚀 Features

* use v2 of the twitter API for posting tweets ([8f810c2](https://github.com/engineervix/garmin-activity-share/commit/8f810c2f777b974318781061a587bfbf750f2e57))

## [v0.2.0](https://github.com/engineervix/garmin-activity-share/compare/v0.1.0...v0.2.0) (2022-12-30)


### 🚀 Features

* save last activity data to REDIS instead of a JSON file ([3f777d1](https://github.com/engineervix/garmin-activity-share/commit/3f777d11003097344b0b19024220501376badffa))


### ♻️ Code Refactoring

* add docker-compose related invoke tasks ([ecf487e](https://github.com/engineervix/garmin-activity-share/commit/ecf487ebeca5cfd92d2a191743fa0a9ded9fa4d9))
* add REDIS_URL and MODE to env variables ([7b32874](https://github.com/engineervix/garmin-activity-share/commit/7b328749479db3b0b7c2487a24bfe1bc3d2f3d28))


### 👷 CI/CD

* add REDIS service to Github Actions ([60b88f5](https://github.com/engineervix/garmin-activity-share/commit/60b88f51efcc96746e4ed82a0359a76f6777d76b))
* update GitHub Actions ENV Variables ([9e54131](https://github.com/engineervix/garmin-activity-share/commit/9e54131cb25360bfc9bf50d2d891724ff6998c06))


### 🐛 Bug Fixes

* remove comment from JSON file ([1cc0daf](https://github.com/engineervix/garmin-activity-share/commit/1cc0daf4b245cd1c425412da8cdc513dc607f3fb))


### ⚙️ Build System

* add `app.json` as part of Dokku deployment setup ([ab576fb](https://github.com/engineervix/garmin-activity-share/commit/ab576fb651f4b2b57e653a602113ab5eb08e6a9b))
* **deps:** move colorama from dev to base ([0fcaa01](https://github.com/engineervix/garmin-activity-share/commit/0fcaa012d550b98af069a360b34f57a29227bc1c))
* **deps:** move tomli from dev.in to base.in ([4bb8ae0](https://github.com/engineervix/garmin-activity-share/commit/4bb8ae060f784c20ffbe61f16d1bb833525517b0))
* dockerize the app ([ea3df00](https://github.com/engineervix/garmin-activity-share/commit/ea3df00476c327bc8825b1161ebf34cefffc25cd))
* install redis and re-organise dependencies ([4d44778](https://github.com/engineervix/garmin-activity-share/commit/4d44778de00685ca5451047c8d6b78f79815bab1))
* set timezone in `Dockerfile` to Africa/Lusaka ([1c79cf0](https://github.com/engineervix/garmin-activity-share/commit/1c79cf000658ded77556dd07a68bb3d512155ace))


### 💄 Styling

* remove extra whitespace in base.in ([3b0cd3d](https://github.com/engineervix/garmin-activity-share/commit/3b0cd3d13b1c62928b330abe2227375407a8d536))


### 📝 Docs

* add a TODO item to save sessions to REDIS ([a8136d1](https://github.com/engineervix/garmin-activity-share/commit/a8136d1d0014dcfaa551ad018ef529ddbc1b171c))
* rewrite README to include updated setup instructions ([e2ecf0d](https://github.com/engineervix/garmin-activity-share/commit/e2ecf0dfa080a90038362bf3957b5028b821cbec))

## [v0.1.0](https://github.com/engineervix/garmin-activity-share/compare/v0.0.0...v0.1.0) (2022-12-30)


### 🚀 Features

* add sample DotENV file ([7479913](https://github.com/engineervix/garmin-activity-share/commit/74799130c9ba8b7d3c6a1e87b0e582b76ad1cb1a))
* add some assets (fonts & images) to work with ([65c90c3](https://github.com/engineervix/garmin-activity-share/commit/65c90c3f27199bc0aea363e3325ade1ba0310f91))
* write scripts to perform 3 actions: connect, draw, tweet! ([6c0371a](https://github.com/engineervix/garmin-activity-share/commit/6c0371a386fb58e30e31402970529168aae39ff5))


### ♻️ Code Refactoring

* update invoke tasks ([248ddd2](https://github.com/engineervix/garmin-activity-share/commit/248ddd2df92da00b782677a47f39b80a93d03d86))


### ⚙️ Build System

* **deps:** specify required dependencies ([b72a22a](https://github.com/engineervix/garmin-activity-share/commit/b72a22ab4ff2fae981904dc2283e86db7e75e292))
* **deps:** update renovate config ([8a2d333](https://github.com/engineervix/garmin-activity-share/commit/8a2d333d27dff10640e3c1b3d9d34e36e16530a5))


### ✅ Tests

* remove sample test and add a simple test to get started ([a2744d0](https://github.com/engineervix/garmin-activity-share/commit/a2744d030c7ec8debe0fe1aca2ed9a884332bd88))


### 👷 CI/CD

* add missing environment variables to GitHub Actions config ([775f135](https://github.com/engineervix/garmin-activity-share/commit/775f135a818e2aeeb2996132a491fbf54d712c69))


### 📝 Docs

* update README with some meaningful info ([628873f](https://github.com/engineervix/garmin-activity-share/commit/628873f01f9c3d03c9a1afb892492b90a0c7c1a3))
