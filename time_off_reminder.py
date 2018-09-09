import datetime

from datetime import datetime
from dateutil.relativedelta import *
from project_team import ProjectTeam

SUBJECT = "Time Off Reminder - '{}'"


class TimeOffReminder:

    def __init__(self, project_team: ProjectTeam) -> None:
        self.team_name = project_team.name
        self.subject = SUBJECT.format(self.team_name)
        self.to = [report_to.email for report_to in project_team.reports]
        self.members = [member for member in project_team.members]

    def as_email(self):
        return self.subject, self.to, self.__format_time_offs_in_html(self.members, self.team_name)

    @staticmethod
    def __format_time_offs_in_html(members, team_name):

        content = TimeOffReminder.start_html(team_name)

        content_this_month = TimeOffReminder.start_a_month(datetime.now())
        content_next_month = TimeOffReminder.start_a_month(datetime.now() + relativedelta(months=1))

        for member in members:

            if member.time_offs:
                time_offs_this_month = member.get_time_offs_this_month()

                if time_offs_this_month:
                    for t in time_offs_this_month:
                        TimeOffReminder.add_time_off(content_this_month, t)
                else:
                    TimeOffReminder.no_time_off(content_this_month, member)

                time_offs_next_month = member.get_time_offs_next_month()

                if time_offs_next_month:
                    for t in time_offs_next_month:
                        TimeOffReminder.add_time_off(content_next_month, t)
                else:
                    TimeOffReminder.no_time_off(content_next_month, member)

            else:
                TimeOffReminder.no_time_off(content_this_month, member)
                TimeOffReminder.no_time_off(content_next_month, member)

        full_content = content + content_this_month + content_next_month
        TimeOffReminder.end_html(full_content)

        return ''.join(full_content)

    @staticmethod
    def no_time_off(content, employee):
        return content.append("""
        <tr>
        <td bgcolor="#ffffff" colspan="3"
            style="padding:0px 40px; border-left:solid #bebebe 1px; border-right:solid #bebebe 1px">

            <table border="0" cellpadding="0" cellspacing="0" style="margin-bottom:10px">
                <tbody>
                <tr>
                    <td style=""><img data-imagetype="External"
                                      src="{}"
                                      alt="" height="41" width="41"
                                      style="line-height:100%; text-decoration:none; outline:0; width:41px; height:41px; border:solid #898989 1px; margin-right:10px; display:block">
                    </td>
                    <td style="vertical-align:top">
                        <p style="margin-top: 0px; margin-bottom: 0px; font-family: Arial, Helvetica, san-serif, serif, EmojiFont; font-size: 14px; color: rgb(136, 136, 136); line-height: 15px;"><br>
                            {}<br>
                            <span style="color:#222222"></span><span
                                style="color:#548400; font-weight:600">{}</span>
                            </p>
                    </td>
                </tr>
                </tbody>
            </table>
        </td>
    </tr> 
        """.format(employee.photoUrl, "None", employee.fullname if employee.fullname else employee.email))

    @staticmethod
    def start_a_month(time_month):
        return ["""<tr><td style="padding:10px 40px; border-left:solid #bebebe 1px; border-right:solid #bebebe 1px" bgcolor="white">
           <p style="margin-top: 0px; margin-bottom: 0px; font-family: Arial, Helvetica, san-serif, serif, EmojiFont; font-size: 14px; color: #A3256A; line-height: 25px; font-weight:600">{}</p>
       </td></tr>""".format(time_month.strftime("%B"))]

    @staticmethod
    def add_time_off(content, time_off):
        content.append(time_off.to_html())

    @staticmethod
    def start_html(team_name):
        return ["""
        <html>       
<table class="main_container" cellpadding="0" cellspacing="0" style="background-color:#eee; max-width:520px; width: 100%;">
    <tbody>

    <!-- Title -->
    <tr>
        <td>
            <table class="title" border="0" cellpadding="0" cellspacing="0" style="background-color:#3a3a3a; height:68px; width:100%;">
                <tbody>
                <tr>
                    <td style="padding:0 20px">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tbody>
                            <tr>
                                <td style="padding-right:14px">
                                    <img data-imagetype="External"
                                         src="http://resources.bamboohr.com/images/emails/icons/pto-reminder.png"
                                         height="auto"
                                         style="line-height:100%; text-decoration:none; border:0; height:auto; outline:0">
                                </td>
                                <td width="100%"
                                    style="font-weight:700; color:#fff; font-size:24px; padding-top:2px; width:100%">
                                    Time Off Reminder - {0}
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                </tbody>
            </table>
        </td>
    </tr>
 
    <!-- border -->   
    <tr>
        <td style="">
            <table class="border" border="0" cellpadding="0" cellspacing="0" width="100%">
                <tbody>
                <tr>
                    <td bgcolor="#A3256A" height="4" id="x_brandbar" style="background-color:#A3256A; height:4px"></td>
                </tr>
                </tbody>
            </table>
        </td>
    </tr>
    
    <!-- Time offs -->    
   """.format(team_name)]

    @staticmethod
    def end_html(content):
        return content.append(
            """<!-- powered by commencis -->
            <tr>
            <td align="center" style="padding-bottom:5px">
            <table class="powered_by" border="0" cellpadding="0" cellspacing="0" width="518">
            <tbody>
            <tr>
                <td style="padding:8px 0 0 5px"></td>
                <td align="right" style="padding:7px 5px 0 0; font-family:'source sans pro',Helvetica,Arial,san-serif; font-size:11px; color:#888888">powered by commencis
                </td>
            </tr>
            </tbody>
        </table>
    </td>
</tr>
</tbody>
</table>
</html>""")
