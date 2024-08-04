from dataclasses import dataclass
from typing import Tuple


@dataclass
class InstagramBotConfiguration():
    """InstagramBotConfiguration: The configuration for the Instagram bot."""
    posting_interval: str
    """str: This is the cron job used to post to the platform."""

    follow_for_follow: bool
    """bool: If the bot should follow for follow."""

    follow_interval: str
    """str: The cron schedule for when it should do it's follow for follow actions"""

    follow_limit: Tuple[int, int]
    """Tuple[int, int]: The minimum and maximum number of users the bot should follow. On Each iteration, the bot will follow a random number of users between the minimum and maximum."""

    reply_to_comments: bool
    """bool: If the bot should reply to comments."""

    reply_interval: str
    """str: The cron schedule for when it should reply to comments."""

    reply_limit: Tuple[int, int]
    """Tuple[int, int]: The minimum and maximum number of comments the bot should reply to. On Each iteration, the bot will reply to a random number of comments between the minimum and maximum."""

    self_like: bool
    """bool: If the bot should like its own posts, right after posting!"""

    comment_dm_promotion: bool
    """bool: If the bot should comment on other posts, to try and get a promotion in DM's"""

    comment_dm_promotion_interval: str
    """str: The cron schedule for when it should do self dm promotions."""

    comment_dm_promotion_limit: Tuple[int, int]
    """Tuple[int, int]: The minimum and maximum number of comments the bot should make to try and get a promotion in DM's. On Each iteration, the bot will comment on a random number of posts between the minimum and maximum."""

    cron_job_posting_interval: int = None
    """int: The cron-job.org jobId"""
