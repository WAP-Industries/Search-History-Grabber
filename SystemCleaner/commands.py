term_cmd = '''
SELECT
    keyword_search_terms.term AS search_term,
    datetime(visits.visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') AS search_time
FROM
    visits
JOIN
    keyword_search_terms
ON
    visits.id = keyword_search_terms.url_id
ORDER BY
    search_time DESC;
'''

url_cmd = '''
SELECT
    urls.url AS search_url,
    datetime(visits.visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') AS search_time
FROM
    visits
JOIN
    urls
ON
    visits.url = urls.id
ORDER BY
    search_time DESC;
'''
