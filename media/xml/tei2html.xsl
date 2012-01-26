<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.tei-c.org/ns/1.0" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:tesla="http://www.exmaralda.org">
  <xsl:output method="html" encoding="utf-8" indent="yes"/>
  
  <!-- MANAGE HTML PARTS -->
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml">
    
      <head>
        <title>Transcription</title>
        <link rel="stylesheet" href="/reanalyse/media/xml/mlab_transcription.css" />
      </head>
      
      <body>
        <div class="meta">
          <h1>Meta</h1>
          <h2>File</h2>
          made from XML-TEI file using tei2html.xls
          <h2>Speakers</h2>
          <ul>
            <xsl:for-each select="/TEI/teiHeader/profileDesc/particDesc/person">
              <li>speaker: <xsl:value-of select="@id"/></li>
            </xsl:for-each>
          </ul>
        </div>
        <div class="verbatim">
          <h1>Transcription</h1>
          <xsl:for-each select="/Trans/Episode/Section/Turn">
            <div class="speaker-part">
	            <div class="speaker-name"><h3><xsl:value-of select="@speaker"/>:</h3></div>
	            <div class="speaker-verbatim">
		            <xsl:for-each select="w">
		            <xsl:variable name="lem" select="interp[@tttype='#ttlemma']"/>
		            <xsl:variable name="pos" select="interp[@tttype='#ttpos']"/>
		            <span class="speaker-word lem_{$lem} pos_{$pos}" title="Info: LEM={$lem} POS={$pos}"><xsl:value-of select="txm:form"/></span> 
		            </xsl:for-each>
	            </div>
          	</div>
          </xsl:for-each>
        </div>
      </body>
    </html>
  </xsl:template>
  
</xsl:stylesheet>
