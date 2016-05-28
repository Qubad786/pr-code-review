from django.shortcuts import render
from django.views.generic import View
from github import Github
from web.utils.pullrequest_utils import (
    get_mentions_from_body_and_issue_comments,
    get_reviewers
)


class PullRequestView(View):
    template_name = 'pullrequest/pull_request.html'

    def get(self, request):
        github = Github(request.user.access_token)
        edx_platform_repository = github.get_user(login='edx').get_repo('edx-platform')
        pr_map = {}

        try:
            pr_number = int(request.GET.get('pull_request_number'))
            pull_req = edx_platform_repository.get_pull(pr_number)
            issue_comments = pull_req.get_issue_comments()
            review_comments = pull_req.get_review_comments()
            pull_request_body = pull_req.body
            mentions = get_mentions_from_body_and_issue_comments(pull_request_body, issue_comments)

            pr_map[pr_number] = dict(
                title=pull_req.title,
                owner=pull_req.user.login,
                created_at=pull_req.created_at,
                updated_at=pull_req.updated_at,
                reviewers=get_reviewers(mentions, pull_request_body, issue_comments, review_comments),
            )

            response = render(
                request,
                template_name=self.template_name,
                context=dict(pr_data=pr_map, mentions=mentions)
            )
        except ValueError:
            response = render(
                request,
                template_name='web/dashboard.html',
                context=dict(error='Invalid Number! Please enter valid PR#.')
            )
        except Exception as ex:
            response = render(
                request,
                template_name='web/dashboard.html',
                context=dict(error=ex.data['message'])
            )

        return response
