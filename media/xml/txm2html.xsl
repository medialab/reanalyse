<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:txm="http://textometrie.org/1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	  <xsl:output method="html" encoding="utf-8" indent="yes"/>
	  
	  <!-- MANAGE HTML PARTS -->


<xsl:template match="w">
	<xsl:element name="span">
		<xsl:attribute name="class">speaker-word</xsl:attribute>
		<xsl:attribute name="title">
				<xsl:value-of select="interp[@type='#ttpos']"/>_<xsl:value-of select="interp[@type='#ttlemma']"/>
		</xsl:attribute>
		<xsl:attribute name="pos">
			<xsl:value-of select="interp[@type='#ttpos']"/>
		</xsl:attribute>
		<xsl:attribute name="lem">
			<xsl:value-of select="interp[@type='#ttlemma']"/>
		</xsl:attribute>
		<xsl:value-of select="txm:form"/>
	</xsl:element> 
</xsl:template>


<xsl:template match="Event">
	<xsl:element name="span">
		<xsl:attribute name="class">speaker-event</xsl:attribute>
		<xsl:attribute name="title"><xsl:value-of select="@desc"/></xsl:attribute>
		<xsl:value-of select="@desc"/>
	</xsl:element> 
</xsl:template>
  

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
  		made from XML-TXM file using txm2html.xls
  		<h2>Speakers</h2>
  		<ul>
			<xsl:for-each select="/Trans/Speakers/Speaker">
  			<li>speaker: <xsl:value-of select="@id"/></li>
			</xsl:for-each>
  		</ul>
		</div>
		<div class="verbatim">
  		<h1>Transcription</h1>
  		<xsl:for-each select="/Trans/Episode/Section/Turn">
			<div class="speaker-part">
				<div class="speaker-name">
					<h3><xsl:value-of select="@speaker"/>: </h3>
				</div>
				<div class="speaker-verbatim">
					<xsl:for-each select="*">
						<xsl:apply-templates select="." />
<!--
<xsl:variable name="lem" select="interp[@tttype='#ttlemma']"/>
<xsl:variable name="pos" select="interp[@tttype='#ttpos']"/>
<span class="speaker-word lem_{$lem} pos_{$pos}" title="Info: LEM={$lem} POS={$pos}">
<xsl:value-of select="txm:form"/>
</span>
-->
					</xsl:for-each>
				</div>
  			</div>
  		</xsl:for-each>
		</div>
  	</body>
	</html>
  </xsl:template>
  
</xsl:stylesheet>
