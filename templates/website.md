# {{ basic_info.name }}

<img src="images/me.jpeg" alt="me" width="200" />  <!-- Adjust '200' to your preferred width -->

## Bio {.bio-class}


{{ basic_info.bio }}
[Email](mailto:{{ basic_info.email }}) · [MIT Sloan]({{ basic_info.mit_url }}) · [NBER]({{ basic_info.nber_url }}) · [Google Scholar]({{ basic_info.google_scholar }}) · [ORCID]({{ basic_info.orcid_url }}) · [\{{ basic_info.twitter_handle }}]({{ basic_info.twitter_url }})

# Employment

{% for job in jobs %}
   {{ job.title }}, {% if job.url %}[{{ job.institution }}]({{ job.url }}){% else %}{{ job.institution }}{% endif %}, {{ job.start}}{% if job.end %}---{{ job.end }}{% endif %}
{% endfor %} 

## Affiliations

{% for affiliation in affiliations %}
   {{ affiliation.role }}, {% if affiliation.url %}[{{ affiliation.organization }}]({{ affiliation.url }}){% else %}{{ affiliation.organization }}{% endif %}, {{ affiliation.start }}---{{ affiliation.end }}
{% endfor %}

# Research {.paper-class}

{% for paper in papers %}
### {{ paper.title }} {%if paper.with_line %} {.paper-class}
(with {{ paper.with_line }}){% endif %}
{% if paper.version_line %}
* Paper: {{ paper.version_line }}
{% endif %}
{% if paper.primary_publication %}
* {{ paper.publication_label }}: {{ paper.primary_publication.citation }}
{% endif %}
{% if paper.show_status %}
* Status: {{ paper.status }}
{% endif %}
{% if paper.has_additional_links %}
* Links: {% if paper.google_scholar_url %} Citations: {{paper.google_scholar_url }} {% endif %} {% if paper.media_line %} Media: {{ paper.media_line }} {% endif %} {% if paper.video_line %} Videos: {{ paper.video_line }} {% endif %} {% if paper.slides_line %} Slides: {{ paper.slides_line }} {% endif %} {% if paper.twitter_thread_line %}Twitter Thread(s): {{ paper.twitter_thread_line }} {% endif %} {% if paper.code_line %} Replication: {{ paper.code_line }} {% endif %}
{% endif %}
{% endfor %}


# Awards & Grants

## Awards
{% for award in awards %}
   {% if award.url %}[{{ award.award }}]({{ award.url }}){% else %}{{ award.award }}{% endif %}, {{ award.year }}
{% endfor %}

## Grants
{% for grant in grants %}
   {{ grant.grant }}, {{ grant.year }}
{% endfor %}

# Talks
{% for talk in talks %}
   {% if talk.url %}[{{ talk.event }}]({{ talk.url }}), {{ talk.year }}{% else %}{{ talk.event }}, {{ talk.year }}{% endif %}
{% endfor %}

# Education

{% for school in education %}
{% if school.url %}[{{ school.institution }}]({{ school.url }}){% else %}{{ school.institution }}{% endif %}, {{ school.degree}}{% if school.field %} in {{ school.field }}{% endif %}{% if school.finish %}, {{ school.finish }}{% endif %}
{% endfor %}

# Teaching & Service

## Teaching

{% for item in teaching %}
### {{ item.course_title }}

{{ item.institution }} — {{ item.terms | join(' · ') }}
{% endfor %}

## Service

{% for item in service %}
   {{ item.role }}, {{ item.organization }}, {{ item.start }}---{{ item.end }}
{% endfor %}

## Reviewing

{{ reviewing | map(attribute='journal') | join(' · ') }}
