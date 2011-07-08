from pyparsing import *
 
def filter_str(instr,removechars):
    for c in removechars:
        instr = instr.replace(c,"")
    return instr
 
 
"""
Simple BNF for parsing a BibTeX file.
Based on: http://www.gerg.ca/software/btOOL/doc/bt_language.html
 
<comment> :: "%" - end of line ;
<bibfile> :: <entry>*;
<entry>   :: <bib_entry> | <macro_entry> | <preamble_entry> | <comment_entry>
<bib_entry>   :: "@" <type> ("{" <key> "," <fields> "}") |
                        ("(" <key> "," <fields> ")") ;
<macro_entry>   :: "@" <type> ("{" <field> "}") | ("(" <field> ")");
<preamble_entry> :: "@" <type> ("{" <value> "}") | ("(" <value> ")");
<comment_entry> :: "@" <type> <string>;
 
<fields>  :: <field> ("," fields);
<field>   :: <name> "=" <value>;
<value>   :: <simple_value> ("#" <simple_value>)*;
<simple_value> :: <string> | <number> | <name> ;
 
<name>    :: "a-zA-Z0-9" "!$&*+-./:;<>?[]^_`|"
<key>     :: <name> | <number>
<string>  :: <quoted_string> | <braces_string>
<type>    :: <name>
"""
 
# basic punctation
COMMA, LBRACK, RBRACK, EQUAL, AT, HASH,LPAR,RPAR = map(Suppress,",{}=@#()")
 
comment = "%" + restOfLine
 
name = Word(filter_str(printables,"{}, ="))
key = Optional(name,'')('key')
number = Word(nums)
entrytype = Word(alphanums)('entrytype')
 
quoted_string = QuotedString('"',multiline=True,escChar='\\')
braced_string = (nestedExpr('{', '}'))
 
bstring = (quoted_string | braced_string)('string')
 
bstring.setParseAction(keepOriginalText)
# remove braces/quote chars
bstring.addParseAction(lambda tokens: tokens[0].strip()[1:-1])
 
simplevalue = (bstring('string') | number('number') | name('macro'))
value = Group(simplevalue + ZeroOrMore(HASH + simplevalue))('value')
field = (name('fieldname') + EQUAL+ value)('field')
fields = Group(Group(field) + ZeroOrMore(COMMA+Group(field)))
 
bib_entry = (AT + entrytype + ((LBRACK+key+COMMA+ fields('fields')+RBRACK) | \
               (LPAR+key+COMMA+ fields('fields')+RPAR)))('bib_entry')
macro_entry = (AT + CaselessKeyword('string')('entrytype') + \
             ((LBRACK + field + RBRACK) | (LPAR + field + RPAR)))('macro_entry')
comment_entry = (AT + CaselessKeyword('comment')('entrytype') + \
                 bstring)('comment_entry')
preamble_entry = (AT + CaselessKeyword('preamble')('entrytype') + \
                   value)('preamble_entry');
entry = bib_entry | macro_entry | comment_entry | preamble_entry
 
#entry.ignore(comment)
if __name__ == '__main__':
    teststrings = []
    teststrings.append("""
@BOOK{texbook,
   author = {Donald E. Knuth},
   title= {The {{\TeX}book}},
   publisher = "Addison-Wesley",
   year = 1984,
   note = jan # {test}
   }
""")
    teststrings.append("""@book{Anderson2007,
    title = {What is Web 2.0?: ideas, technologies and implications for education},
    publisher = {Citeseer},
    year = {2007},
    author = {Andersen, P.},
    booktitle = {Technology},
    file = {:media/datapart/Dokumente/eBooks/master\_thesis/Articles/10.1.1.108.9995.pdf:pdf},
    keywords = {Web 2.0},
    url = {http://www.jisc.ac.uk/media/documents/techwatch/tsw0701b.pdf}
}""")
    teststrings.append("""@STRING{jan = "january" }""")
    teststrings.append("""@comment{some text}""")
    for s in teststrings:
        print entry.parseString(s)
