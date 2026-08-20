"""Query GraphQL da coleta dos repositórios mais populares."""

from __future__ import annotations

TOP_REPOS_QUERY = """
query TopRepos($searchQuery: String!, $first: Int!, $after: String) {
  search(
    query: $searchQuery
    type: REPOSITORY
    first: $first
    after: $after
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        nameWithOwner
        stargazerCount
        createdAt
        pushedAt
        primaryLanguage { name }
        pullRequests(states: MERGED) { totalCount }
        releases { totalCount }
        closedIssues: issues(states: CLOSED) { totalCount }
        openIssues:   issues(states: OPEN)   { totalCount }
      }
    }
  }
  rateLimit {
    cost
    remaining
    resetAt
    limit
  }
}
"""
