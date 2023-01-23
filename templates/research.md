# John Horton

# Academic Employment

{% for job in jobs %}
   {{ job.title }}, {{ job.institution }}, {{ job.start}}---{{ job.end }} 
{% endfor %} 

# Research

## Papers
{% for paper in papers %}
{{ paper.title }} {%if paper.with_line %} (with {{ paper.with_line }}){% endif %}
{% if paper.version_line %}
   * Versions: {{ paper.version_line }}
{% endif %}
{% if paper.status %}
* Status: {{ paper.status }}
{% endif %}
* Links: {% if paper.google_scholar_url %} Citations: {{paper.google_scholar_url }} {% endif %} {% if paper.media_line %} Media: {{ paper.media_line }} {% endif %} {% if paper.video_line %} Videos: {{ paper.video_line }} {% endif %} {% if paper.slides_line %} Slides: {{ paper.slides_line }} {% endif %} {% if paper.twitter_thread_line %}Twitter Thread(s): {{ paper.twitter_thread_line }} {% endif %}
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