author_xml = """<?xml version="1.0" encoding="utf-8"?>
<author xmlns="http://someurl/"
    xmlns:atom="http://www.w3.org/2005/atom">
    <name>
        Jack
    </name>
    <address>
        123 Funroad
    </address>
    <affiliation>
        None
    </affiliation>
    <email>
        None@none.none
    </email>
</author>"""

user_xml = """<?xml version="1.0" encoding="utf-8"?>
<user xmlns="http://test"
    xmlns:atom="http://www.w3.org/2005/atom">
    <username>
        test
    </username>
    <first_name>
        Scott
    </first_name>
    <last_name>
        Pilgrim
    </last_name>
    <password>
        test
    </password>
    <email>
        Scott@scott.scott
    </email>
    <degree>
        
    </degree>
    <institution>
        
    </institution>
    <fields>
    </fields>
</user>"""

comment_xml = """<?xml version="1.0" encoding="utf-8"?>
<comment xmlns="http://url/"
    xmlns:atom="http://www.w3.org/2005/atom">
    <title>
        A Comment
    </title>
    <text>
        Text
    </text>
    <votes>
        <vote>
            <atom:link rel="vote" type="application/xml" href="http://url/vote/%s"/>
        </vote>
    </votes>
</comment>"""

publication_xml="""
<?xml version="1.0" encoding="utf-8"?>
<publication xmlns="http://test/"
    xmlns:atom="http://www.w3.org/2005/atom">
    <address>
        An address
    </address>
    <booktitle>
        A title
    </booktitle>
    <chapter>
        A chapter
    </chapter>
    <rating>
    </rating>
    <edition>
        1
    </edition>
    <editor>
        An editor
    </editor>
    <howpublished>
        Not at all
    </howpublished>
    <institution>
        Some institute
    </institution>
    <isbn>
        1234-1234-1234
    </isbn>
    <journal>
        Nature
    </journal>
    <number>
        1
    </number>
    <organization>
        None
    </organization>
    <pages>
        234
    </pages>
    <publisher>
        PubCorp
    </publisher>
    <review_status>
        1
    </review_status>
    <series>
        Series
    </series>
    <publicationtype>
        Book
    </publicationtype>
    <volume>
        1
    </volume>
    <title>
        Super publication.
    </title>
    <month>
        Jan
    </month>
    <note>
        Notes notes notes notes.
    </note>
    <year>
        2010
    </year>
    <owner>
        <atom:link rel="owner" type="application/xml" href="http://test/user/%s" />
    </owner>
    <authors>    
        <author>
            <atom:link rel="author" type="application/xml" href="http://test/author/%s" />
        </author>
    </authors>
    <comments>    
        <comment>
            <atom:link rel="comment" type="application/xml" href="http://test/comment/%s" />
        </comment>
    </comments>
    <tags>
        <tag>
            <atom:link rel="tag" type="application/xml" href="http://test/tag/%s" />
        </tag>
    </tags>
    <referencematerials>
        <referencematerial>
        </referencematerial>
    </referencematerials>
    <fields>
            <somefield>
                somevalue
            </somefield>
    </fields>
</publication>"""

vote_xml = """<?xml version="1.0" encoding="utf-8"?>
<vote xmlns="http://test/"
    xmlns:atom="http://www.w3.org/2005/atom">
    <upvotes>
        10
    </upvotes>
    <downvotes>
        5
    </downvotes>
</vote>"""

esteem_xml = """<?xml version="1.0" encoding="utf-8"?>
<esteems xmlns="http://test/"
    xmlns:atom="http://www.w3.org/2005/atom">
    <esteem>
        <user>
            <atom:link rel="user" type="application/xml" href="http://{{ url }}/user/{{ esteem.user.id }}"/>
        </user>
        <tag>
            <atom:link rel="tag" type="application/xml" href="http://{{ url }}/user/{{ esteem.tag.id }}"/>
        </tag>
        <value>
            {{ esteem.value }}
        </value>
    </esteem>
    {% endfor %}
</esteems>"""

material_xml = """<?xml version="1.0" encoding="utf-8"?>
<referencematerial xmlns="http://{{ url }}"
    xmlns:atom="http://www.w3.org/2005/atom">
    <publication>
        <atom:link rel="publication" type="application/xml" href="http://{{ url
            }}/publication/{{ referencematerial.publication.id }}"/>
    </publication>
    <name>
        {{ referencematerial.name }}
    </name>
    <url>
        {{ referencematerial.url }}
    </url>
    <notes>
        {{ referencematerial.notes }}
    </notes>
</referencematerial>"""

keyword_xml = """<?xml version="1.0" encoding="utf-8"?>
<keywords xmlns="http://{{ url }}"
    xmlns:atom="http://www.w3.org/2005/atom">
    {% for key in keywords %}
    <keyword>
        <title>
            {{ key.keyword }}
        </title>
        <atom:link rel="keyword" type="application/xml" href="http://{{ url }}/keyword/{{ keyword.id }}/"/>
    </keyword>
    {% endfor %}
</keywords>"""

tag_xml = """<?xml version="1.0" encoding="utf-8"?>
<tag xmlns="http://{{ url }}"
    xmlns:atom="http://www.w3.org/2005/atom">
    <name>
        {{ tag.name }}
    </name>
    <description>
        {{ tag.description }}
    </description>
</tag>"""

rating_xml = """<?xml version="1.0" encoding="utf-8"?>
<rating xmlns="http://{{ url }}"
    xmlns:atom="http://www.w3.org/2005/atom">
    <publication>
        <atom:link rel="publication" type="application/xml" href="http://{{ url
            }}/publication/{{ rating.publication.id }}"/>
    </publication>
    <rating>
        {{ rating.rating }}
    </rating>
    <votes>
        {{ rating.votes }}
    </votes>
</rating>"""


papergroup_xml = """<?xml version="1.0" encoding="utf-8"?>
<papergroup xmlns="http://{{ url }}"
    xmlns:atom="http://www.w3.org/2005/atom">
    <title>
        {{ papergroup.title }}
    </title>
    <description>
        {{ papergroup.description }}
    </description>
    <blind_review>
        {{ papergroup.blind_review }}
    </blind_review>
    <editors>
    {% for editor in papergroup.editors.all() %}
        <editor>
            <atom:link rel="user" type="application/xml" href="http://{{ url }}/user/{{ editor.id }}" />
        </editor>
    {% endfor %}
    </editors>
    <referees>
    {% for referee in papergroup.referees.all() %}
        <referee>
            <atom:link rel="user" type="application/xml" href="http://{{ url }}/user/{{ referee.id }}" />
        </referee>
    {% endfor %}
    </referees>
    <tags>
    {% for tag in papergroup.tags.all() %}
        <tag>
            <atom:link rel="user" type="application/xml" href="http://{{ url }}/tag/{{ tag.id }}" />
        </tag>
    {% endfor %}
    </tags>
    <publications>
    {% for publication in papergroup.publications.all() %}
        <publication>
            <atom:link rel="user" type="application/xml" href="http://{{ url }}/publication/{{ publication.id }}" />
        </publication>
    {% endfor %}
    </publications>
</papergroup>"""
