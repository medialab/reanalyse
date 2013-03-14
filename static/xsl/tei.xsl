<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output 
  method="html"
  encoding="ISO-8859-1"
  doctype-public="-//W3C//DTD HTML 4.01//EN"
  doctype-system="http://www.w3.org/TR/html4/strict.dtd"
  indent="yes" />
  
<xsl:template match="u">
  <html><body>
    <p>Liste de nombres :</p>
    <ul>
      <xsl:apply-templates select="div" />
    </ul>
  </body></html>
</xsl:template>


</xsl:stylesheet>