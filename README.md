# javascript quality

## Project structure
- folder `jupyter` contains jupyter notebooks used to analyze the data
- folder `sources` contains scripts used to load the data from various sources
- folder `sripts` contains helper scripts to manage the project


## To reproduce this experiment

### Following dependencies
- Postgresql 9.5
- Python 3.5



# Github Archive

## Event types
in more details https://developer.github.com/v3/activity/events/types/#pushevent

type | explanation
------------ | -------------
DeleteEvent | Represents a deleted branch or tag.
PullRequestReviewCommentEvent | Triggered when a comment on a Pull Request's unified diff is created, edited, or deleted (in the Files Changed tab).
GollumEvent | Triggered when a Wiki page is created or updated.
ForkEvent | Triggered when a user forks a repository.
PublicEvent | Triggered when a private repository is open sourced. Without a doubt: the best GitHub event.
IssueCommentEvent | Triggered when an issue comment is created, edited, or deleted.
PushEvent | Triggered when a repository branch is pushed to. In addition to branch pushes, webhook push events are also triggered when repository tags are pushed.
CreateEvent | Represents a created repository, branch, or tag.
PullRequestEvent | Triggered when a pull request is assigned, unassigned, labeled, unlabeled, opened, edited, closed, reopened, or synchronized.
IssuesEvent | Triggered when an issue is assigned, unassigned, labeled, unlabeled, opened, edited, closed, or reopened.
CommitCommentEvent | Triggered when a commit comment is created.
ReleaseEvent | Triggered when a release is published.
WatchEvent | The WatchEvent is related to starring a repository, not watching.
MemberEvent | Triggered when a user is added as a collaborator to a repository.


## Sources

Data sources for more information

- https://github.com/npm/download-counts -> getting download counts for particular package
- http://registry.npmjs.org/-/all -> returns all packages on NPM roughly 250 000 and size of the json is 175 mbs
- http://registry.npmjs.org/{package-name} -> returns json for specific package
- http://npm-stat.com -> has download stats about packages, probably just UI built on top of https://github.com/npm/download-counts
- http://www.npm-stats.com -> same as above
- github API -> contains metadata about packages
- github archive


## Data -> Source
List of what I have been able to get so far
- [x] stargazers count -> github API
- [x] forks count -> github API
- [x] open issues count -> github API
- [x] size -> github API
- [x] subsribers count -> github API
- [x] number of dependencies -> npm API
- [x] mainteners counter -> npm API
- [x] contributors counter -> npm API
- [x] has readme -> npm API
- [ ] has stable release -> npm API
- [x] has tests -> npm API
- [x] downloads count -> npm download API
- [ ] has linter -> ?
- [ ] code complexity -> ?
- [ ] issues, how fast they are attended and closed -> github archive
- [ ] commits, frequency and size -> github archive
