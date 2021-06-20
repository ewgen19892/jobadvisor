# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [1.0.3] 2019-09-05
## Fixed
- Send messages
- Variant weight

### [1.0.2] 2019-09-04
## Fixed
- Firebase service worker

### [1.0.1] 2019-09-04
## Changed
- Admin panel
## Added
- Notification to admin panel
- Integrated documentation
## Fixed
- Comment notification

### [1.0.0] 2019-09-02
## Added
- Ordering for messages from notification

### [0.3.5] 2019-08-27
### Fixed
- Remove cyrillic from email

### [0.3.4] 2019-08-23
## Added
- Filter vacancy by level
## Changed
- Filters
## Fixed
- Validators from company serializer

### [0.3.3] 2019-08-21
## Added
- `is_best` parameter and filter to Company
- `experience_gte` and `experience_lte` filter to Vacancy
- Notifications app
## Changed
- Profile completion rules
## Fixed
- Date validation

### [0.3.2] 2019-08-16
### Added
- Add ordering to vacancies
- Add ordering to reviews
- Add ordering to interviews
### Security
- Setup with `check --deploy`

## [0.3.1] 2019-08-14
### Added
- `works_in` for User
### Changed
- Add `position`, `started_at` and `finished_at` to Review

## [0.2.4] 2019-08-13
### Added
- Delete vacancy after 30 days
- `is_trial` to subscription
- delete vacancies if the company has a trial subscription at the time of its termination
### Fixed
- Remove from top Reviews & Vacancies

## [0.2.3] 2019-08-12
### Added
- Added pages entry point
### Changed
- Replace email with user object at the invite entry point

## [0.2.2] 2019-08-09
### Fixed
- Review admin page

## [0.2.1] 2019-08-08
### Fixed
- User level for invited user
### Updated
- Replace `is_hiring` with `is_best` in Review object and filter

## [0.1.18] 2019-08-07
### Fixed
- User password after registration
- Third level for employee
### Added
- Add `is_responded` parameter to Vacancy
### Updated
- Prepair celery entrypoint 

## [0.1.17] 2019-08-06
### Updated
- Replace user id with User object in Company workers field
### Added
- `has_report` to review and interview serializers.
- Button `View on site` for the report of the admin page with a link to the content object
- Reports for review and interview on the admin page

## [0.1.16] 2019-08-02
### Updated
- Send emails from queue
- Pagination for followers list
- Replace level 3 with 2 in Followers Permission
### Added
- Notification for employer
- Notification for employee
- `is_deleted` filter for vacancies
- `is_hiring` to Review
- Review/Interview filtering by owner is me
- Invite user to JobAdvisor
- Search user by email, first and last name

## [0.1.15] 2019-07-23
### Updated
- rename `companies` with `company` in company relation and add company id to user serializer
- rename FAQ role with level
- Transform position ID to object in the Interview
### Added
- `is_created` for convert token serializer

## [0.1.14] 2019-07-17
### Updated
- Add active subscription to company for employee
- Replace institute id with Institute object in Education
- URL in password reset email
- Filter jobs by owner & hide job salary
### Fixed
- Search filter in vacancies
- Variant validation in admin panel

## [0.1.13] 2019-07-11
### Added
- User to token
- Level to Advantage
### Updated
- Upload user photo from SN
### Fixed
- Trial subscription

## [0.1.12] 2019-07-04
### Updated
- Activation URL in email
- Replace skills ids with Skill objects in Resume
- Replace owner, position and company ids with appropriate objects

## [0.1.11] 2019-06-25
### Added
- User to token serializer
- helpful count to review and interview
### Updated
- Owner validation to company admin

## [0.1.10] 2019-06-20
### Added
- ID to FAQ serializer
- Rewritable user level
- Company owner and workers validation

## [0.1.9]  2019-06-17
### Fixed
- CORS on prod

## [0.1.8]  2019-06-17
### Added
- Contact us entry point
- FAQ category ID to serializer
### Updated
- Transform position ID to object in the Vacancy
- Transform industry ID to object in the Company
- Transform company ID owner ID to objects in the Interview
- Transform company ID owner ID to objects in the Review

## [0.1.7] 2019-06-05
### Added
- Sort company by rating
- `is_hiring` parameter and filter to `Vacancy`
- `created_at` to `Intreview` and `Review`
- `has_offer`, `is_anonymous`, `complication`, `experience` and `position` filter parameters to `Intreview`
- Metrics entry point and logger
- Advantages entry point
### Updated
- Poll result serializer
- Requires the resume to add a response

## [0.1.6] 2019-05-28
### Added
- Salary entry point
### Updated
- Allowed to read these models for unauthorized users: `answer`, `category`, `companies`, `educations`, `faq`, `institutes`, `interview`, `jobs`, `qa`, `question`, `resumes`, `review`, `salaries`, `skills`, `users`, `variant`

## [0.1.5] 2019-05-23
### Added
- Authentication with google
- Localization

## [0.1.4] 2019-05-22
### Added
- Authentication with facebook
### Updated
- Working with CORS
- Search by vacancies, reviews and interviews
- Disable company owner change
- Vacancy soft-delete

## [0.1.3]
### Created
- Subscriptions for companies
- Pagination
- Helpful entry point for reviews and interviews
- `landing` app
### Updated
- Add `started_at` and `finished_at` fields to the Review
- Mixins in almost all views
- Optional fields in `Interview`
- Permissions
- Add Q&A to `InterviewSerializer`
- Creating comments and reports
- Profile completion behavior
- OpenAPI documentation

## [0.1.2]
### Updated
- Enable company owner editing
- Add `profile_completion` parameter to User
- OpenAPI documentation
### Created
- `reviews` app
- `polls` app
### Deleted
- Delete `karma` from models
- Disable users and companies creation on admin panel

## [0.1.1] 2019-04-25
### Created
- Users app
- Companies app
- Contrib features
