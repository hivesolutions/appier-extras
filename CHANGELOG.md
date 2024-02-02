# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

*

### Changed

*

### Fixed

*

## [0.25.1] - 2024-02-02

### Fixed

* Issue with `image_resize()` method - [#42](https://github.com/hivesolutions/appier-extras/issues/42)

## [0.25.0] - 2024-01-04

### Changed

* Renamed repository to `appier-extras`
* New year naming 2023
* Changed codebase to make it compliant with Black code formatter

### Fixed

* Issue with Pillow and the ANTIALIAS resampling constant

## [0.24.9] - 2022-10-22

### Fixed

* More flexible support for multiple recaptcha tokens

## [0.24.8] - 2022-08-02

### Fixed

* Removed nightly build from `.travis.yml`
* Recover password with link to return to the previous page instead of the sign in page

## [0.24.7] - 2022-05-02

### Added

* Lazy loading of image data

## [0.24.6] - 2022-05-02

### Added

* Support for resizing in the avatar routes

## [0.24.5] - 2021-12-26

### Added

* More debug information to logstash and loggly parts

## [0.24.4] - 2021-07-23

### Added

* Support for multiple child add and remove at the `Role` entity level

## [0.24.3] - 2021-07-01

### Fixed

* Issue related with bad list merging in `_join_m`

## [0.24.2] - 2021-06-28

### Added

* RIPE Compose library version loader

## [0.24.1] - 2021-05-22

### Added

* Support for `OAuthToken` patching upon change of username

## [0.24.0] - 2021-05-21

### Added

* Account impersonation support

## [0.23.9] - 2021-05-18

### Added

* Support for changing email of an account

## [0.23.8] - 2021-05-18

### Added

* Support for changing username of an account

## [0.23.7] - 2021-04-08

### Added

* More API endpoints

## [0.23.6] - 2021-03-23

### Added

* `get/find/count/paginate_ve` methods in `Base` model entity

## [0.23.5] - 2021-03-23

### Added

* Support for secrets in `Base` model entity
