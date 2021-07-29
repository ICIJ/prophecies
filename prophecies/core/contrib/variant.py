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
    'info': 'info',
    'pending': 'info',
    'queued': 'info',
    'running': 'info',
    'warning': 'warning',
    'cancelled': 'warning'
}


def to_variant(string='', default_variant='quiet', prefix=''):
    variant_key = slugify(string)
    return prefix + (variants_map[variant_key] or defaultVariant)
