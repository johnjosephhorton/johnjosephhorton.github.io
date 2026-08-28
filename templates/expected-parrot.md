# Expected Parrot

[Back to John J. Horton's website](index.html)

<img class="detail-logo" src="images/expected-parrot.png" alt="Expected Parrot E[parrot] expectation-operator logo" />

I'm excited about the potential for AI to transform the social sciences, which I've explored in [Homo silicus](papers/large-language-models-as-economic-agents-what-can-we-learn-from-homo-silicus/), [Automated social science](papers/automated-social-science-language-models-as-scientist-and-subjects/), and [General social agents](papers/general-social-agents/). But realizing that potential requires the right tools and infrastructure.

I co-founded [Expected Parrot](https://www.expectedparrot.com) with my spouse, [Robin Horton](https://www.linkedin.com/in/robertahorton/), to build those tools and infrastructure. We're building the building blocks for automated social science, centered on [EDSL](https://github.com/expectedparrot/edsl), our open-source package for conducting research with AI agents and language models.

We're particularly focused on supporting researchers, both with credits and direct assistance. Expected Parrot is backed by [Y Combinator](https://www.ycombinator.com/companies/expected-parrot). [Get in touch](mailto:founders@expectedparrot.com)—we'd be glad to hear what you're working on.

<div class="page-link-grid">
<a href="https://www.expectedparrot.com">Expected Parrot <span>Website</span></a>
<a href="https://github.com/expectedparrot/edsl">EDSL <span>Open source</span></a>
<a href="https://docs.expectedparrot.com/">Documentation <span>Learn</span></a>
<a href="https://blog.expectedparrot.com/">Expected Parrot Substack <span>Writing</span></a>
</div>

## Recent writing

<div class="writing-list">
{% for post in writing %}<article>
<time datetime="{{ post.date }}">{{ post.display_date }}</time>
<h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
<p>{{ post.description }}</p>
</article>{% endfor %}
</div>

[Read all Expected Parrot posts](https://blog.expectedparrot.com/)
