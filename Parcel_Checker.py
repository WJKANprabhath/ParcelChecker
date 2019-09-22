# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ParcelChecker
                                 A QGIS plugin
 To convert cad plan to shapfile
                              -------------------
        begin                : 2019-09-16
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Prabhath W.J.K.A.N. Survey Dept. of Sri Lanka
        email                : npjasinghe@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from Parcel_Checker_dialog import ParcelCheckerDialog
import os.path
from qgis.core import*
from qgis.utils import *
from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
import os, sys, datetime
import qgis
import processing
class ParcelChecker:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ParcelChecker_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        self.dlg = ParcelCheckerDialog()



        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&1 Parcel Checker')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'ParcelChecker')
        self.toolbar.setObjectName(u'ParcelChecker')
        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.select_input_file)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ParcelChecker', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        #self.dlg = ParcelCheckerDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ParcelChecker/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Check the parcels V0.1'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&1 Parcel Checker'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def select_input_file(self):
        filename = QFileDialog.getOpenFileName(self.dlg, "Select input file","",'*.dxf')
        self.dlg.lineEdit.setText(filename)


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            #-----clear
            cLayer = iface.mapCanvas().currentLayer()
            QgsMapLayerRegistry.instance().removeMapLayer( cLayer)
            cLayer = iface.mapCanvas().currentLayer()
            QgsMapLayerRegistry.instance().removeMapLayer( cLayer)
            
            line_Dxf = self.dlg.lineEdit.text()
	    db=os.path.expanduser('~\\.qgis2\\python\\plugins\\ParcelChecker\\qgis.dbf')
            outputs_QGISEXPLODELINES_1=processing.runalg('qgis:explodelines', line_Dxf,None)
            outputs_GRASS7VCLEAN_1=processing.runalg('grass7:v.clean', outputs_QGISEXPLODELINES_1['OUTPUT'] ,1,0.001,('0,2000,0,2000'),-1.0,0.0001,None,None)
            outputs_GRASS7VCLEAN_2=processing.runalg('grass7:v.clean', outputs_GRASS7VCLEAN_1['output'],0,0.001,('0,2000,0,2000'),-1.0,0.0001,None,None)
            outputs_QGISFIELDCALCULATOR_1=processing.runalg('qgis:fieldcalculator', outputs_GRASS7VCLEAN_2['output'],'ex',0,10.0,4.0,True,'$length',None)
            outputs_QGISJOINATTRIBUTESTABLE_1=processing.runandload('qgis:joinattributestable', outputs_QGISFIELDCALCULATOR_1['OUTPUT_LAYER'],db,'layer','layer',None)
      
            #---- ---------------iface activity--------------------------------------
            cLayer = iface.mapCanvas().currentLayer()
            expr = QgsExpression("ex=0")
            it = cLayer.getFeatures( QgsFeatureRequest( expr ) )
            ids = [i.id() for i in it]
            cLayer.setSelectedFeatures( ids )
            cLayer.startEditing()
            for fid in ids:
                cLayer.deleteFeature(fid)
            cLayer.commitChanges()

            #---- ---------------iface activity 02--------------------------------------

            cLayer = iface.mapCanvas().currentLayer()
            expr = QgsExpression( " \"layer_2\" is NULL" )
            it = cLayer.getFeatures( QgsFeatureRequest( expr ) )
            ids = [i.id() for i in it]
            cLayer.setSelectedFeatures( ids )
            cLayer.startEditing()
            for fid in ids:
                cLayer.deleteFeature(fid)
            cLayer.commitChanges()
            #------------------
            cLayer = iface.mapCanvas().currentLayer()
            layer = self.iface.activeLayer()
            myfilepath= iface.activeLayer().dataProvider().dataSourceUri()
            QgsMapLayerRegistry.instance().removeMapLayer( cLayer)
            layer = QgsVectorLayer(myfilepath,os.path.basename(line_Dxf[:-4]), 'ogr')
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            cLayer = iface.mapCanvas().currentLayer()
            outputs_QGISPOLYGONIZE_1=processing.runalg('qgis:polygonize', cLayer,False,True,None)
            outputs_QGISPOINTONSURFACE_1=processing.runandload('qgis:pointonsurface', line_Dxf,None)
            cLayer = iface.mapCanvas().currentLayer()
            expr = QgsExpression( " \"Layer\" is not 'LOTNO'" )
            it = cLayer.getFeatures( QgsFeatureRequest( expr ) )
            ids = [i.id() for i in it]
            cLayer.setSelectedFeatures( ids )
            cLayer.startEditing()
            for fid in ids:
                cLayer.deleteFeature(fid)
            cLayer.commitChanges()
            outputs_QGISJOINATTRIBUTESBYLOCATION_1=processing.runandload('qgis:joinattributesbylocation', outputs_QGISPOLYGONIZE_1['OUTPUT'],cLayer,['contains'],0.0,0,'sum,mean,min,max,median',1,None)
            b= r""+line_Dxf[:-4]+"Report01.txt"           
            file = open(b, 'w')
            cLayer = iface.mapCanvas().currentLayer()
            
            #------------------------------------------------------------------------
            cLayer = iface.mapCanvas().currentLayer()
            layer = self.iface.activeLayer()
            myfilepath= iface.activeLayer().dataProvider().dataSourceUri()                

            outputs_QGISDISSOLVE_2=processing.runandload('qgis:dissolve', cLayer,False,'Text',None)
            layer = self.iface.activeLayer()
            myfilepath2= iface.activeLayer().dataProvider().dataSourceUri()                
            QgsMapLayerRegistry.instance().removeMapLayer(cLayer)

            outputs_QGISDISSOLVE_3=processing.runandload('qgis:dissolve', myfilepath,False,'Text',None)

            #---- ---------------iface activity 03--------------------------------------

            cLayer = iface.mapCanvas().currentLayer()
            expr = QgsExpression( " \"Layer\" is NULL" )
            it = cLayer.getFeatures( QgsFeatureRequest( expr ) )
            ids = [i.id() for i in it]
            cLayer.setSelectedFeatures( ids )
            cLayer.startEditing()
            for fid in ids:
                cLayer.deleteFeature(fid)
            cLayer.commitChanges()

            feats_count = cLayer.featureCount()
            file.write('----------Processed result of the plan--------"\n')
            file.write('\nNo of Lots              ')
            file.write(str(feats_count))
            #-----------------------------------------------------------------------------------------
            cLayer = iface.mapCanvas().currentLayer()
            layer = self.iface.activeLayer()
            QgsMapLayerRegistry.instance().removeMapLayer(cLayer)
            cLayer = iface.mapCanvas().currentLayer()
            QgsMapLayerRegistry.instance().removeMapLayer( cLayer)
            cLayer = iface.mapCanvas().currentLayer()
            QgsMapLayerRegistry.instance().removeMapLayer( cLayer)
            layer = QgsVectorLayer(myfilepath,os.path.basename(line_Dxf[:-4]), 'ogr')
            QgsMapLayerRegistry.instance().addMapLayer(layer)

            #---- ---------------iface activity 05--------------------------------------
            cLayer = iface.mapCanvas().currentLayer()
            expr = QgsExpression(" \"area\" is 0")
            it = cLayer.getFeatures( QgsFeatureRequest( expr ) )
            ids = [i.id() for i in it]
            cLayer.setSelectedFeatures( ids )
            cLayer.startEditing()
            for fid in ids:
                cLayer.deleteFeature(fid)
            cLayer.commitChanges()

            count1=cLayer.featureCount()
            file.write('\nNo of Polygons          ')
            file.write(str(count1))
            expr = QgsExpression( " \"Text\" is NULL" )
            it = cLayer.getFeatures( QgsFeatureRequest( expr ) )
            ids = [i.id() for i in it]
            cLayer.setSelectedFeatures( ids )
            count2=len(ids)
            file.write('\nNo of Polygons unloted  ')
            file.write(str(count2))

            if  str(count1 < count2):
                file.write ('\nplease numbered the unloted lots and re do the processed ')
            now = datetime.datetime.now()
            date= str (now)
            a1= str (now.strftime("%Y-%m-%d"))
            file.write ("\nDate : "+ a1+"\n")

            file.write ('\n------------------------- R&D @ SGO ------------------------')

            file.close()
            layer = iface.activeLayer()
            layer.setCustomProperty("labeling", "pal")
            layer.setCustomProperty("labeling/enabled", "true")
            layer.setCustomProperty("labeling/fontFamily", "Arial")
            layer.setCustomProperty("labeling/fontSize", "10")
            layer.setCustomProperty("labeling/fieldName", "Text")
            layer.setCustomProperty("labeling/placement", "4")
            iface.mapCanvas().refresh()
            from PyQt4.QtGui import*
            window = iface.mainWindow()
            QMessageBox.information(window,"Info", "Process complete....!\n \n (if unloted polygon exist, dont goto the next step)")
            
            pass
 
