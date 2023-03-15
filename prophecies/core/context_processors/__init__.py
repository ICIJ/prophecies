from prophecies import VERSION


def version(request):  # pylint: disable=unused-argument
    return {'version': VERSION}
