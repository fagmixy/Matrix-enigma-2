#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
import re
	
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.hoster import cHosterGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.inputParameterHandler import cInputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.outputParameterHandler import cOutputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import progress, isMatrix
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.util import cUtil

SITE_IDENTIFIER = 'rotana'
SITE_NAME = 'rotana'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://rotana.net'

MOVIE_AR = ('https://rotana.net/vod-movies', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
URL_SEARCH = ('https://rotana.net/?s=', 'showSeries')
URL_SEARCH_MOVIES = ('https://rotana.net/?s=', 'showMoviesSearch')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'film.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'أقسام الموقع', 'icon.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://rotana.net/?s='+sSearchText
        showMoviesSearch(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["أكشن","https://rotana.net/movies-genres/%d8%a3%d9%83%d8%b4%d9%86/"] )
    liste.append( ["دراما","https://rotana.net/movies-genres/%d8%af%d8%b1%d8%a7%d9%85%d8%a7/"] )
    liste.append( ["رومانسي","https://rotana.net/movies-genres/%d8%b1%d9%88%d9%85%d8%a7%d9%86%d8%b3%d9%8a/"] )
    liste.append( ["كوميديا","https://rotana.net/movies-genres/%d9%83%d9%88%d9%85%d9%8a%d8%af%d9%8a%d8%a7/"] )
    liste.append( ["المسرحيات","https://rotana.net/theatrical-plays"] )
    liste.append( ["أفلام قصيرة","https://rotana.net/vod-short-movies"] )
    liste.append( ["المسلسلات","https://rotana.net/vod-series-2"] )
    liste.append( ["الأفلام","https://rotana.net/vod-movies"] )
    	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()   
		
def showMoviesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # .+? ([^<]+)

    sPattern = '<img width=".+?" height=".+?" src="([^<]+)" class.+?<h2 class="elementor-heading-title elementor-size-default"><a href="([^<]+)">([^<]+)</a></h2>.+?<div class="elementor-widget-container">([^<]+)</div>'
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
 
            if "vod" not in aEntry[1]:
                continue
 
            sTitle = aEntry[2]
            siteUrl = aEntry[1]
            sThumbnail = aEntry[0]
            sInfo = aEntry[3]
            sYear = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()
			
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # .+? ([^<]+)

    sPattern = '<a href=([^<]+)>.+?title="([^<]+)" data-lazy-src="([^<]+)"><noscript>'

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
 
            sTitle = aEntry[1]
            siteUrl = aEntry[0].replace("'","")
            sThumbnail = aEntry[2]
            sInfo = ""
            sYear = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a href="([^<]+)" rel="next">&raquo;</a></li></ul></div>'
	 #.+?([^<]+)
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
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
    #.+? ([^<]+)
                     
    sPattern = "video([^<]+).player"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sId = aEntry.replace("')","").replace("('","")              
            url = 'https://embed.hibridvod.app/video/'+sId
            sTitle = sMovieTitle  
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

        progress_.VSclose(progress_) 
    oGui.setEndOfDirectory()                