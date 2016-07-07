# javascript quality




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
