from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import list_route, api_view
from rest_framework.response import Response
from app.ask_chip.models import AskChip
from ask_chip.applications.confluence_operations import ConfluenceOperations
from ask_chip.applications.drive_operations import DriveOperations
from ask_chip.applications.slack_operations import SlackOperations
from ask_chip.search.search_results_reordering import SearchResultsUpdater
from ask_chip.serializers import AskChipSerializer
from ask_chip.utils import preprocess_query

from hub.api import RPModelViewSet
from hub.lib import parseRole, parseRoleOrRaise
from ask_chip.search.search_handler import SearchHandler


class AskChipViewSet(RPModelViewSet):
    model = AskChip

    @login_required
    @api_view(["GET"])
    def get_confluence_result(self, request):
        role = parseRoleOrRaise(request)
        pass

    @login_required
    @api_view(["GET"])
    def get_slack_result(self, request):
        role = parseRoleOrRaise(request)
        pass

    @login_required
    @api_view(["GET"])
    def get_drive_result(self, request):
        role = parseRoleOrRaise(request)
        pass

    @login_required
    @api_view(["GET"])
    def get_email_result(self, request):
        role = parseRoleOrRaise(request)
        pass

    @login_required
    @api_view(["POST"])
    def post_query(self, request):
        role = parseRoleOrRaise(request)
        query = request.data.get("query")
        query_type = request.data.get("query_type")
        query_sub_type = request.data.get("query_sub_type")
        date = request.data.get("date")

        query_posted = AskChip.post_query(role = role, query = query, query_type = query_type,
                                          query_sub_type = query_sub_type, date = date)

        return Response(query_posted)

    @login_required
    @api_view()
    def list_all_related_results(self, request):
        all_requests = AskChip.list_all_related_results(request)
        serializer = AskChipSerializer(instances = all_requests, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchHandlerViewSet(RPModelViewSet):
    model = SearchHandler

    def get_result(self, query, is_error=False):
        if is_error:
            query =  preprocess_query(query)
        slack_results = SlackOperations().search_text(query=query)
        drive_results = DriveOperations().search_text(query=query)
        confluence_results = ConfluenceOperations().search_text(query=query)
        arranged_results = SearchResultsUpdater(query).get_ordered_contexts(slack_results, drive_results, confluence_results)
        return JsonResponse({"results": arranged_results})
