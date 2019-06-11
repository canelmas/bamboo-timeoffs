from datetime import datetime

DATE_FORMAT_BAMBOO = "%Y-%m-%d"

STATUS_APPROVED = 'approved'
STATUS_REQUESTED = 'requested'
STATUS_ALLOWED = [STATUS_APPROVED, STATUS_REQUESTED]

LABEL_PENDING_APPROVAL = '(pending approval)'


class TimeOff:

    def __init__(self, data, employee_photo_url, employee_id) -> None:
        self.start = datetime.strptime(data['start'], DATE_FORMAT_BAMBOO)
        self.end = datetime.strptime(data['end'], DATE_FORMAT_BAMBOO)
        self.dates = data['dates']
        self.status = data['status']['status']
        self.amount = float(data['amount']['amount'])
        self.employee_name = data['name']
        self.status = data['status']['status']
        self.employee_photo_url = employee_photo_url
        self.employee_id = employee_id
        self.type = data['type']['name']

    def to_html(self):
        return """
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
                    <td style="">
                        <table cellpadding="0" cellspacing="0" height="43" width="43" style="border:solid #d1d1d1 2px">
                            <tbody>
                            <tr>
                                <td align="center" bgcolor="#ececec"
                                    style="text-transform:uppercase; color:#888888; font-family:Arial,Helvetica,san-serif; font-weight:700; font-size:11px">
                                    {}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" bgcolor="#ffffff" valign="middle"
                                    style="color:#acacac; font-family:Arial,Helvetica,san-serif; font-weight:700; font-size:20px">
                                    {}
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </td>
                    <td valign="middle" style="padding:0 6px 0 7px">
                        <img data-imagetype="External"
                             src="http://app.bamboohr.com/images/emails/icons/arrow-right.png"
                             alt="" height="auto" width="20"
                             style="line-height:100%; text-decoration:none; border:0; height:auto; outline:0">
                    </td>
                    <td style="">
                        <table cellpadding="0" cellspacing="0" height="43" width="43" style="border:solid #d1d1d1 2px">
                            <tbody>
                            <tr>
                                <td align="center" bgcolor="#ececec"
                                    style="text-transform:uppercase; color:#888888; font-family:Arial,Helvetica,san-serif; font-weight:700; font-size:11px">
                                    {}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" bgcolor="#ffffff" valign="middle"
                                    style="color:#acacac; font-family:Arial,Helvetica,san-serif; font-weight:700; font-size:20px">
                                    {}
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </td>
                    <td style="padding-left:9px; vertical-align:top">
                        <p style="margin-top: 0px; margin-bottom: 0px; font-family: Arial, Helvetica, san-serif, serif, EmojiFont; font-size: 14px; color: rgb(136, 136, 136); line-height: 15px;">
                            <a href="https://commencis.bamboohr.com/employees/employee.php?id={}&amp;utm_swu=6071" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable" style="display:inline-block; color:#006ec2; text-decoration:none">{}</a>
                            <span style="color:#e6ac00; font-weight:50; font-style:italic;">{}</span><br>
                            {}<br>
                            <span style="color:#222222"></span>
                            <span style="color:#548400; font-weight:600">{}</span>
                        </p>
                    </td>
                </tr>
                </tbody>
            </table>
        </td>
    </tr> 
        """.format(self.employee_photo_url,
                   datetime.strftime(self.start, "%B"),
                   datetime.strftime(self.start, "%d"),
                   datetime.strftime(self.end, "%B"),
                   datetime.strftime(self.end, "%d"),
                   self.employee_id,
                   self.amount,
                   LABEL_PENDING_APPROVAL if self.status != STATUS_APPROVED else "",
                   self.type,
                   self.employee_name)

    def is_passed(self):
        return datetime.now() > datetime(self.end.year, self.end.month, self.end.day, 23, 59, 59)

    def __str__(self) -> str:
        return "name={}, id={}, amount={}, status={} start={} end={}".format(self.employee_name,
                                                                             self.employee_id,
                                                                             self.amount, self.status,
                                                                             self.start,
                                                                             self.end)
