#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.hoster import cHosterGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.inputParameterHandler import cInputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.outputParameterHandler import cOutputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import progress, VSlog, isMatrix
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.parser import cParser
import re
 
SITE_IDENTIFIER = 'faselhd'
SITE_NAME = 'faselhd'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://www.faselhd.pro'

MOVIE_EN = ('https://www.faselhd.pro/movies', 'showMovies')
MOVIE_HI = ('https://www.faselhd.pro/hindi', 'showMovies')
MOVIE_ASIAN = ('https://www.faselhd.pro/asian-movies', 'showMovies')
KID_MOVIES = ('https://www.faselhd.pro/dubbed-movies', 'showMovies')
SERIE_EN = ('https://www.faselhd.pro/series', 'showSeries')
REPLAYTV_NEWS = ('https://www.faselhd.pro/tvshows', 'showSeries')
ANIM_MOVIES = ('https://www.faselhd.pro/anime-movies', 'showMovies')
SERIE_ASIA = ('https://www.faselhd.co/asian-series', 'showSeries')
ANIM_NEWS = ('https://www.faselhd.pro/anime', 'showAnimes')
DOC_NEWS = ('https://www.faselhd.pro/movies-cats/%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A', 'showMovies')
DOC_SERIES = ('https://www.faselhd.pro/series_genres/documentary', 'showSeries')
MOVIE_TOP = ('https://www.faselhd.pro/movies_top_votes', 'showMovies')
MOVIE_POP = ('https://www.faselhd.pro/movies_top_views', 'showMovies')

