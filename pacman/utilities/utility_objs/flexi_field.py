from enum import Enum

SUPPORTED_TAGS = Enum(
    value="SUPPORTED_TAGS",
    names=[("APPLICATION", 0),
           ("ROUTING", 1)])


class FlexiField(object):
    """
    FlexiField
    """

    def __init__(
            self, flexi_field_name, value=None, instance_n_keys=None, tag=None):
        self._flexi_field_name = flexi_field_name
        self._value = value
        self._tag = tag
        if instance_n_keys is not None:
            self._instance_n_keys = instance_n_keys
        else:
            self._instance_n_keys = None

    @property
    def name(self):
        """
        property method for getting the flexi_field_id for this Flexi field
        :return:
        """
        return self._flexi_field_name

    @property
    def value(self):
        """

        :return:
        """
        return self._value

    @property
    def tag(self):
        return self._tag

    @property
    def instance_n_keys(self):
        """

        :return:
        """
        return self._instance_n_keys

    def __eq__(self, other):
        if not isinstance(other, FlexiField):
            return False
        else:
            if (self._flexi_field_name == other.name
                    and self._instance_n_keys == other.instance_n_keys
                    and self._tag == other.tag):
                return True
            else:
                return False

    def __hash__(self):
        if self._instance_n_keys is not None:
            return (self._flexi_field_name, self._instance_n_keys,
                    self._tag).__hash__()
        else:
            return (self._flexi_field_name, self._value,
                    self._tag).__hash__()

    def __repr__(self):
        return "ID:{}:IV:{}:INK:{}:TAG:{}".format(
            self._flexi_field_name, self._value, self._instance_n_keys,
            self._tag)
