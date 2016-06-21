##  These are the utils used by pullrequest django application ##

import re

# thumbs up and github username regex expression
thumbs_up = re.compile(u'(:\+1:|\U0001f44d)')
github_mention_regex = re.compile(r'\B@([a-z0-9](?:-?[a-z0-9]){0,38})')

def get_reviewers(mentions, pull_request_body, issue_comments, review_comments):
    """
    Returns the reviewers_mapping containing the information about the time
    when each of the reviewer was tagged, responded for the first time and
    gave thumbs up.
    :param mentions: mentions on pull request.
    :param pull_request_body: body of pull request.
    :param issue_comments: comments on pull request.
    :param review_comments: comments on pull request diffs.
    :return:
    {
        'reviewer_login':{
                'tagged_at': '',
                'responded_at': '',
                'gave_thumbs_up_at': '',
        }
            ...
    }
    """
    reviewers_mapping = {}

    # Reviewers are supposed to be those mentions who have given thumbs up.
    for comment in issue_comments:
        if comment.user.login in mentions and bool(thumbs_up.search(comment.body)):
            reviewers_mapping[comment.user.login] = dict(
                tagged_at=None,
                responded_at=None,
                gave_thumbs_up_at=comment.created_at
            )

    # We have reviewers, now, look for the time for their first response in issue comments.
    for comment in issue_comments:
        if comment.user.login in reviewers_mapping.keys() \
                and reviewers_mapping[comment.user.login]['responded_at'] is None:
            reviewers_mapping[comment.user.login]['responded_at'] = comment.created_at

        # TODO: Scrap the time when the PR's body was updated.
        # Story behind: Mostly, people just create the PR and update their body with description and reviewers
        # once the PR is ready for the review. Unfortunately, github v3 api dont have end point for knowing the
        # time when the PR's body was updated. So, most likely, we will not get precise 'tagged_at' attribute
        # for the reviewers that are in PR's body.

        # Look for time when each of reviewer was tagged, this should be
        # searched in pull request body and issue comments.
        for login in reviewers_mapping.keys():
            if login in comment.body and reviewers_mapping[login]['tagged_at'] is None:
                if reviewers_mapping[login]['responded_at'] is None \
                        or reviewers_mapping[login]['responded_at'] > comment.created_at:
                    reviewers_mapping[login]['tagged_at'] = comment.created_at

    # Check for reviewers' first response in review comments too, and
    # update the reviewers_mapping if necessary.
    for comment in review_comments:
        if comment.user.login in reviewers_mapping.keys():
            if reviewers_mapping[comment.user.login]['responded_at'] is None:
                reviewers_mapping[comment.user.login]['responded_at'] = comment.created_at
            elif reviewers_mapping[comment.user.login]['responded_at'] > comment.created_at:
                reviewers_mapping[comment.user.login]['responded_at'] = comment.created_at

    return reviewers_mapping


def get_mentions_from_body_and_issue_comments(pull_request_body, pull_request_comments):
    """
    Returns a set containing all the unique mentions in given pull request
    :param pull_request_body: body of pull request.
    :param pull_request_comments: comments on pull request.
    :return: set containing mentions.
    """
    unique_mentions = set()
    unique_mentions.update(github_mention_regex.findall(pull_request_body))
    for comment in pull_request_comments:
        unique_mentions.update(github_mention_regex.findall(comment.body))

    return unique_mentions
