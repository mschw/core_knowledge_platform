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

invalid_email_user_xml = """<?xml version="1.0" encoding="utf-8"?>
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
        S@s
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
    <publication>
        <atom:link rel="publication" type="application/xml" href="http://test/publication/%s"/>
    </publication>
    <user>
            <atom:link rel="user" type="application/xml" href="http://test/user/%s"/>
    </user>
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
    <votetype>
        upvote
    </votetype>
    <caster>
        <atom:link rel="user" type="application/xml" href="http://test/user/%s"/>
    </caster>
    <comment>
        <atom:link rel="comment" type="application/xml" href="http://test/comment/%s"/>
    </comment>
</vote>"""

downvote_xml = """<?xml version="1.0" encoding="utf-8"?>
<vote xmlns="http://test/"
    xmlns:atom="http://www.w3.org/2005/atom">
    <votetype>
        downvote
    </votetype>
    <caster>
        <atom:link rel="user" type="application/xml" href="http://test/user/%s"/>
    </caster>
    <comment>
        <atom:link rel="comment" type="application/xml" href="http://test/comment/%s"/>
    </comment>
</vote>"""

esteem_xml = """<?xml version="1.0" encoding="utf-8"?>
<esteem xmlns="http://test/"
    xmlns:atom="http://www.w3.org/2005/atom">
        <user>
            <atom:link rel="user" type="application/xml" href="http://test/user/%s"/>
        </user>
        <tag>
            <atom:link rel="tag" type="application/xml" href="http://test/user/%s"/>
        </tag>
        <value>
            512
        </value>
</esteem>"""

material_xml = """<?xml version="1.0" encoding="utf-8"?>
<referencematerial xmlns="http://test"
    xmlns:atom="http://www.w3.org/2005/atom">
    <publication>
        <atom:link rel="publication" type="application/xml" href="http://test/publication/%s"/>
    </publication>
    <name>
        Statistic Files
    </name>
    <url>
        http://www.google.com/
    </url>
    <notes>
        Statistic Files for the documentation.
    </notes>
</referencematerial>"""

keyword_xml = """<?xml version="1.0" encoding="utf-8"?>
<keyword xmlns="http://test"
    xmlns:atom="http://www.w3.org/2005/atom">
    <keyword>
            Some keyword.
    </keyword>
</keyword>"""

tag_xml = """<?xml version="1.0" encoding="utf-8"?>
<tag xmlns="http://test"
    xmlns:atom="http://www.w3.org/2005/atom">
    <name>
        AI
    </name>
    <description>
        Artificial Intelligence.
    </description>
</tag>"""

rating_xml = """<?xml version="1.0" encoding="utf-8"?>
<rating xmlns="http://test"
    xmlns:atom="http://www.w3.org/2005/atom">
    <publication>
        <atom:link rel="publication" type="application/xml" href="http://test/publication/%s"/>
    </publication>
    <rating>
        5
    </rating>
</rating>"""


papergroup_xml = """<?xml version="1.0" encoding="utf-8"?>
<papergroup xmlns="http://test"
    xmlns:atom="http://www.w3.org/2005/atom">
    <title>
        Nature papergroup.
    </title>
    <description>
        Papergroup of nature.
    </description>
    <blind_review>
        1
    </blind_review>
    <editors>
        <editor>
            <atom:link rel="user" type="application/xml" href="http://test/user/%s" />
        </editor>
    </editors>
    <referees>
        <referee>
            <atom:link rel="user" type="application/xml" href="http://test/user/%s" />
        </referee>
    </referees>
    <tags>
        <tag>
            <atom:link rel="user" type="application/xml" href="http://test/tag/%s" />
        </tag>
    </tags>
    <publications>
        <publication>
            <atom:link rel="user" type="application/xml" href="http://test/publication/%s" />
        </publication>
    </publications>
</papergroup>"""

papergroup_no_publication_xml = """<?xml version="1.0" encoding="utf-8"?>
<papergroup xmlns="http://test"
    xmlns:atom="http://www.w3.org/2005/atom">
    <title>
        Nature papergroup.
    </title>
    <description>
        Papergroup of nature.
    </description>
    <blind_review>
        1
    </blind_review>
    <editors>
        <editor>
            <atom:link rel="user" type="application/xml" href="http://test/user/%s" />
        </editor>
    </editors>
    <referees>
        <referee>
            <atom:link rel="user" type="application/xml" href="http://test/user/%s" />
        </referee>
    </referees>
    <tags>
        <tag>
            <atom:link rel="user" type="application/xml" href="http://test/tag/%s" />
        </tag>
    </tags>
    <publications>
    </publications>
</papergroup>"""

template_xml = """<?xml version="1.0" encoding="utf-8"?>
<peerreviewtemplate xmlns="http://test"
    xmlns:atom="http://www.w3.org/2005/atom">
    <templatetext>
        A template.

        With linebreaks.

        An stuff like that.
    </templatetext>
    <binarypath>
        Some fancy Path.
    </binarypath>
</peerreviewtemplate>"""

peerreview_xml = """<?xml version="1.0" encoding="utf-8"?>
<peerreview xmlns="http://test"
    xmlns:atom="http://www.w3.org/2005/atom">
    <peerreviewer>
        <atom:link rel="user" type="application/xml" href="http://test/user/%s"/>
    </peerreviewer>
    <publication>
        <atom:link rel="publicaiton" type="application/xml" href="http://test/publication/%s"/>
    </publication>
    <template>
        <atom:link rel="template" type="application/xml" href="http://test/peerreviewtemplate/%s"/>
    </template>
    <title>
        The reviewing of stuff.
    </title>
    <review>
        This stuff is pretty awesome stuff and awesome in the extreme.
    </review>
</peerreview>"""

login_xml = """<?xml version="1.0" encoding="utf-8"?>
<login>
    <username>unittest</username>
    <password>unit</password>
</login>"""

login_invalid_xml = """<?xml version="1.0" encoding="utf-8"?>
<login>
    <username>unittest</username>
    <password>invalid</password>
</login>"""
