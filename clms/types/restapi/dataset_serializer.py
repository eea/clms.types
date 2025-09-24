"""Custom serializer for DataSet content type to exclude sensitive fields."""

from clms.types.content.data_set import IDataSet
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.serializer.dxcontent import SerializeToJson
from plone.dexterity.utils import iterSchemata
from plone.autoform.interfaces import READ_PERMISSIONS_KEY
from plone.supermodel.utils import mergedTaggedValueDict
from zope.interface import Interface, implementer
from zope.component import adapter
from zope.schema import getFields


@implementer(IFieldSerializer)
@adapter(IDataSet, Interface)
class DataSetSerializer(SerializeToJson):
    """Custom serializer for DataSet content that excludes sensitive fields."""

    def __call__(self, version=None, include_items=True):
        """Serialize the DataSet content, excluding sensitive fields."""
        # Call the parent serializer to get the default serialization
        result = super().__call__(version=version, include_items=include_items)

        version = "current" if version is None else version
        obj = self.getVersion(version)

        for schema in iterSchemata(self.context):
            read_permissions = mergedTaggedValueDict(
                schema, READ_PERMISSIONS_KEY)

            for name, _ in getFields(schema).items():
                if not self.check_permission(read_permissions.get(name), obj):
                    result[name] = None
                    continue

        return result
