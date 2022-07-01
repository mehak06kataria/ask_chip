from __future__ import absolute_import
from django_mongoengine import fields

from hub.lib import parseRole
from hub.models import RPDocumentWithRole, RoleWithCompany
from common import DateField, on_change, on_change_patch_module, StrModelChoices

QUERYSTATE = StrModelChoices("RESOLVED", "NEW", "NO FIX YET" )
QUERYTYPE = StrModelChoices("PYCHARM_QUERIES", "FE_SUPPORT", "CLOUD_DEV_ENV", "BANGALORE", "EXEC", "INDIA_INTERNS",
                             "ALL_HANDS", "DOCUMENTATIONS", "MISCELLANEOUS")
QUERYSUBTYPE = StrModelChoices("PY_SETUP", "PY_ERRORS", "FE_FEATURE", "FE_ERROR", "CLOUD_DEV_ERRORS", "BANGALORE",
                               "EXEC", "INDIA_INTERNS", "ALL_HANDS", "DOCUMENTATIONS", "MISCELLANEOUS")
RESULT_IN_APPS = StrModelChoices("Slack", "Confluence", "Drive")

class AskChip(RPDocumentWithRole):
    query = fields.StringField()
    query_type = fields.StringField(choices=QUERYTYPE.choices(), blank=True)
    query_sub_type = fields.StringField(choices=QUERYSUBTYPE.choices(), blank=True)
    query_state = fields.StringField(choices=QUERYSTATE.choices(), blank=True)
    date = fields.DateTimeField(blank=True)
    # search_in = fields.StringField(choices=RESULT_IN_APPS.choices(),blank=True)
    #
    # if search_in == RESULT_IN_APPS[0]:
    #     search_private_channel = fields.BooleanField(default=False)
    #     search_direct_messages = fields.BooleanField(default=False)
    #     search_groups = fields.BooleanField(default=False)
    #
    # if search_in == RESULT_IN_APPS[1]:
    #     search_header = fields.BooleanField(default=False)
    #     search_content = fields.BooleanField(default=False)
    #     search_blogpost = fields.BooleanField(default=False)
    #     search_pages = fields.BooleanField(default=False)
    #     search_comments = fields.BooleanField(default=False)
    #     search_attachments = fields.BooleanField(default=False)
    #
    # if search_in == RESULT_IN_APPS[2]:
    #     search_header = fields.BooleanField(default=False)
    #     search_content = fields.BooleanField(default=False)
    #     search_sheet = fields.BooleanField(default=False)
    #     search_doc = fields.BooleanField(default=False)

    @classmethod
    def post_query(cls, role, query, query_type, query_sub_type, query_state, date):
        query_posted = AskChip(company = role.company, role = role, query = query, query_type = query_type,
                                          query_sub_type = query_sub_type, query_state = query_state.NEW, date = date)
        query_posted.save()
        return query_posted

    @classmethod
    def list_all_related_results(cls, request):
        role = parseRole(request)
        all_requests = AskChip.objects_across_company(company = role.company,
                                                      query_state = QUERYSTATE.RESOLVED).order_by('date')
        return all_requests

    @on_change(status=QUERYSTATE.NEW)
    def query_posted_notif_to_user(self):
        print("Query posted with ID " + str(self.id))