URL_SEARCH = ('https://www.faselhd.pro/?s=', 'showSeries')
URL_SEARCH_MOVIES = ('https://www.faselhd.pro/?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = ('https://www.faselhd.pro/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH MOVIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH SERIES', 'search.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
	
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://www.faselhd.pro/?s=%D9%81%D9%8A%D9%84%D9%85+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://www.faselhd.pro/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+'+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

 # ([^<]+) .+? (.+?)
    sPattern = '<div class="postDiv "><a href="(.+?)">.+?data-src="(.+?)" class="img-fluid lazy" alt="(.+?)" />'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            
            sTitle = aEntry[2].replace("????????????","").replace("??????????","").replace("????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("????????????????","").replace("?????????? ??????????????","??????????").replace("????????????????","").replace("??????????","").replace("?????????? ??????????","").replace("??????????????","").replace("????????????","").replace("?????????? ","").replace("???????? ??????????","").replace("????????","").replace("HD","").replace("?????????????? ??????????????????","").replace("???????????? ????????????????","").replace("?????? ????????","").replace("????????????","")
            siteUrl = aEntry[0]
            sThumbnail = aEntry[1].replace("(","").replace(")","")
            sInfo = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

 # ([^<]+) .+?
    sPattern = '<div class="postDiv"><a href="([^<]+)">.+?data-src="([^<]+)" class="img-fluid lazy" alt="([^<]+)" />'


    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            
            sTitle = aEntry[2].replace("????????????","").replace("??????????","").replace("????????","").replace("??????????","").replace("????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("????????????????","").replace("?????????? ??????????????","??????????").replace("????????????????","").replace("??????????","").replace("?????????? ??????????","").replace("??????????????","").replace("????????????","").replace("?????????? ","").replace("???????? ??????????","").replace("????????","").replace("HD","").replace("?????????????? ??????????????????","").replace("???????????? ????????????????","").replace("?????? ????????","").replace("????????????","")
            siteUrl = aEntry[0]
            sThumbnail = aEntry[1].replace("(","").replace(")","")
            sInfo = ''
            sDisplayTitle2 = sTitle.split('????')[0]
            sDisplayTitle2 = sDisplayTitle2.split('??????????')[0]
            sDisplayTitle = sTitle.replace("???????????? ????????????","S10").replace("???????????? ???????????? ??????","S11").replace("???????????? ???????????? ??????","S12").replace("???????????? ???????????? ??????","S13").replace("???????????? ???????????? ??????","S14").replace("???????????? ???????????? ??????","S15").replace("???????????? ???????????? ??????","S16").replace("???????????? ???????????? ??????","S17").replace("???????????? ???????????? ??????","S18").replace("???????????? ???????????? ??????","S19").replace("???????????? ??????????????","S20").replace("???????????? ???????????? ?? ??????????????","S21").replace("???????????? ???????????? ?? ??????????????","S22").replace("???????????? ???????????? ?? ??????????????","S23").replace("???????????? ???????????? ????????????????","S24").replace("???????????? ???????????? ?? ??????????????","S25").replace("???????????? ???????????? ????????????????","S26").replace("???????????? ???????????? ????????????????","S27").replace("???????????? ???????????? ????????????????","S28").replace("???????????? ???????????? ????????????????","S29").replace("???????????? ????????????????","S30").replace("???????????? ???????????? ?? ????????????????","S31").replace("???????????? ???????????? ??????????????????","S32").replace("???????????? ??????????","S1").replace("???????????? ??????????","S1").replace(" ????????????","2").replace("???????????? ????????????","S2").replace("???????????? ????????????","S3").replace("???????????? ????????????","S3").replace("???????????? ????????????","S4").replace("???????????? ????????????","S5").replace("???????????? ????????????","S6").replace("???????????? ????????????","S7").replace("???????????? ????????????","S8").replace("???????????? ????????????","S9").replace("???????????? "," E").replace("????????????","S").replace("S ","S")


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle2)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
		
def showAnimes(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if isMatrix(): 
       sHtmlContent = str(sHtmlContent.encode('latin-1',errors='ignore'),'utf-8',errors='ignore')
 

    sPattern = '<div class="postDiv"><a href="([^<]+)">.+?data-src="([^<]+)" class="img-fluid lazy" alt="([^<]+)" />'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("&#8217;","'").replace("????????????","").replace("??????????","").replace("????????","").replace("????????","").replace("????????","").replace("????????????","")
            siteUrl = aEntry[0]
            sThumbnail = aEntry[1].replace("(","").replace(")","")
            sInfo = ""


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes1', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showAnimes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="seasonDiv.+?" data-href="(.+?)">.+?data-src="(.+?)" class="img-fluid lazy" alt="(.+?)" />.+?<div class="title">(.+?)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            postid = aEntry[0]
            nume = aEntry[3].replace("???????? "," S")
            link = 'https://www.faselhd.pro/series-ajax/?_action=get_season_list&_post_id='+postid
 
            sTitle = aEntry[2]+nume           
            sTitle = sTitle.replace("????????????","").replace("??????????","").replace("????????","").replace("??????????","").replace("????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("????????????????","").replace("?????????? ??????????????","??????????").replace("????????????????","").replace("??????????","").replace("?????????? ??????????","").replace("??????????????","").replace("????????????","").replace("?????????? ","").replace("???????? ??????????","").replace("????????","").replace("HD","").replace("?????????????? ??????????????????","").replace("???????????? ????????????????","").replace("?????? ????????","").replace("????????????","")
            siteUrl = sUrl
            sThumbnail = aEntry[1]
            sInfo = ""
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('postid', postid)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
       
    oGui.setEndOfDirectory() 
  
def showEpisodes():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    postid = oInputParameterHandler.getValue('postid')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent2 = oRequestHandler.request()
    oParser = cParser()

    sStart = '<div class="epAll" id="epAll">'
    sEnd = '<div class="postShare">'
    sHtmlContent2 = oParser.abParse(sHtmlContent2, sStart, sEnd)
    
    import requests

    postdata = {'seasonID':postid}
    link = 'https://www.faselhd.pro/series-ajax/?_action=get_season_list&_post_id='+postid
    headers = {'Host': 'www.faselhd.pro',
							'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36',
							'Referer': sUrl,
							'origin': 'https://www.faselhd.pro'}
    s = requests.Session() 	
    r = s.post(link,data = postdata)
    sHtmlContent = r.content 
    if isMatrix(): 
       sHtmlContent = sHtmlContent.decode('utf8',errors='ignore') 
       VSlog(sHtmlContent)
    if sHtmlContent:
       sPattern = '<a href="([^<]+)>([^<]+)</a>' 

       oParser = cParser()
       aResult = oParser.parse(sHtmlContent,sPattern)
       if (aResult[0] == True):
                  for aEntry in aResult[1]:
                      oOutputParameterHandler = cOutputParameterHandler() 
                      if "??????????????" in aEntry[1]:
                         continue
 
                      sTitle = aEntry[1].replace("???????????? "," E")
                      sTitle = ('%s %s') % (sTitle, sMovieTitle)
                      siteUrl = aEntry[0].replace(' class="active"', "").replace('"', "") 
                      sThumbnail = sThumbnail
                      sInfo = ""


                      oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                      oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                      oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
          
 
                      oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
      # (.+?) ([^<]+) .+?
    else :
       sPattern = '<a href="(.+?)">(.+?)</a>' 

       oParser = cParser()
       aResult = oParser.parse(sHtmlContent2,sPattern)
       if (aResult[0] == True):
                  for aEntry in aResult[1]:
                      oOutputParameterHandler = cOutputParameterHandler() 
                      if "??????????????" in aEntry[1]:
                         continue
 
                      sTitle = aEntry[1].replace("???????????? "," E")
                      sTitle = ('%s %s') % (sTitle, sMovieTitle)
                      siteUrl = aEntry[0].replace(' class="active"', "").replace('"', "") 
                      sThumbnail = sThumbnail
                      sInfo = ""


                      oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                      oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                      oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
          
 
                      oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
       
    oGui.setEndOfDirectory() 

def showEpisodes1():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    
    #Recuperation infos
    sNote = ''

    sPattern = '<div class="epAll"(.+?)<div class="col-xl-12 col-lg-12 col-md-12 col-sm-12">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
     
    
    if (aResult[0]):
        sHtmlContent1 = aResult[1][0]
	
     # (.+?) ([^<]+) .+?
    sPattern = '<a href="([^<]+)">([^<]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent1, sPattern)
	
	
    if (aResult[0] == True):  
        oOutputParameterHandler = cOutputParameterHandler()                     
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("???????????? "," E")
            sTitle = sMovieTitle+sTitle
            siteUrl = aEntry[0].replace('" class="active',"")
            sThumbnail = sThumbnail
            sInfo = sNote
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	
def showLink():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    
    #Recuperation infos
    sNote = ''

    sPattern = '<div class="singleDesc">.+?<p>([^<]+)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0]
	
     # (.+?) ([^<]+) .+?
    sPattern = 'onclick="player_iframe.location.href = ([^<]+)"><a.+?href="javascript:;"><i.+?class="fa fa-play-circle"></i>([^<]+)</a></li>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
   
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            if "01#" not in aEntry[1]:
                continue
 
            sTitle = aEntry[1].replace("&#8217;", "'") 
            siteUrl = aEntry[0].replace("'", "") 


 

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumbnail, sNote, oOutputParameterHandler)

    # (.+?)

    sPattern = 'onclick="player_iframe.location.href = ([^<]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
 
            if "embed.php?url=" in aEntry:
               continue
            
            url = aEntry.replace("'", "")

            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				


    oGui.setEndOfDirectory()       
  
def __checkForNextPage(sHtmlContent):
    sPattern = "href='([^<]+)'>&rsaquo;</a>"
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    # (.+?)
               

    sPattern = 'name="iframe" src="([^<]+)" frameborde'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = " " 
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
               sDisplayTitle = sMovieTitle+sTitle
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				
               
        
    sPattern = 'file: "(.+?)",type: "hls",'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = " " 
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
               sDisplayTitle = sMovieTitle+sTitle
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				
               
        
    sPattern = 'file: "(.+?)",.+?"type": "hls",'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = " "
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = sMovieTitle+sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				                        
    sPattern = '<a href="(.+?)" class="download-btn" '
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = " " 
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
               sDisplayTitle = sMovieTitle+sTitle
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

                
    oGui.setEndOfDirectory()