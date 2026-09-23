# Security policy

CSFB has no network service and does not process audio. Please report security issues privately to the repository maintainers rather than posting exploitable details publicly.

The optional external engine adapter starts the configured subprocess and sends it local benchmark text. That command executes arbitrary local code with the current user's permissions. The runner is not a sandbox. Only run trusted engine commands and datasets.
