from wagtail.core import hooks
from .handlers import NewWindowExternalLinkHandler





@hooks.register('register_rich_text_features')
def register_external_link(features):
    features.register_link_type(NewWindowExternalLinkHandler)




