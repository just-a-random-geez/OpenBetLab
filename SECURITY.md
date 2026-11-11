# Security Policy

## Supported versions

OpenBetLab is at an early stage. Only the latest release receives fixes.

| Version | Supported |
| ------- | --------- |
| 0.1.x   | Yes       |

## What makes this project low-risk by design

- It has **no runtime dependencies** beyond the Python standard library.
- It makes **no network connections**.
- It does **not** handle money, accounts, passwords or API keys.
- Its only data file is bundled, synthetic and contains no personal data.

Please help keep it that way: changes that add network access, credentials or
personal data are out of scope (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## Reporting a vulnerability

> **Maintainer note:** GitHub's private reporting is switched OFF by default.
> It must be enabled once in the repository under
> **Settings → Code security → Private vulnerability reporting**, otherwise
> the button described below does not appear.

**Please do not report security problems in a public issue.**

Instead, use GitHub's private reporting: open the repository's **Security**
tab and choose **Report a vulnerability**. Please include:

- a description of the problem and its possible impact;
- the steps to reproduce it;
- the OpenBetLab version and Python version you used.

We aim to acknowledge reports within 7 days and to keep you informed while we
work on a fix. We are happy to credit you once the fix is released, unless you
prefer to remain anonymous.

## Secrets

Never commit passwords, API keys or tokens to this repository, not even in
examples. OpenBetLab does not need any.
