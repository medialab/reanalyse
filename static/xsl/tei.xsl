<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	
<xsl:output method="html" indent="no"/>

<xsl:template match="/|comment()|processing-instruction()">
   <h2>Hello</h2>
   <xsl:apply-templates/>
   

</xsl:template>

<xsl:template match="teiHeader">
	<!-- teiHeader -->
</xsl:template>

<xsl:template match="text">
	<xsl:for-each select="body/div/u">
		fefe
	</xsl:for-each>
</xsl:template>


</xsl:stylesheet>