"""A7: independence's registrable-domain step uses the Public Suffix List's private section
(GitHub Pages, europa.eu subdomains, ...) offline, from tldextract's bundled snapshot — never a
network fetch."""
from tldextract import TLDExtract

_EXTRACT = TLDExtract(suffix_list_urls=(), include_psl_private_domains=True)


def test_github_pages_subdomains_get_different_registrable_domains():
    foo = _EXTRACT("foo.github.io")
    bar = _EXTRACT("bar.github.io")
    assert foo.top_domain_under_public_suffix != bar.top_domain_under_public_suffix
    assert foo.top_domain_under_public_suffix == "foo.github.io"
    assert bar.top_domain_under_public_suffix == "bar.github.io"


def test_europa_eu_subdomains_share_a_registrable_domain():
    edpb = _EXTRACT("edpb.europa.eu")
    eur_lex = _EXTRACT("eur-lex.europa.eu")
    assert edpb.top_domain_under_public_suffix == eur_lex.top_domain_under_public_suffix == "europa.eu"
