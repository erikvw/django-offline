from django.core.urlresolvers import reverse
from django.db import models

from edc_base.model.models import BaseUuidModel

from edc_sync import transaction_producer


class BaseTransaction(BaseUuidModel):

    tx = models.TextField(
        max_length=500,
        help_text='stores secret bytes as a b64 encoded string'
    )

    tx_name = models.CharField(
        max_length=64,
        db_index=True,
    )

    tx_pk = models.UUIDField()

    tx_modified = models.DateTimeField()

    producer = models.CharField(
        max_length=75,
        default='producer',  # transaction_producer.transaction_producer,
        null=True,
        help_text='Producer name',
    )

    action = models.CharField(
        max_length=1,
        default='I',
        choices=(('I', 'Insert'), ('U', 'Update'), ('D', 'Delete')),
    )

    timestamp = models.CharField(
        max_length=50,
        null=True,
        db_index=True,
    )

    consumed_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )

    consumer = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        db_index=True,
    )

    is_ignored = models.BooleanField(
        default=False,
        help_text='Ignore if update'
    )

    is_error = models.BooleanField(
        default=False,
    )

    error = models.TextField(
        max_length=1000,
        null=True,
        blank=True,
    )

    batch_seq = models.IntegerField(null=True, blank=True)

    batch_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{0} {1} {2}'.format(self.tx_name, self.producer, self.action)

    def render(self):
        url = reverse(
            'view_transaction_url',
            kwargs={'model_name': self._meta.object_name.lower(), 'pk': self.pk}
        )
        ret = ('<a href="{url}" class="add-another" id="add_id_report" onclick="return '
               'showAddAnotherPopup(this);"> <img src="/static/admin/img/icon_addlink.gif" '
               'width="10" height="10" alt="View transaction"/></a>'.format(url=url))
        return ret
    render.allow_tags = True

    class Meta:
        abstract = True