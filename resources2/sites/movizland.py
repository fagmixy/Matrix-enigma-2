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
 
SITE_IDENTIFIER = 'movizland'
SITE_NAME = 'movizland'
SITE_DESC = 'arabic anime'
 
URL_MAIN = 'https://movizland.fun'

RAMADAN_SERIES = (URL_MAIN + '/category/series/arab-series/', 'showSeries')
MOVIE_FAM = (URL_MAIN + '/category/movies/foreign/?genre=%d8%b9%d8%a7%d8%a6%d9%84%d9%8a', 'showMovies')
MOVIE_AR = (URL_MAIN + '/category/newmovies/arab/', 'showMovies')
MOVIE_EN = (URL_MAIN + '/category/newmovies/newforeign/', 'showMovies')
MOVIE_HI = (URL_MAIN + '/category/newmovies/india/', 'showMovies')
KID_MOVIES = (URL_MAIN + '/category/newmovies/anime/', 'showMovies')
MOVIE_TURK = (URL_MAIN + '/category/newmovies/turkey/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/category/newmovies/asia/', 'showMovies')
MOVIE_PACK = (URL_MAIN + '/category/newmovies/backs/', 'showPacks')

DOC_NEWS = (URL_MAIN + '/category/newmovies/documentary/', 'showMovies')

SERIE_EN = (URL_MAIN + '/category/series/foreign-series/', 'showSeries')
SERIE_AR = (URL_MAIN + '/category/series/arab-series/', 'showSeries')
SPORT_WWE = (URL_MAIN + '/category/series/wwe/', 'showMovies')

