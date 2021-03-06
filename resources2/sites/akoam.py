#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.hoster import cHosterGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.inputParameterHandler import cInputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.outputParameterHandler import cOutputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import progress, VSlog
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.parser import cParser
import re

SITE_IDENTIFIER = 'akoam'
SITE_NAME = 'akoam'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://old.akwam.cc'
MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_CLASSIC = (URL_MAIN + '/cat/165/%D8%A7%D8%B1%D8%B4%D9%8A%D9%81-%D8%A7%D9%84%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9', 'showMovies')
MOVIE_PACK = (URL_MAIN + '/cat/186/%D8%B3%D9%84%D8%A7%D8%B3%D9%84-%D8%A7%D9%84%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9', 'showSeries')
MOVIE_EN = (URL_MAIN + '/cat/156/%D8%A7%D9%84%D8%A3%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9', 'showMovies')
KID_MOVIES = (URL_MAIN + '/cat/179/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%A7%D9%86%D9%85%D9%8A-%D8%A7%D9%84%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D8%A9', 'showMovies')
MOVIE_AR = (URL_MAIN + '/cat/155/%D8%A7%D9%84%D8%A3%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9', 'showMovies')
MOVIE_HI = (URL_MAIN + '/cat/168/%D8%A7%D9%84%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D9%87%D9%86%D8%AF%D9%8A%D8%A9', 'showMovies')
REPLAYTV_NEWS = (URL_MAIN + '/cat/81/%D8%A7%D9%84%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%A7%D9%84%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86%D9%8A%D8%A9', 'showSeries')
SERIE_AR = (URL_MAIN + '/cat/80/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9', 'showSeries')
SERIE_EN = (URL_MAIN + '/cat/166/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9', 'showSeries')
SERIE_DUBBED = (URL_MAIN + '/cat/190/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D8%A9', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/cat/185/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D8%A7%D8%B3%D9%8A%D9%88%D9%8A%D8%A9', 'showSeries')
SERIE_TR = (URL_MAIN + '/cat/190/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D8%A9', 'showSeries')
ANIM_NEWS = (URL_MAIN + '/cat/83/%D8%A7%D9%84%D8%A7%D9%86%D9%85%D9%8A', 'showSeries')
SERIE_GENRES = (True, 'showGenres')
DOC_NEWS = (URL_MAIN + '/cat/94/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A%D8%A9', 'showMovies')
URL_SEARCH = (URL_MAIN + '/search/', 'showMoviesSearch')
URL_SEARCH_MOVIES = (URL_MAIN + '/search/%D9%81%D9%8A%D9%84%D9%85+', 'showMoviesSearch')
URL_SEARCH_SERIES = (URL_MAIN + '/search/%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSeriesSearch')
URL_SEARCH_MISC = (URL_MAIN + '/search/', 'showSeriesSearch')
FUNCTION_SEARCH = 'showSearch'

def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchAll', 'Search All', 'search.png', oOutputParameterHandler)
    

            
    oGui.setEndOfDirectory()
 
def showSearchAll():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + '/search/'+sSearchText
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return  
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + '/search/%D9%81%D9%8A%D9%84%D9%85+'+sSearchText
        showMoviesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + '/search/%D9%85%D8%B3%D9%84%D8%B3%D9%84+'+sSearchText
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showMoviesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
      # (.+?) ([^<]+) .+?

    sPattern = '<div class="tags_box"><a href="(.+?)">.+?style=(.+?)>.+?<h1>(.+?)</h1>'

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


            sTitle = aEntry[2].replace("????????????","").replace("??????????","").replace("????????????","").replace("????????","").replace("????????????","").replace("??????????","").replace("?????????????? ??????????????????","").replace("???????????? ????????????????","").replace("????????","").replace("????????????","").replace("?????? ????????","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("?????????? ??????????????","??????????")
            siteUrl = aEntry[0]
            sInfo = ""
            sThumbnail = aEntry[1].replace("'background-image: url(","").replace(");'","")
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showSeriesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
      # (.+?) ([^<]+) .+?

    sPattern = '<div class="tags_box"><a href="(.+?)">.+?style=(.+?)>.+?<h1>(.+?)</h1>'


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
 
            sTitle = aEntry[2].replace("????????????","").replace("??????????","").replace("????????????","").replace("????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("?????????????? ??????????????????","").replace("?????? ????????","").replace("????????????","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("?????????????? ??????????????","(?????????????? ??????????????)").replace("?????????? ??????????????","??????????").replace("??????????","????????????")
            siteUrl = aEntry[0]
            sInfo = ''
            sThumbnail = aEntry[1].replace("'background-image: url(","").replace(");'","")
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                  sYear = str(m.group(0))
                  sTitle = sTitle.replace(sYear,'')
            sDisplayTitle = sTitle.replace("???????????? ????????????","S10").replace("???????????? ???????????? ??????","S11").replace("???????????? ???????????? ??????","S12").replace("???????????? ???????????? ??????","S13").replace("???????????? ???????????? ??????","S14").replace("???????????? ???????????? ??????","S15").replace("???????????? ???????????? ??????","S16").replace("???????????? ???????????? ??????","S17").replace("???????????? ???????????? ??????","S18").replace("???????????? ???????????? ??????","S19").replace("???????????? ??????????????","S20").replace("???????????? ???????????? ?? ??????????????","S21").replace("???????????? ???????????? ?? ??????????????","S22").replace("???????????? ???????????? ?? ??????????????","S23").replace("???????????? ???????????? ????????????????","S24").replace("???????????? ???????????? ?? ??????????????","S25").replace("???????????? ???????????? ????????????????","S26").replace("???????????? ???????????? ????????????????","S27").replace("???????????? ???????????? ????????????????","S28").replace("???????????? ???????????? ????????????????","S29").replace("???????????? ????????????????","S30").replace("???????????? ???????????? ?? ????????????????","S31").replace("???????????? ???????????? ??????????????????","S32").replace("???????????? ??????????","S1").replace("???????????? ????????????","S2").replace("???????????? ????????????","S3").replace("???????????? ????????????","S3").replace("???????????? ????????????","S4").replace("???????????? ????????????","S5").replace("???????????? ????????????","S6").replace("???????????? ????????????","S7").replace("???????????? ????????????","S8").replace("???????????? ????????????","S9").split('????????????')[0]





            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addTV(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
		
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["?????????????? ????????????","https://old.akwam.co/cat/190/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D8%A9"] )

    
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)
       
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

    sPattern = '<div class="subject_box shape"><a href="(.+?)">.+?src="(.+?)" alt.+?<h3>(.+?)</h3>'
		
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
 
            sTitle = aEntry[2].replace("????????????","").replace("??????????","").replace("????????????","").replace("????????","").replace("????????????","").replace("??????????","").replace("?????????????? ??????????????????","").replace("???????????? ????????????????","").replace("????????","").replace("????????????","").replace("?????? ????????","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("?????????? ??????????????","??????????")
            siteUrl = aEntry[0]
            sDesc = ''
            sThumb = aEntry[1]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
               sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
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

    sPattern = '<div class="sub_desc">.+?<span style="color:#FFD700">.+?</span>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult:
        sNote = aResult[1]
     # (.+?) ([^<]+) .+?
    sPattern = "class='sub_file_title'>(.+?)<i>(.+?)</i>.+?class='download_btn' target='_blank' href=(.+?)>"
		
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

                sTitle = aEntry[0].split('akoam', 1)[0]
                sTitle = sTitle.replace("."," ").replace("Ep","E").replace("Se","S").replace("??????????","").replace("????????","").replace("?????? ????????","").replace("WEB-DL","").replace("BRRip","").replace("720P","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080P","").replace("1080p","").replace("HC","").replace("Web-dl","").replace("DVD","").replace("BRRIP","").replace("BRRiP","").replace("WEB","")
                sYear = ''
                sEpisode = re.search('Ep(.+?).',  str(aEntry[0]))
                if sEpisode:
                   sEpisode= str(sEpisode.group(0))
                   sEpisode= sEpisode.replace("Ep","E").replace("ep","E")
                   sTitle= sEpisode+sMovieTitle
                
                else: 
                     sEpisode = re.search('ep(.+?).',  str(aEntry[0]))
                     if sEpisode:
                        sEpisode= str(sEpisode.group(0))
                        sEpisode= sEpisode.replace("ep","E")
                        sTitle= sEpisode+sMovieTitle
                m = re.search('([0-9]{4})', sTitle)
                if m:
                   sYear = str(m.group(0))
                   sTitle = sTitle.replace(sYear,'')
                siteUrl = aEntry[2].replace('"','')
                sThumbnail = sThumbnail
                sInfo = '[COLOR yellow]'+str(sNote)+'[/COLOR]'
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oOutputParameterHandler.addParameter('sYear', sYear)
                if 'akwam'  in siteUrl:
                    oGui.addLink(SITE_IDENTIFIER, 'showLinks', sTitle+'('+aEntry[1]+')', sThumbnail, sInfo, oOutputParameterHandler)
                if '/video/'  in siteUrl:
                    oGui.addLink(SITE_IDENTIFIER, 'showHosters2', sTitle+'('+aEntry[1]+')', sThumbnail, sInfo, oOutputParameterHandler)
    # (.+?) .+?
    sPattern = '<a href="https://akwam.net/movie/(.+?)" target="_blank"><span style='

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = " ???????? ???????????????? ?????? ?????????????? ???????????? ???? ??????"
            siteUrl = "https://akwam.net/movie/"+aEntry
            sThumbnail = sThumbnail
            sInfo = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeasons2', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
    if '?????? ???????????? ???? ?????????? ?????? ???????? ?????????? ??????????' in sHtmlContent:
        oGui.addText(SITE_IDENTIFIER,'?????? ???????????? ???? ?????????? ?????? ???????? ?????????? ???????????? ???????? ???????????? ?????? ?????????? ???? ?????????????? ?????????????? ???????????? ????????????')
 
    oGui.setEndOfDirectory()
	
def showLinks():
    oGui = cGui()
    import requests
    sgn=requests.Session()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    # ([^<]+) .+?

    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36')
    oRequestHandler.addHeaderEntry('origin', 'https://old.akwam.cc')
    oRequestHandler.addHeaderEntry('Cookie', cook)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Referer', sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"direct_link":"(.+?)",'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            sHosterUrl = aEntry
            sTitle = sMovieTitle
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl
             
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
         
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
# ([^<]+) .+? (.+?)
    sPattern = '<div class="subject_box shape"><a href="(.+?)">.+?src="(.+?)" alt.+?<h3>(.+?)</h3>'

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
 

            sTitle = aEntry[2].replace("????????????","").replace("????????????","").replace("??????????","").replace("????????","").replace("?????? ????????","").replace("????????????","").replace("??????????","").replace("????????????","").replace("????????","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("?????????? ??????????????","??????????")
            siteUrl = aEntry[0]
            sInfo = ""
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
               sTitle = sTitle.replace(sYear,'')
            sThumbnail = aEntry[1]
            sDisplayTitle = sTitle.replace("???????????? ???????????? ??????","S11").replace("???????????? ???????????? ??????","S12").replace("???????????? ???????????? ??????","S13").replace("???????????? ???????????? ??????","S14").replace("???????????? ???????????? ??????","S15").replace("???????????? ???????????? ??????","S16").replace("???????????? ???????????? ??????","S17").replace("???????????? ???????????? ??????","S18").replace("???????????? ???????????? ??????","S19").replace("???????????? ??????????????","S20").replace("???????????? ???????????? ?? ??????????????","S21").replace("???????????? ???????????? ?? ??????????????","S22").replace("???????????? ???????????? ?? ??????????????","S23").replace("???????????? ???????????? ????????????????","S24").replace("???????????? ???????????? ?? ??????????????","S25").replace("???????????? ???????????? ????????????????","S26").replace("???????????? ???????????? ????????????????","S27").replace("???????????? ???????????? ????????????????","S28").replace("???????????? ???????????? ????????????????","S29").replace("???????????? ????????????????","S30").replace("???????????? ???????????? ?? ????????????????","S31").replace("???????????? ???????????? ??????????????????","S32").replace("???????????? ??????????","S1").replace("???????????? ????????????","S2").replace("???????????? ????????????","S3").replace("???????????? ????????????","S3").replace("???????????? ????????????","S4").replace("???????????? ????????????","S5").replace("???????????? ????????????","S6").replace("???????????? ????????????","S7").replace("???????????? ????????????","S8").replace("???????????? ????????????","S9").replace("???????????? ????????????","S10").split('????????????')[0]
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
      # (.+?) ([^<]+) .+?
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="next".+?href="(.+?)">'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False

  
def showSeasons():
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

    sPattern = '<div class="sub_desc"><span style="color:#FFD700">.+?</span>([^<]+)<br />'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0]
    # .+? ([^<]+)
    sPattern = '<a href="([^<]+)" target="_blank"><span style="color:#.+?">([^<]+)</span></a><br />'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1]
            sTitle = '[COLOR cyan]'+sTitle+'[/COLOR]'
            siteUrl = aEntry[0]
            sThumbnail = sThumbnail
            sInfo = ""
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
     # (.+?) ([^<]+)
    sPattern = "class='sub_file_title'>(.+?)<i>(.+?)</i>.+?class='download_btn' target='_blank' href=(.+?)>"


    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
                sTitle = aEntry[0].replace("."," ").replace("WEB"," ").replace("Ep","E").split('akoam', 1)[0].split('akwam', 1)[0]
                sTitle = sTitle.replace("."," ").replace("??????????","").replace("????????","").replace("?????? ????????","").replace("????????????","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("DVD","").replace("BRRIP","").replace("BRRiP","").replace("-DL","")
                sYear = ''
                m = re.search('([0-9]{4})', sTitle)
                if m:
                    sYear = str(m.group(0))
                    sTitle = sTitle.replace(sYear,'')
                siteUrl = aEntry[2].replace('"','')
                sInfo = sNote

                sInfo = '[COLOR yellow]'+sInfo+'[/COLOR]'
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
  
def showSeasons2():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()       
    sPattern =  '<a href="http([^<]+)/watch/(.+?)"'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
             m3url =  'http'+aEntry[0]+'/watch/' + aEntry[1]
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
    
    oParser = cParser()
    # .+? ([^<]+)
    sPattern = '<a href="([^<]+)".+?class="download-link"'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
    
            sTitle = '[COLOR yellow]link[/COLOR]'
            siteUrl = aEntry
            sThumbnail = sThumbnail
            sInfo = ""
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
       
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    # .+? ([^<]+) (.+?)
               

    sPattern = 'src="(.+?)".+?type='
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
            for aEntry in aResult[1]:            
                sHosterUrl = aEntry
                sTitle = sMovieTitle
                if sHosterUrl.startswith('//'):
                   sHosterUrl = 'http:' + sHosterUrl
            
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                   oHoster.setDisplayName(sMovieTitle)
                   oHoster.setFileName(sMovieTitle)
                   cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				                
    oGui.setEndOfDirectory()