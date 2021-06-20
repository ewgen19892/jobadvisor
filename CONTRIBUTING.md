# Contributing to JobAdvisor
The following is a set of guidelines for contributing to the project.

### Links to Important Resources:
#### Bugs:
* **Issue tracker [GitLab Issues](https://gitlab.fingers.by/jobadvisor/backend/issues)**
* **Error tracker [Sentry](https://sentry.fingers.by/fingers/jobadvisor-backend/)**
#### Docs:
* **OpenAPI [GitLab Pages](https://jobadvisor.pages.fingers.by/backend)**
#### Communications:
* **Slack [#jobadvisor](https://fingers-media.slack.com/messages/CH9K90STV)**

## Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers understand your report, reproduce the behavior, and find related reports.

Before creating bug reports, please check [this list](#before-submitting-a-bug-report) as you might find out that you don't need to create one. When you are creating a bug report, please [include as many details as possible](#how-do-i-submit-a-good-bug-report). Fill out [the required template](.gitlab/issue_templates/Bug.md), the information it asks for helps us resolve issues faster.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.


#### Before Submitting A Bug Report

* **Check if** you might be able to find the cause of the problem and fix things yourself. Most importantly, check if you can reproduce the problem in the latest version of app.
* **Determine which repository the problem should be reported**.
* **Perform a [cursory search](#bugs)** to see if the problem has already been reported. If it has **and the issue is still open**, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [Gitlab issues](https://gitlab.fingers.by/help/user/project/issues/index.md). After you've determined which repository your bug is related to, create an issue on that repository and provide the following information by filling in [the template](.gitlab/issue_templates/Bug.md).

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible.
> **Note:** It is not necessary to indicate the color of the cat that sits on your lap, but preferably.
* **Provide specific examples to demonstrate the steps**. Include links to files or Gitlab projects, or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue, use [Markdown code blocks](https://gitlab.fingers.by/help/user/markdown#code-and-syntax-highlighting).
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **If you have a GUI problem** include screenshots and animated GIFs which help you demonstrate the steps or point out the part of Atom which the suggestion is related to. You can use [this tool](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.
* **If you're reporting that app crashed**, include a crash report with a stack trace from the [error tracking system](#bugs) in the issue in a [code block](https://gitlab.fingers.by/help/user/markdown#code-and-syntax-highlighting).
* **If the problem is related to performance or memory**, include a [CPU profile capture](https://flight-manual.atom.io/hacking-atom/sections/debugging/#diagnose-runtime-performance) with your report.
* **If the problem wasn't triggered by a specific action**, describe what you were doing before the problem happened and share more information using the guidelines below.

Provide more context by answering these questions:

* **Did the problem start happening recently** or was this always a problem?
* **Can you reliably reproduce the issue?** If not, provide details about how often the problem happens and under which conditions it normally happens.
* If the problem is related to working with files (e.g. uploading or downloading), **does the problem happen for all files and projects or only some?** Does the problem happen only when working with files of a specific type (e.g. only images or text files), with large files or files with very long lines, or with files in a specific encoding? Is there anything else special about the files you are using?

Include details about your configuration and environment:

* **Which version of app are you using?** You can get the exact version from request header in your client, or by image tag.
* **If you have a GUI problem** What's the name and version of the client you're using?

## Merge Requests

The process described here has several goals:

- Maintain projects's quality
- Implement the planned features in the project
- Fix problems that are important to users

Please follow these steps to have your contribution considered by the maintainers:

1. Follow all instructions in [the template](.gitlab/merge_request_templates/Feature.md)
2. Follow the [styleguides](#styleguides)
3. Before you submit your pull request, verify that all [pipeline status](https://gitlab.fingers.by/help/ci/README.md) are passing 
<details>
<summary>What if the status checks are failing?</summary>
If a status check is failing, and you believe that the failure is unrelated to your
change, please leave a comment on the pull request explaining why you believe the
failure is unrelated. A maintainer will re-run the status check for you. If we
conclude that the failure was a false positive, then we will open an issue to track
that problem with our status check suite.
</details>

While the prerequisites above must be satisfied prior to having your pull request reviewed, the reviewer(s) may ask you to complete additional design work, tests, or other changes before your pull request can be ultimately accepted.

## Styleguides

### [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.3/)
The Conventional Commits specification is a lightweight convention on top of commit messages. It provides an easy set of rules for creating an explicit commit history; which makes it easier to write automated tools on top of. This convention dovetails with SemVer, by describing the features, fixes, and breaking changes made in commit messages.

The commit message should be structured as follows:
```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

#### Message rules:
The commit contains the following structural elements, to communicate intent to the consumers of your library:

1. **fix**: a commit of the type `fix` patches a bug in your codebase (this correlates with `PATCH` in semantic versioning).
2. **feat**: a commit of the type feat introduces a new feature to the codebase (this correlates with `MINOR` in semantic versioning).
3. **BREAKING CHANGE**: a commit that has the text `BREAKING CHANGE`: at the beginning of its optional body or footer section introduces a breaking API change (correlating with `MAJOR` in semantic versioning). A BREAKING CHANGE can be part of commits of any type.
4. Others: commit types other than fix: and feat: are allowed, for example [@commitlint/config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional) (based on the the Angular convention) recommends chore:, docs:, style:, refactor:, perf:, test:, and others.

We also recommend `improvement` for commits that improve a current implementation without adding a new feature or fixing a bug. Notice these types are not mandated by the conventional commits specification, and have no implicit effect in semantic versioning (unless they include a BREAKING CHANGE). 
A scope may be provided to a commit’s type, to provide additional contextual information and is contained within parenthesis, e.g.,

`feat(parser): add ability to parse arrays.`
