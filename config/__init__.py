"""
WIN PROFESSIONAL ACADEMY configuration package.
Includes Python 3.14+ compatibility patch for template context copying.
"""
from django.template import context

# Python 3.14 compatibility patch for django.template.context.BaseContext.__copy__
_original_copy = getattr(context.BaseContext, '__copy__', None)

def _safe_basecontext_copy(self):
    obj = self.__class__.__new__(self.__class__)
    obj.__dict__.update(getattr(self, '__dict__', {}))
    obj.dicts = self.dicts[:]
    return obj

context.BaseContext.__copy__ = _safe_basecontext_copy
