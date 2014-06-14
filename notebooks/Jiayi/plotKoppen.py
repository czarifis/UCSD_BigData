def plotKoppenMap(joined):    
    # http://matplotlib.org/basemap/users/merc.html

    from mpl_toolkits.basemap import Basemap
    import numpy as np
    import matplotlib.pyplot as plt


    longitudes=joined.ix[:,'longitude'].values

    latitudes=joined.ix[:,'latitude'].values
    label = joined.ix[:,'Cls'].values
    lonmin=-180;lonmax=180;latsmin=-80;latsmax=80;
    plt.figure(figsize=(15,10),dpi=3000)
    m = Basemap(projection='merc',llcrnrlat=latsmin,urcrnrlat=latsmax,\
                llcrnrlon=lonmin,urcrnrlon=lonmax,lat_ts=20,resolution='i')
    m.drawcoastlines()
    #m.fillcontinents(color='coral',lake_color='aqua')

    # draw parallels and meridians.
    parallels = np.arange(-80,81,10.)
    # labels = [left,right,top,bottom]
    m.drawparallels(parallels,labels=[False,True,True,False])
    meridians = np.arange(10.,351.,20.)
    m.drawmeridians(meridians,labels=[True,False,False,True])

    #m.drawparallels(np.arange(-90.,91.,30.))
    #m.drawmeridians(np.arange(-180.,181.,60.))
    #m.drawmapboundary(fill_color='aqua')


    xCfa = xCfb = xCfc = xDfa = xDfb = xDfd = xDfd = xAf = xAm = xAw = xBWh = xBWk = xBSh = xBSk = []
    xCsa = xCsb = xCwa = xCwb = xCwc = xDsa = xDsb = xDsc = xDsd = []
    xDwa = xDwb = xDwc = xDwd = xET = xEF = xDfc = []
    yCfa = yCfb = yCfc = yDfa = yDfb = yDfc = yDfd = yAf = yAm = yAw = yBWh = yBWk = yBSh = yBSk = []
    yCsa = yCsb = yCwa = yCwb = yCwc = yDsa = yDsb = yDsc = yDsd = []
    yDwa = yDwb = yDwc = yDwd = yET = yEF = yDfc = []

    for i in range(len(label)):
    # draw map with markers for locations
        if label[i]=='Cfa': #c8fe00
            xCfa.append(longitudes[i])
            yCfa.append(latitudes[i])
        elif label[i]=='Cfb': #70fd00
            xCfb.append(longitudes[i])
            yCfb.append(latitudes[i])
        elif label[i]=='Cfc': #43c600
            xCfc.append(longitudes[i])
            yCfc.append(latitudes[i])
        elif label[i]=='Af': #0000ff
            xAf.append(longitudes[i])
            yAf.append(latitudes[i])
        elif label[i]=='Am': #0070ff
            xAm.append(longitudes[i])
            yAm.append(latitudes[i])
        elif label[i]=='Aw': #3ba8ff
            xAw.append(longitudes[i])
            yAw.append(latitudes[i])
        elif label[i]=='BWh': #fa1d00
            xBWh.append(longitudes[i])
            yBWh.append(latitudes[i])
        elif label[i]=='BWk': #fb9793
            xBWk.append(longitudes[i])
            yBWk.append(latitudes[i])
        elif label[i]=='BSh': #f5a400
            xBSh.append(longitudes[i])
            yBSh.append(latitudes[i])
        elif label[i]=='BSk': #fedb49
            xBSk.append(longitudes[i])
            yBSk.append(latitudes[i])
        elif label[i]=='Csa': #feff00
            xCsa.append(longitudes[i])
            yCsa.append(latitudes[i])
        elif label[i]=='Csb': #cfcd00
            xCsb.append(longitudes[i])
            yCsb.append(latitudes[i])
        elif label[i]=='Cwa': #9afe8a
            xCwa.append(longitudes[i])
            yCwa.append(latitudes[i])
        elif label[i]=='Cwb': #66c756
            xCwb.append(longitudes[i])
            yCwb.append(latitudes[i])
        elif label[i]=='Cwc': #3d961a
            xCwc.append(longitudes[i])
            yCwc.append(latitudes[i])
        elif label[i]=='Dsa': #f70bff
            xDsa.append(longitudes[i])
            yDsa.append(latitudes[i])
        elif label[i]=='Dsb': #c507cb
            xDsb.append(longitudes[i])
            yDsb.append(latitudes[i])
        elif label[i]=='Dsc': #95339b
            xDsc.append(longitudes[i])
            yDsc.append(latitudes[i])
        elif label[i]=='Dsd': #8c5d95
            xDsd.append(longitudes[i])
            yDsd.append(latitudes[i])
        elif label[i]=='Dwa': #a4aeff
            xDwa.append(longitudes[i])
            yDwa.append(latitudes[i])
        elif label[i]=='Dwb': #4676ea
            xDwb.append(longitudes[i])
            yDwb.append(latitudes[i])
        elif label[i]=='Dwc': #444cba
            xDwc.append(longitudes[i])
            yDwc.append(latitudes[i])
        elif label[i]=='Dwd': #2b008f
            xDwd.append(longitudes[i])
            yDwd.append(latitudes[i])
        elif label[i]=='Dfa': #2df9fc
            xDfa.append(longitudes[i])
            yDfa.append(latitudes[i])
        elif label[i]=='Dfb': #42c4ff
            xDfb.append(longitudes[i])
            yDfb.append(latitudes[i])
        elif label[i]=='Dfc': #0f7d7e
            xDfc.append(longitudes[i])
            yDfc.append(latitudes[i])
        elif label[i]=='Dfd': #034664
            xDfd.append(longitudes[i])
            yDfd.append(latitudes[i])
        elif label[i]=='ET': #aeb0ad
            xET.append(longitudes[i])
            yET.append(latitudes[i])
        elif label[i]=='EF': #686967
            xEF.append(longitudes[i])
            yEF.append(latitudes[i])


    #x, y = m(longitudes,latitudes)
    x, y = m(xCfa,yCfa)
    m.scatter(x,y,color = '#c8fe00', marker = '.')

    x, y = m(xCfb,yCfb)
    m.plot(x,y,color = '#70fd00', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xCfc,yCfc)
    m.plot(x,y,color = '#43c600', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xAf,yAf)
    m.plot(x,y,color = '#0000ff', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xAm,yAm)
    m.plot(x,y,color = '#0070ff', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xAw,yAw)
    m.plot(x,y,color = '#3ba8ff', linestyle = 'None', marker = '.', markersize=0.3)



    x, y = m(xCsb,yCsb)
    m.plot(x,y,color = '#cfcd00', linestyle = 'None', marker = '.',markersize=0.3)

    x, y = m(xCwa,yCwa)
    m.plot(x,y,color = '#9afe8a', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xCwb,yCwb)
    m.plot(x,y,color = '#66c756', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xCwc,yCwc)
    m.plot(x,y,color = '#3d961a', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xDsa,yDsa)
    m.plot(x,y,color = '#f70bff', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xDsb,yDsb)
    m.plot(x,y,color = '#c507cb', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xDsc,yDsc)
    m.plot(x,y,color = '#95339b', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xDsd,yDsd)
    m.plot(x,y,color = '#8c5d95', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xDwa,yDwa)
    m.plot(x,y,color = '#a4aeff', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xDwb,yDwb)
    m.plot(x,y,color = '#4676ea', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xDwc,yDwc)
    m.plot(x,y,color = '#444cba', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xDwd,yDwd)
    m.plot(x,y,color = '#2b008f', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xDfa,yDfa)
    m.plot(x,y,color = '#2df9fc', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xDfb,yDfb)
    m.plot(x,y,color = '#42c4ff', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xDfc,yDfc)
    m.plot(x,y,color = '#0f7d7e', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xDfd,yDfd)
    m.plot(x,y,color = '#034664', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xET,yET)
    ho, = m.plot(x,y,color = '#aeb0ad', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xEF,yEF)
    hh, = m.plot(x,y,color = '#686967', linestyle = 'None', marker = '.', markersize=0.3)


    x, y = m(xBSh,yBSh)
    h, = m.plot(x,y,color = '#f5a400', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xBSk,yBSk)
    a, = m.plot(x,y,color = '#fedb49', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xCsa,yCsa)
    l, = m.plot(x,y,color = '#feff00', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xBWh,yBWh)
    ll, = m.plot(x,y,color = '#fa1d00', linestyle = 'None', marker = '.', markersize=0.3)

    x, y = m(xBWk,yBWk)
    lo, = m.plot(x,y,color = '#fb9793', linestyle = 'None', marker = '.', markersize=0.3)



    plt.title('weather stations grouped into regions')
    plt.show()