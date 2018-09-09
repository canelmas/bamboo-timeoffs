from base_api import BaseApi


class TempoApi(BaseApi):

    def __init__(self, base_url, basic_auth_token) -> None:
        super().__init__(base_url, None, basic_auth_token)

    def get_all_teams(self):
        return self.get("/tempo-teams/1/team")

    def get_all_teams_and_filter(self, func):
        return list(filter(func, self.get("/tempo-teams/1/team")))

    def get_team(self, team_id):
        return self.get("/tempo-teams/1/team/{}".format(team_id))

    def get_team_members(self, team_id):
        return self.get("/tempo-teams/2/team/{}/member".format(team_id))
