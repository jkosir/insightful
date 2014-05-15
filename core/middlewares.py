
class XForwardedForMiddleware(object):

    # Set request remote_addr to x_forwarded_for when behind proxy (e.g. heroku)
    def process_request(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR']
        return None