SERIE_TR = (URL_MAIN + '/category/series/turkish-series/', 'showSeries')
ANIM_NEWS = (URL_MAIN + '/category/series/anime-series/', 'showSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showMoviesearch')
URL_SEARCH_MOVIES = (URL_MAIN + '/?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSearchSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', 'search.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + '/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+'+sSearchText
        showSearchSeries(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + '/?s=%D9%81%D9%8A%D9%84%D9%85+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
   
 
def showMoviesearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 

      # (.+?) ([^<]+) .+?

    sPattern = '<div class="BlockItem">.+?<a href="([^<]+)">.+?<div class="BlockImageItem"><img width=".+?" height=".+?" src="([^<]+)" class="attachment-defaultb size-defaultb wp-post-image" alt="([^<]+)" />'

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
 

            siteUrl = aEntry[0]
            sTitle = aEntry[2].replace("????????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("?????? ????????","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("??????????","").replace("??????????","").replace("??????????????","").replace("????????","")
            sThumbnail = aEntry[1]
            sInfo = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMoviesearch', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
 
def showSearchSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 

      # (.+?) ([^<]+) .+?

    sPattern = '<div class="BlockItem">.+?<a href="([^<]+)">.+?src="([^<]+)" class.+?<div class="BlockTitle">([^<]+)</div>'

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
 

            siteUrl = aEntry[0]
 
            sTitle = aEntry[2].replace("????????????","").replace("??????????","").replace("????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("?? ??????????????","").replace("????????????????","").replace("????????????????","").replace("????????????????","").replace("?????? ????????","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("??????????","").replace("??????????","").replace("??????????????","").replace("????????","")
            
            sThumbnail = aEntry[1]
            sInfo = ""
            sDisplayTitle3 = sTitle.split('????????????')[0].split('????????????')[0].replace("???????????? ????????????","S10").replace("???????????? ???????????? ??????","S11").replace("???????????? ???????????? ??????","S12").replace("???????????? ???????????? ??????","S13").replace("???????????? ???????????? ??????","S14").replace("???????????? ???????????? ??????","S15").replace("???????????? ???????????? ??????","S16").replace("???????????? ???????????? ??????","S17").replace("???????????? ???????????? ??????","S18").replace("???????????? ???????????? ??????","S19").replace("???????????? ??????????????","S20").replace("???????????? ???????????? ?? ??????????????","S21").replace("???????????? ???????????? ?? ??????????????","S22").replace("???????????? ???????????? ?? ??????????????","S23").replace("???????????? ???????????? ????????????????","S24").replace("???????????? ???????????? ?? ??????????????","S25").replace("???????????? ???????????? ????????????????","S26").replace("???????????? ???????????? ????????????????","S27").replace("???????????? ???????????? ????????????????","S28").replace("???????????? ???????????? ????????????????","S29").replace("???????????? ????????????????","S30").replace("???????????? ???????????? ?? ????????????????","S31").replace("???????????? ???????????? ??????????????????","S32").replace("???????????? ??????????","S1").replace("???????????? ????????????","S2").replace("???????????? ????????????","S3").replace("???????????? ????????????","S3").replace("???????????? ????????????","S4").replace("???????????? ????????????","S5").replace("???????????? ????????????","S6").replace("???????????? ????????????","S7").replace("???????????? ????????????","S8").replace("???????????? ????????????","S9").replace("????????????","S").replace("S ","S")
            sDisplayTitle = sTitle.split('????????????')[-1].split('???????????? ')[-1].split('????')[0]
            sDisplayTitle = sDisplayTitle3+" "+" E"+sDisplayTitle


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			

            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters2', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
 
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
 

      # (.+?) ([^<]+) .+?


    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?src="([^<]+)" class.+?<div class="BlockTitle">([^<]+)</div>'
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
 

            siteUrl = aEntry[0]
            sTitle = aEntry[2].replace("????????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("?????? ????????","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("??????????","").replace("??????????","").replace("??????????????","").replace("????????","")
            
            sThumbnail = aEntry[1]
            sInfo = ''
            sYear = ''
            sDub = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear) 
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters2', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showPacks(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 

      # (.+?) ([^<]+) .+?

    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?src="([^<]+)" class.+?<div class="BlockTitle">([^<]+)</div>'

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
 

            siteUrl = aEntry[0]
            sTitle = aEntry[2].replace("????????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("?????? ????????","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("??????????","").replace("??????????????","").replace("????????????","??????????").replace("??????????","").replace("????????","").replace("?????????? ??????????","")           
            sThumbnail = aEntry[1]
            sInfo = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			

            oGui.addMoviePack(SITE_IDENTIFIER, 'showPack', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showPacks', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?src="([^<]+)" class.+?<div class="BlockTitle">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 


            sTitle = aEntry[2].replace("</em>","").replace("<em>","").replace("</span>","").replace("<span>","").replace("????????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("?????? ????????","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("??????????","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("??????????","").replace("??????????????","").replace("????????","")
            siteUrl = aEntry[0]
            sThumbnail = aEntry[1]
            sInfo = ""
            sYear = ''
            sDub = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sYear', sYear) 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
       
       
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
      # (.+?) ([^<]+) .+?
    sPattern = '<div class="BlockItem"><a href="(.+?)">.+?<img width=".+?" height=".+?" src="([^<]+)" class.+?class="BlockTitle">([^<]+)</div>'

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
 

            sTitle = aEntry[2].replace("????????????","").replace("??????????","").replace("????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("?????? ????????","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("??????????","").replace("Web-dl","").replace("??????????","").replace("??????????????","").replace("??????????","").replace("????????","").replace("????????????????","").replace("?? ??????????????","").replace("????????????????","").replace("????????????????","")
 
 
            siteUrl = aEntry[0]
            sInfo = ''
            sThumbnail = aEntry[1]
            sDisplayTitle = sTitle.replace("???????????? ????????????","S10").replace("???????????? ???????????? ??????","S11").replace("???????????? ???????????? ??????","S12").replace("???????????? ???????????? ??????","S13").replace("???????????? ???????????? ??????","S14").replace("???????????? ???????????? ??????","S15").replace("???????????? ???????????? ??????","S16").replace("???????????? ???????????? ??????","S17").replace("???????????? ???????????? ??????","S18").replace("???????????? ???????????? ??????","S19").replace("???????????? ??????????????","S20").replace("???????????? ???????????? ?? ??????????????","S21").replace("???????????? ???????????? ?? ??????????????","S22").replace("???????????? ???????????? ?? ??????????????","S23").replace("???????????? ???????????? ????????????????","S24").replace("???????????? ???????????? ?? ??????????????","S25").replace("???????????? ???????????? ????????????????","S26").replace("???????????? ???????????? ????????????????","S27").replace("???????????? ???????????? ????????????????","S28").replace("???????????? ???????????? ????????????????","S29").replace("???????????? ????????????????","S30").replace("???????????? ???????????? ?? ????????????????","S31").replace("???????????? ???????????? ??????????????????","S32").replace("???????????? ??????????","S1").replace("???????????? ????????????","S2").replace("???????????? ????????????","S3").replace("???????????? ????????????","S3").replace("???????????? ????????????","S4").replace("???????????? ????????????","S5").replace("???????????? ????????????","S6").replace("???????????? ????????????","S7").replace("???????????? ????????????","S8").replace("???????????? ????????????","S9").replace("????????????","S").replace("S ","S").split('????????????')[0]

			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler) 

        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser() 
        
    if '<div class="EpisodesList"' in sHtmlContent:
            sStart = '<div class="EpisodesList" id="LoadEpisodes">'
            sEnd = '<script type="text/javascript">'
            sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    else:
           
            sStart = '<meta property="og:image"'
            sEnd = '<meta property="og:type"'
            sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd) 
 

      # (.+?) ([^<]+) .+?

    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?src="([^<]+)" class.+?<div class="BlockTitle">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            if "????????" in aEntry[2]:
                continue
 

            siteUrl = aEntry[0]
            sTitle = aEntry[2].replace("????????????","").replace("??????????","").replace("????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("?? ??????????????","").replace("????????????????","").replace("????????????????","").replace("????????????????","").replace("?????? ????????","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("??????????","").replace("??????????","").replace("??????????????","").replace("????????","")
            
            sThumbnail = aEntry[1]
            sInfo = ""
            sDisplayTitle3 = sTitle.split('????????????')[0].split('????????????')[0].replace("???????????? ????????????","S10").replace("???????????? ???????????? ??????","S11").replace("???????????? ???????????? ??????","S12").replace("???????????? ???????????? ??????","S13").replace("???????????? ???????????? ??????","S14").replace("???????????? ???????????? ??????","S15").replace("???????????? ???????????? ??????","S16").replace("???????????? ???????????? ??????","S17").replace("???????????? ???????????? ??????","S18").replace("???????????? ???????????? ??????","S19").replace("???????????? ??????????????","S20").replace("???????????? ???????????? ?? ??????????????","S21").replace("???????????? ???????????? ?? ??????????????","S22").replace("???????????? ???????????? ?? ??????????????","S23").replace("???????????? ???????????? ????????????????","S24").replace("???????????? ???????????? ?? ??????????????","S25").replace("???????????? ???????????? ????????????????","S26").replace("???????????? ???????????? ????????????????","S27").replace("???????????? ???????????? ????????????????","S28").replace("???????????? ???????????? ????????????????","S29").replace("???????????? ????????????????","S30").replace("???????????? ???????????? ?? ????????????????","S31").replace("???????????? ???????????? ??????????????????","S32").replace("???????????? ??????????","S1").replace("???????????? ????????????","S2").replace("???????????? ????????????","S3").replace("???????????? ????????????","S3").replace("???????????? ????????????","S4").replace("???????????? ????????????","S5").replace("???????????? ????????????","S6").replace("???????????? ????????????","S7").replace("???????????? ????????????","S8").replace("???????????? ????????????","S9").replace("????????????","S").replace("S ","S")
            sDisplayTitle = sTitle.split('????????????')[-1].split('???????????? ')[-1].split('????')[0]
            sDisplayTitle = " E"+sDisplayTitle+sDisplayTitle3


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            if '/series/' in siteUrl:
                oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
            else:
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters2', sDisplayTitle, '', sThumbnail, sInfo,  oOutputParameterHandler)   
 

      # (.+?) ([^<]+) .+?

    sPattern = '<div class="EpisodeItem"><a href="(.+?)">.+?<em>(.+?)</em>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 

            siteUrl = aEntry[0]
            sTitle = 'E'+aEntry[1]
            sTitle = sMovieTitle+sTitle
            sThumbnail = sThumbnail
            sInfo = ""


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters2', sTitle, '', sThumbnail, sInfo,  oOutputParameterHandler)  
 

      # (.+?) ([^<]+) .+?

    sPattern = 'property="og:title" content="([^<]+)" />'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 

            siteUrl = sUrl
            sTitle = aEntry.replace("????????????","").replace("??????????","").replace("????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("?? ??????????????","").replace("????????????????","").replace("????????????????","").replace("????????????????","").replace("?????? ????????","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("??????????","").replace("??????????","").replace("??????????????","").replace("????????","").replace("???????????? "," E").split('????')[0]
            sThumbnail = sThumbnail
            sInfo = ""


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters2', sTitle, '', sThumbnail, sInfo,  oOutputParameterHandler)
        
       
    oGui.setEndOfDirectory()
		
def __checkForNextPage(sHtmlContent):
    sPattern = '<link rel="next" href="([^<]+)" />'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    import requests
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

   
    oParser = cParser()

  # ([^<]+) .+?
    headers = {'Host': 'movizland.top',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
     'Accept': '*/*',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'X-Requested-With': 'XMLHttpRequest',
     'Referer': sUrl,
     'Connection': 'keep-alive'}

    data = {'watch':'1'}
    s = requests.Session()
    r = s.post(sUrl,data = data)
    sHtmlContent += r.content
    # ([^<]+) (.+?)      

    sPattern = '</td><td>([^<]+)</td><td><a href="(.+?)" target'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry[1]
            sTitle =  aEntry[0]
            if '?download' in url:
                url = url.replace("moshahda","ddcdd")
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN   
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				
    # ([^<]+) (.+?)      

    sPattern = 'rel="nofollow" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
             url = aEntry[1]
             sTitle = aEntry[0]
             if url.startswith('//'):
                url = 'http:' + url
            
             sHosterUrl = url
             if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
             if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
             if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
             oHoster = cHosterGui().checkHoster(sHosterUrl)
             if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				            

    sPattern = 'rel="nofollow" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				          

    sPattern = 'allowfullscreen data-srcout="([^<]+)" FRAMEBORDER'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				         

    sPattern = '<IFRAME allowfullscreen SRC="(.+?)" FRAMEBORDER'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				
 
                
    oGui.setEndOfDirectory()
 
def showHosters1():
    oGui = cGui()
    import requests
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

   
    oParser = cParser()

  # ([^<]+) .+?
    headers = {'Host': 'movizland.top',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
     'Accept': '*/*',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'X-Requested-With': 'XMLHttpRequest',
     'Referer': sUrl,
     'Connection': 'keep-alive'}

    data = {'watch':'1'}
    s = requests.Session()
    r = s.post(sUrl,data = data)
    sHtmlContent += r.content
    # ([^<]+) (.+?)      

    sPattern = '</td><td>([^<]+)</td><td><a href="(.+?)" target'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry[1]
            sTitle =  aEntry[0]
            if '?download' in url:
                url = url.replace("moshahda","ddcdd")
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

    # ([^<]+) (.+?)      

    sPattern = 'rel="nofollow" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry[1]
            sTitle =  aEntry[0]
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				
            

    sPattern = 'rel="nofollow" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				            

    sPattern = 'allowfullscreen data-srcout="([^<]+)" FRAMEBORDER'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				
 
                
    oGui.setEndOfDirectory()
 
def showHosters2():
    oGui = cGui()
    import requests
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

   
    oParser = cParser()

  # ([^<]+) .+?
    headers = {'Host': 'movizland.top',
     'User-Agent': 'Mozilla/5.0',
     'Accept': '*/*',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'X-Requested-With': 'XMLHttpRequest',
     'Referer': sUrl,
     'Connection': 'keep-alive'}

    data = {'watch':'1'}
    s = requests.Session()
    r = s.post(sUrl,data = data)
    sHtmlContent = r.content
    if isMatrix(): 
       sHtmlContent = sHtmlContent.decode('utf8',errors='ignore')
    # ([^<]+) (.+?)      

    sPattern = '</td><td>([^<]+)</td><td><a href="(.+?)" target'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry[1]
            sTitle =  aEntry[0]
            if '?download' in url:
                url = url.replace("moshahda","ddcdd")
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				           

    sPattern = 'allowfullscreen data-srcout="([^<]+)" FRAMEBORDER'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				
    # ([^<]+) (.+?)      

    sPattern = 'rel="nofollow" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry[1]
            sTitle =  aEntry[0]
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				           

    sPattern = 'rel="nofollow" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry
            if url.startswith('//'):
               url = 'http:' + url
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

                
    oGui.setEndOfDirectory()