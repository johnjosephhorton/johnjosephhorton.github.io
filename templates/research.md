# John Horton

# Academic Employment

{% for job in jobs %}
   {{ job.title }}, {{ job.institution }}, {{ job.start}}---{{ job.end }} 
{% endfor %} 


# Research

## Working papers

{% for paper in papers %}

``{{ paper.title }}''

* {{ paper.with_line }}

* {{ paper.status }}

* {{ paper.media }} 

{% endfor %}


# Awards
{% for award in awards %}
   {{ award.award }},    {{ award.year }}
{% endfor %}


# Talks
{% for talk in talks %}
   {{ talk.event }},    {{ talk.year }}
{% endfor %}

# Education

{% for school in education %}
{{ school.degree}}, {{ school.institution }} 
{% endfor %}

# Other Employment


## Published 