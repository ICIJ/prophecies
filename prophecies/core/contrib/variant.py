from django.utils.text import slugify

variants_map = {
    'success': 'success',
    'ok': 'success',
    'done': 'success',
    'danger': 'danger',
    'error': 'danger',
    'fail': 'danger',
    'failed': 'danger',
    'failure': 'danger',
    'pending': 'quiet',
    'queued': 'quiet',
    'info': 'info',
    'assigned': 'info',
    'running': 'info',
    'warning': 'warning',
    'cancelled': 'warning'
}


def to_variant(string='', default_variant='quiet', prefix=''):
    variant_key = slugify(string)
    return prefix + variants_map.get(variant_key, default_variant)
