# {{ basic_info.name }}

<img src="images/me.jpeg" alt="Portrait of John J. Horton" width="200" />

## Bio {.bio-class}


{{ basic_info.bio }}
[Email](mailto:{{ basic_info.email }}) · [MIT Sloan]({{ basic_info.mit_url }}) · [NBER]({{ basic_info.nber_url }}) · [Google Scholar]({{ basic_info.google_scholar }}) · [ORCID]({{ basic_info.orcid_url }}) · [CV](cv.pdf) · [Bio & press](bio.html) · [\{{ basic_info.twitter_handle }}]({{ basic_info.twitter_url }})

{% for venture in ventures %}<aside class="venture-card" aria-label="{{ venture.name }}">
<div class="venture-label">Also building</div>
<div class="venture-intro">
<a href="{{ venture.url }}"><img class="venture-logo" src="{{ venture.logo }}" alt="Expected Parrot E[parrot] expectation-operator logo" /></a>
<div><div class="venture-heading"><a href="{{ venture.url }}">{{ venture.name }}</a></div>
<p>{{ venture.description }}</p>
<p class="venture-support">{{ venture.support }}</p></div>
</div>
<div class="venture-links"><a href="expected-parrot.html">More about Expected Parrot</a><a href="{{ venture.package_url }}">{{ venture.package }} · open-source package</a><a href="{{ venture.blog_url }}">{{ venture.blog }}</a><a href="{{ venture.backer_url }}"><img class="venture-backer-logo" src="{{ venture.backer_logo }}" alt="" />{{ venture.backer }}</a></div>
</aside>
{% endfor %}

<section class="recent-writing" aria-labelledby="recent-writing-heading">
<div class="section-heading-row"><h2 id="recent-writing-heading">Recent writing</h2><a href="https://blog.expectedparrot.com/">All posts</a></div>
<div class="writing-list">{% for post in writing %}<article><time datetime="{{ post.date }}">{{ post.display_date }}</time><h3><a href="{{ post.url }}">{{ post.title }}</a></h3><p>{{ post.description }}</p></article>{% endfor %}</div>
</section>

# Employment

{% for job in jobs %}
   {{ job.title }}, {% if job.url %}[{{ job.institution }}]({{ job.url }}){% else %}{{ job.institution }}{% endif %}, {{ job.start}}{% if job.end %}---{{ job.end }}{% endif %}
{% endfor %} 

## Affiliations

{% for affiliation in affiliations %}
   {{ affiliation.role }}, {% if affiliation.url %}[{{ affiliation.organization }}]({{ affiliation.url }}){% else %}{{ affiliation.organization }}{% endif %}, {{ affiliation.start }}---{{ affiliation.end }}
{% endfor %}

# Research {.paper-class}

<div class="research-tools" role="search" aria-label="Filter research">
<label for="research-search">Find a paper</label>
<input id="research-search" type="search" placeholder="Search titles, authors, venues, or status…" autocomplete="off" />
<span id="research-count" aria-live="polite"></span>
<label class="sort-label" for="research-sort">Sort</label>
<select id="research-sort"><option value="updated">Recently updated</option><option value="newest">Newest publication</option><option value="oldest">Oldest publication</option></select>
</div>
<div class="research-view" aria-label="Research collection"><button class="view-chip active" type="button" data-view="selected">Selected research</button><button class="view-chip" type="button" data-view="recent">Recently updated</button><button class="view-chip" type="button" data-view="all">All research</button></div>
<div class="filter-label">Topics</div><div class="filter-chips" aria-label="Research topic filters"><button class="filter-chip active" type="button" data-topic="all">All topics</button>{% for topic in research_topics %}<button class="filter-chip" type="button" data-topic="{{ topic }}">{{ topic }}</button>{% endfor %}</div>
<div class="filter-label">Publication type</div><div class="filter-chips type-chips" aria-label="Research publication type filters"><button class="type-chip active" type="button" data-type="all">All types</button>{% for type in research_types %}<button class="type-chip" type="button" data-type="{{ type }}">{{ type }}</button>{% endfor %}</div>
<div class="filter-chips status-chips" aria-label="Research status filters"><button class="status-chip active" type="button" data-status="all">Any status</button>{% for status in research_statuses %}<button class="status-chip" type="button" data-status="{{ status }}">{{ status }}</button>{% endfor %}</div>

<div id="research-results">{% for paper in papers %}<article class="paper-entry" data-topic="{{ paper.topic }}" data-type="{{ paper.type_label }}" data-status="{{ paper.status_group }}" data-selected="{{ 'true' if paper.selected else 'false' }}" data-recent="{{ 'true' if paper.recent else 'false' }}" data-updated="{{ paper.last_updated }}" data-year="{{ paper.publication_year }}" data-order="{{ paper.original_order }}" data-search="{{ paper.title }} {{ paper.with_line or '' }} {{ paper.status }} {{ paper.type_label }} {% if paper.primary_publication %}{{ paper.primary_publication.venue }}{% endif %}">
<div class="paper-kicker">{{ paper.type_label }}</div>
### {% if paper.page_url %}[{{ paper.title }}]({{ paper.page_url }}){% else %}{{ paper.title }}{% endif %} {%if paper.with_line %} {.paper-class}
(with {{ paper.with_line }}){% endif %}
{% if paper.version_line or paper.page_url %}
* Paper Links: {% if paper.page_url %}[Details]({{ paper.page_url }}){% if paper.version_line %} · {% endif %}{% endif %}{{ paper.version_line or '' }}
{% endif %}
{% if paper.primary_publication %}
* {{ paper.publication_label }}: {{ paper.primary_publication.citation }}
{% endif %}
{% if paper.show_status %}
* Status: {{ paper.status }}
{% endif %}
{% if paper.has_additional_links %}
<div class="resource-links" aria-label="Resources for {{ paper.title }}">{% for resource in paper.resource_links %}<a class="resource-chip" href="{{ resource.url }}">{{ resource.label }}</a>{% endfor %}</div>
{% endif %}
</article>{% endfor %}</div>


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
## Featured talks
<div class="featured-talks">{% for talk in featured_talks %}<a class="resource-chip" href="{{ talk.url }}">{{ talk.topic }} <span>Video</span></a>{% endfor %}</div>

## Complete talk archive
<div class="talk-tools"><label for="talk-search">Find a talk</label><input id="talk-search" type="search" placeholder="Search events or years…" autocomplete="off" /></div>
{% for year, year_talks in talk_groups.items() %}<details class="talk-year" {% if loop.index <= 2 %}open{% endif %}><summary>{{ year }} <span>({{ year_talks|length }})</span></summary>
{% for talk in year_talks %}
   {% if talk.url %}[{{ talk.event }}]({{ talk.url }}), {{ talk.year }}{% else %}{{ talk.event }}, {{ talk.year }}{% endif %}
{% endfor %}</details>{% endfor %}

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
