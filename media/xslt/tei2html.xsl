<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:tesla="http://www.exmaralda.org">
<xsl:output method="html" encoding="utf-8" indent="yes"/>
<!--

02/12/2012

This XSL file translate exmaralda TEI format to HTML display

	<div>
		<u who="#s001">
			<anchor synch="#T0" />
			<seg function="utterance" type="interrogative">
				<incident>
					<desc>question: sur place</desc>
				</incident>
				<incident>
					<desc>comment:avec brio</desc>
				</incident>
				<w>Comment</w>
				<pause />
				<w>allez</w>
				<incident>
					<desc>strong:vous</desc>
				</incident>
			</seg>
			<seg function="utterance" type="not_classified">
				<w>je</w>
				<incident>
					<desc>body:touche</desc>
				</incident>
				<w>suis</w>
				<w>vert</w>
			</seg>
			<anchor synch="#T1" />
		</u>
	</div>


									<xsl:variable name="lem" select="interp[@tttype='#ttlemma']"/>
									<xsl:variable name="pos" select="interp[@tttype='#ttpos']"/>
									<span class="speaker-word lem_{$lem} pos_{$pos}" title="Info: LEM={$lem} POS={$pos}">
										<xsl:value-of select="txm:form"/>
									</span>
									
-->

<!-- MANAGE HTML PARTS -->
<xsl:template match="/">
 	<html xmlns="http://www.w3.org/1999/xhtml">
 	
		<head>
		<title>Document </title>
		<link rel="stylesheet" href="/reanalyse/media/css/reanalyse.css" />
		
		<style type="text/css">
			<!-- ? filled automatically using js ? -->
			.speakerColor_#s001 {background-color:#EFEDFC;fill:#EFEDFC;}
			.speakerColor_#s002 {background-color:#E3FBE9;fill:#E3FBE9;}
			.speakerColor_#s003 {background-color:#FFDC98;fill:#FFDC98;}
		</style>
		
		</head>
		
		<body>
		<div class="meta">
 			<h1>Meta</h1>
 			<h2>File</h2>
 			made from XM-TEI (exmaralda) file
 			<h2>Speakers</h2>
 			<ul>
				<xsl:for-each select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:person">
					<li>speaker: <xsl:value-of select="@xml:id"/></li>
				</xsl:for-each>
 			</ul>
		</div>
		<div class="text_verbatim">
 			<h1>Transcription</h1>
 			<xsl:for-each select="/tei:TEI/tei:text/tei:body/tei:div">
				<div class="text_part">
					<xsl:for-each select="tei:u">
						<div class="text_speaker_name"><h3><xsl:value-of select="@who"/>:</h3></div>
						<!-- store spk name to set color... -->
						<xsl:variable name="spkname" select="@who"/>
						<div class="speaker-verbatim speakerColor_{$spkname}">
							<xsl:for-each select="tei:seg">
								<!-- here is a sentence -->
									<xsl:for-each select="./*">
										<!-- loop within all elements of a sentence -->
										<xsl:apply-templates select="."/>
									</xsl:for-each>
							<!-- ponctuation -->
							[<xsl:value-of select="@type"/>]
							</xsl:for-each>
						</div>
					</xsl:for-each>
				</div>
 			</xsl:for-each>
		</div>
		</body>
 	</html>
</xsl:template>

<xsl:template match="tei:w">
	<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="tei:incident">
	<xsl:variable name="contenu" select="."/>
	<a rel="text_tooltip" title="{$contenu}" class="text_anyparvb text_{$contenu}"><div> </div></a>
</xsl:template>

<xsl:template match="tei:pause">
	<a rel="text_tooltip" title="empty" class="text_anyparvb text_silence"><div> </div></a>
</xsl:template>

</xsl:stylesheet>

