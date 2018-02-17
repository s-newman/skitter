# How do I add code to Skitter?
Here's how you do it!

## Issues
Before writing up a new feature, you should create an issue for it with the
proper tags, and a complete description of the feature.  Here are the tags that
can be applied:
- **Epic** - This issue is an epic.  Epics can be closed when all their
  required issues and bugs have been closed.
- **Feature** - This issue relates to the implementation of a specific feature.
  This issue can be closed once the feature has been implemented.
- **Test** - This issue relates to the implementation of a test for a specific
  feature.  The development of the test and any related bug fixes as the test
is developed should be included in this issue.  This issue can be closed once
the feature has been added to Travis CI and is passing.
- **Security** - This issue relates to the hardening of a feature against a
  specific type of attack.  A script should be written to make multiple
different attack attempts against the feature.  The development of this script
and all related hardening modifications should be included in this issue.  This
issue can be closed once the script has been added to Travis CI and is passing.
Passing in this case is defined as resisting all attempted attacks.
- **Bug** - This issue relates to a bug found through testing outside of any
  other features.  Bug issues should be created on an as-needed basis, and
added to a relevant epic if possible.  Modifications of microservices and tests
\- as well as the creation of any new tests (if needed) - that relate to fixing
  the bug should be included in this issue.  This issue can be closed when the
bug is fixed and all relevant tests are passing in Travis CI.

In addition to being tagged with one of the above labels, one of the following
labels must be applied to each feature, test, and security issue:
- **Required** - This issue is required as part of the project write up.
- **Enhancement** - This issue is not required as part of the project write up,
  and is an optional extra undertaking if there is additional time.  Note that
there may be open enhancements when the project is submitted - this represents
additional features that may be added to future releases.

## Branches
Specific branches have been set up for various purposes.  Please use these
branches appropriately.
- `master` - Stable, tested code.  Only release versions and hotfixes are
  merged with `master`.
- `dev` - Branched from `master`, contains completed but unstable features.
  Bugfixes and features are merged with `dev`.  Once `dev` is stable, it should
be merged with `master`.
  - Will need to be rebased when/if hotfixes are applied directly to `master`.
- "Feature" branches - Branched from `dev`, these branches contain code for a
  specific feature/issue in development.  Merged with `dev` when feature is
implemented.
  - Will need to rebase feature branches before merging with dev to help
    resolve merge conflicts
  - Should be based on individual "feature" issues
  - Names don't have to include the relevant issue name, but should be named
    appropriately.
  - Pull/merge requests should include the name(s) and number(s) of the
    issue(s) resolved by the branch.
- "Bugfix" branches - Branched from `dev` (or, in the case of a hotfix,
  `master`), works to fix a specific bug in implemented features
  - Should be based on individual "bug" issues
  - Names don't have to include the relevant issue name, but should be named
    appropriately.
  - Pull/merge requests should include the name(s) and number(s) of the
    issue(s) resolved by the branch.
