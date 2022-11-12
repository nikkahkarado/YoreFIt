from django import template

register = template.Library()


@register.filter
def split(value, key):
    """
    Returns the value split based on the key turned into a list.
    """
    return value.split(key)


@register.filter
def returnVal(dic, key):
    """
    Returns the value of the dictionary using the key
    """
    return dic[key]


@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)


@register.filter(name='range')
def list_range(a):
    return range(a)


@register.filter(name='invrange')
def list_inv_range(a, b):
    return range(b-a)

# Abdullah
@register.filter(name="element")
def element(array, index):
    return array[index]