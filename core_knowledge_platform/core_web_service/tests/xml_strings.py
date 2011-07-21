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

publication_xml = """ """

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
