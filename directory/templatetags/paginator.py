# adapted from https://www.tummy.com/articles/django-pagination/

from django import template

register = template.Library()

def paginator(context, adjacent_pages = 3):

    page_obj = context['page_obj']
    paginator = context['paginator']
    page = page_obj.number
    num_pages = paginator.num_pages

    startPage = max(page - adjacent_pages, 1)
    if startPage <= 3: startPage = 1
    endPage = page + adjacent_pages + 1
    if endPage >= num_pages - 1: endPage = num_pages + 1
    adjacent_range = [n for n in range(startPage, endPage) \
            if n > 0 and n <= num_pages]


    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'adjacent_range': adjacent_range,
        'show_first': 1 not in adjacent_range,
        'show_last': num_pages not in adjacent_range,
    }

register.inclusion_tag('generic\paginator.html', takes_context=True)(paginator)
