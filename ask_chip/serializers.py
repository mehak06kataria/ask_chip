from hub.serializers import RPDocumentSerializer
from ask_chip.models import AskChip


class AskChipSerializer(RPDocumentSerializer):
    class Meta:
        model = AskChip
        fields = ('query', 'query_type', 'query_sub_type', 'query_state', 'date')
