# Amira Script
remove -all
remove {physics.icol} {grey.am} {mito_branched.mrc} {mito_branched.Labels} {mito_branched.SpatialGraph.am} {mito_branched.surf} {mito_branched.remeshed.surf} {SmoothTree.spatialgraph.am} {SmoothTree.statistics.am} {OrthoSlice} {BoundingBox} {LabelVoxel} {CenterlineTree} {SurfaceGen} {RemeshSurface} {SurfaceView} {Smooth} {SpatialGraphView} {SpatialGraphStatistics}

# Create viewers
viewer setVertical 0

viewer 0 setBackgroundMode 0
viewer 0 setBackgroundColor 1 1 1
viewer 0 setBackgroundColor2 0.4 0.4 0.4
viewer 0 setTransparencyType 5
viewer 0 setAutoRedraw 0
viewer 0 show
mainWindow show

set hideNewModules 1
[ load ${AMIRA_ROOT}/data/colormaps/physics.icol ] setLabel physics.icol
{physics.icol} setIconPosition 0 0
{physics.icol} setNoRemoveAll 1
{physics.icol} fire
{physics.icol} setMinMax 0 1
{physics.icol} {flags} setValue 1
{physics.icol} {shift} setMinMax -1 1
{physics.icol} {shift} setButtons 0
{physics.icol} {shift} setIncrement 0.133333
{physics.icol} {shift} setValue 0
{physics.icol} {shift} setSubMinMax -1 1
{physics.icol} {scale} setMinMax 0 1
{physics.icol} {scale} setButtons 0
{physics.icol} {scale} setIncrement 0.1
{physics.icol} {scale} setValue 1
{physics.icol} {scale} setSubMinMax 0 1
physics.icol fire
physics.icol setViewerMask 16383

set hideNewModules 1
[ load ${AMIRA_ROOT}/data/colormaps/grey.am ] setLabel grey.am
{grey.am} setIconPosition 0 0
{grey.am} setNoRemoveAll 1
{grey.am} fire
{grey.am} setMinMax 0 255
{grey.am} {flags} setValue 1
{grey.am} {shift} setMinMax -1 1
{grey.am} {shift} setButtons 0
{grey.am} {shift} setIncrement 0.133333
{grey.am} {shift} setValue 0
{grey.am} {shift} setSubMinMax -1 1
{grey.am} {scale} setMinMax 0 1
{grey.am} {scale} setButtons 0
{grey.am} {scale} setIncrement 0.1
{grey.am} {scale} setValue 1
{grey.am} {scale} setSubMinMax 0 1
grey.am fire
grey.am setViewerMask 16383

set hideNewModules 0
[ load ${SCRIPTDIR}/mito_branched.mrc ] setLabel mito_branched.mrc
{mito_branched.mrc} setIconPosition 20 10
mito_branched.mrc fire
mito_branched.mrc setViewerMask 16383

set hideNewModules 0
[ load ${SCRIPTDIR}/SmoothTree.spatialgraph.am ] setLabel SmoothTree.spatialgraph.am
{SmoothTree.spatialgraph.am} setIconPosition 48 281
SmoothTree.spatialgraph.am setTransform 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1
SmoothTree.spatialgraph.am fire
SmoothTree.spatialgraph.am setViewerMask 16383

set hideNewModules 0
create {HxOrthoSlice} {OrthoSlice}
{OrthoSlice} setIconPosition 227 10
{OrthoSlice} {data} connect mito_branched.mrc
{OrthoSlice} fire
{OrthoSlice} {sliceOrientation} setValue 0
{OrthoSlice} fire
{OrthoSlice} {origin}  setBoundingBox -1e+08 1e+08 -1e+08 1e+08 -1e+08 1e+08
{OrthoSlice} {origin}  setImmediate 0
{OrthoSlice} {origin}  setOrtho 0
{OrthoSlice} {origin}  showDragger 0
{OrthoSlice} {origin}  showPoints 0
{OrthoSlice} {origin}  setPointScale 1
{OrthoSlice} {origin}  showOptionButton 1
{OrthoSlice} {origin}  setNumPoints 1 1 1
{OrthoSlice} {origin}  setValue 0 14133.1 11689.5 13786
{OrthoSlice} {normal}  setBoundingBox -1e+08 1e+08 -1e+08 1e+08 -1e+08 1e+08
{OrthoSlice} {normal}  setImmediate 0
{OrthoSlice} {normal}  setOrtho 0
{OrthoSlice} {normal}  showDragger 0
{OrthoSlice} {normal}  showPoints 0
{OrthoSlice} {normal}  setPointScale 1
{OrthoSlice} {normal}  showOptionButton 1
{OrthoSlice} {normal}  setNumPoints 1 1 1
{OrthoSlice} {normal}  setValue 0 0 0 1
{OrthoSlice} {options} setValue 0 1
OrthoSlice options setToggleVisible 0 1
{OrthoSlice} {options} setValue 1 0
OrthoSlice options setToggleVisible 1 1
{OrthoSlice} {options} setValue 2 0
OrthoSlice options setToggleVisible 2 1
{OrthoSlice} {options} setValue 3 0
OrthoSlice options setToggleVisible 3 1
{OrthoSlice} {mapping} setIndex 0 1
{OrthoSlice} {contrastLimit} setMinMax 0 -2147483648 2147483648
{OrthoSlice} {contrastLimit} setValue 0 7
{OrthoSlice} {colormap} setDefaultColor 1 0.8 0.5
{OrthoSlice} {colormap} setDefaultAlpha 1.000000
{OrthoSlice} {colormap} setLocalRange 1
{OrthoSlice} {colormap} setLocalMinMax 0.000000 1.000000
{OrthoSlice} {colormap} connect grey.am
{OrthoSlice} {sliceNumber} setMinMax 0 46
{OrthoSlice} {sliceNumber} setButtons 1
{OrthoSlice} {sliceNumber} setIncrement 1
{OrthoSlice} {sliceNumber} setValue 46
{OrthoSlice} {sliceNumber} setSubMinMax 0 46
{OrthoSlice} {transparency} setValue 0
{OrthoSlice} fire
{OrthoSlice} {frameSettings} setState item 0 1 item 2 1 color 3 1 0.5 0 
{OrthoSlice} fire

OrthoSlice fire
OrthoSlice setViewerMask 16382
OrthoSlice setShadowStyle 0
OrthoSlice setPickable 1

set hideNewModules 0
create {HxBoundingBox} {BoundingBox}
{BoundingBox} setIconPosition 405 10
{BoundingBox} {data} connect mito_branched.mrc
{BoundingBox} fire
{BoundingBox} {options} setState item 0 0 color 1 1 0.5 0 item 3 0 
{BoundingBox} {lineWidth} setMinMax 1 10
{BoundingBox} {lineWidth} setButtons 0
{BoundingBox} {lineWidth} setIncrement 1
{BoundingBox} {lineWidth} setValue 1
{BoundingBox} {lineWidth} setSubMinMax 1 10
{BoundingBox} {font} setState name: {Helvetica} size: 12 bold: 0 italic: 0 color: 0.8 0.8 0.8
BoundingBox fire
BoundingBox setViewerMask 16383
BoundingBox setShadowStyle 0
BoundingBox setPickable 1

set hideNewModules 0
create {HxLabelVoxel} {LabelVoxel}
{LabelVoxel} setIconPosition 265 67
{LabelVoxel} {data} connect mito_branched.mrc
{LabelVoxel} fire
{LabelVoxel} {regions} setState {Exterior Inside}
{LabelVoxel} {boundary01} setMinMax 0 1
{LabelVoxel} {boundary01} setButtons 1
{LabelVoxel} {boundary01} setIncrement 10
{LabelVoxel} {boundary01} setValue 0
{LabelVoxel} {boundary01} setSubMinMax 0 1
{LabelVoxel} {boundary12} setMinMax 0 1
{LabelVoxel} {boundary12} setButtons 1
{LabelVoxel} {boundary12} setIncrement 10
{LabelVoxel} {boundary12} setValue 1
{LabelVoxel} {boundary12} setSubMinMax 0 1
{LabelVoxel} {boundary23} setMinMax 0 1
{LabelVoxel} {boundary23} setButtons 1
{LabelVoxel} {boundary23} setIncrement 10
{LabelVoxel} {boundary23} setValue 1
{LabelVoxel} {boundary23} setSubMinMax 0 1
{LabelVoxel} {boundary34} setMinMax 0 1
{LabelVoxel} {boundary34} setButtons 1
{LabelVoxel} {boundary34} setIncrement 10
{LabelVoxel} {boundary34} setValue 1
{LabelVoxel} {boundary34} setSubMinMax 0 1
{LabelVoxel} {options} setValue 0 0
LabelVoxel options setToggleVisible 0 1
{LabelVoxel} {options} setValue 1 0
LabelVoxel options setToggleVisible 1 1
{LabelVoxel} {options} setValue 2 0
LabelVoxel options setToggleVisible 2 1
LabelVoxel fire
LabelVoxel setViewerMask 16383
LabelVoxel setPickable 1

set hideNewModules 0
[ {LabelVoxel} create
 ] setLabel {mito_branched.Labels}
{mito_branched.Labels} setIconPosition 20 30
{mito_branched.Labels} {master} connect LabelVoxel
{mito_branched.Labels} {ImageData} connect mito_branched.mrc
{mito_branched.Labels} fire
{mito_branched.Labels} {primary} setIndex 0 0
mito_branched.Labels fire
mito_branched.Labels setViewerMask 16383

set hideNewModules 0
create {HxTEASAR} {CenterlineTree}
{CenterlineTree} setIconPosition 127 140
{CenterlineTree} {data} connect mito_branched.Labels
{CenterlineTree} fire
{CenterlineTree} {maps} setValue 0 0
CenterlineTree maps setToggleVisible 0 1
{CenterlineTree} {maps} setValue 1 0
CenterlineTree maps setToggleVisible 1 1
{CenterlineTree} {maps} setValue 2 0
CenterlineTree maps setToggleVisible 2 1
{CenterlineTree} {maps} setValue 3 0
CenterlineTree maps setToggleVisible 3 1
{CenterlineTree} {tubesParams} setMinMax 0 -3.40282346638529e+38 3.40282346638529e+38
{CenterlineTree} {tubesParams} setValue 0 2.5
{CenterlineTree} {tubesParams} setMinMax 1 -3.40282346638529e+38 3.40282346638529e+38
{CenterlineTree} {tubesParams} setValue 1 4
{CenterlineTree} {numParts} setMinMax 0 -2147483648 2147483648
{CenterlineTree} {numParts} setValue 0 -1
{CenterlineTree} {options} setValue 0 1
CenterlineTree options setToggleVisible 0 1
{CenterlineTree} {options} setValue 1 1
CenterlineTree options setToggleVisible 1 1
{CenterlineTree} {root}  setBoundingBox -999 29265.2 0 23378.9 -14 13786
{CenterlineTree} {root}  setImmediate 0
{CenterlineTree} {root}  setOrtho 0
{CenterlineTree} {root}  showDragger 0
{CenterlineTree} {root}  showPoints 0
{CenterlineTree} {root}  setPointScale 1
{CenterlineTree} {root}  showOptionButton 1
{CenterlineTree} {root}  setNumPoints 1 -1 -1
{CenterlineTree} {root}  setValue 0 0 0 0
CenterlineTree fire
CenterlineTree setViewerMask 16383
CenterlineTree setPickable 1

set hideNewModules 0
[ load ${SCRIPTDIR}/mito_branched.SpatialGraph.am ] setLabel mito_branched.SpatialGraph.am
{mito_branched.SpatialGraph.am} setIconPosition 26 219
{mito_branched.SpatialGraph.am} {master} connect CenterlineTree
mito_branched.SpatialGraph.am fire
mito_branched.SpatialGraph.am setViewerMask 16383

set hideNewModules 0
create {HxGMC} {SurfaceGen}
{SurfaceGen} setIconPosition 78 466
{SurfaceGen} {data} connect mito_branched.mrc
{SurfaceGen} fire
{SurfaceGen} {smoothing} setIndex 0 3
{SurfaceGen} {options} setValue 0 1
SurfaceGen options setToggleVisible 0 1
{SurfaceGen} {options} setValue 1 1
SurfaceGen options setToggleVisible 1 1
{SurfaceGen} {border} setValue 0 1
SurfaceGen border setToggleVisible 0 1
{SurfaceGen} {border} setValue 1 0
SurfaceGen border setToggleVisible 1 1
{SurfaceGen} {minEdgeLength} setMinMax 0 0 0.800000011920929
{SurfaceGen} {minEdgeLength} setValue 0 0.800000011920929
{SurfaceGen} {materialList} setIndex 0 0
{SurfaceGen} {smoothMaterial} setIndex 0 2
SurfaceGen fire
SurfaceGen setViewerMask 16383
SurfaceGen setPickable 1

set hideNewModules 0
[ load ${SCRIPTDIR}/mito_branched-files/mito_branched.surf ] setLabel mito_branched.surf
{mito_branched.surf} setIconPosition 54 487
{mito_branched.surf} {master} connect SurfaceGen
{mito_branched.surf} fire
{mito_branched.surf} {LevelOfDetail} setMinMax -1 -1
{mito_branched.surf} {LevelOfDetail} setButtons 1
{mito_branched.surf} {LevelOfDetail} setIncrement 1
{mito_branched.surf} {LevelOfDetail} setValue -1
{mito_branched.surf} {LevelOfDetail} setSubMinMax -1 -1
mito_branched.surf setTransform 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1
mito_branched.surf fire
mito_branched.surf setViewerMask 16383

set hideNewModules 0
create {HxRemeshSurface} {RemeshSurface}
{RemeshSurface} setIconPosition 66 509
{RemeshSurface} {data} connect mito_branched.surf
{RemeshSurface} fire
{RemeshSurface} fire
{RemeshSurface} fire
{RemeshSurface} {advancedOptions} setValue 0 0
RemeshSurface advancedOptions setToggleVisible 0 1
{RemeshSurface} {objective} setIndex 0 1
{RemeshSurface} {triangleArea} setMinMax 0 -2147483648 2147483648
{RemeshSurface} {triangleArea} setValue 0 5
{RemeshSurface} {triangleArea} setMinMax 1 -2147483648 2147483648
{RemeshSurface} {triangleArea} setValue 1 3
{RemeshSurface} {triangleArea} setMinMax 2 -2147483648 2147483648
{RemeshSurface} {triangleArea} setValue 2 3
{RemeshSurface} {vertexValence} setMinMax 0 -2147483648 2147483648
{RemeshSurface} {vertexValence} setValue 0 1
{RemeshSurface} {triangleQuality} setMinMax 0 -2147483648 2147483648
{RemeshSurface} {triangleQuality} setValue 0 10
{RemeshSurface} {lloydRelaxation} setMinMax 0 -2147483648 2147483648
{RemeshSurface} {lloydRelaxation} setValue 0 40
{RemeshSurface} {desiredSize} setMinMax 0 -2147483648 2147483648
{RemeshSurface} {desiredSize} setValue 0 2012
{RemeshSurface} {desiredSize} setMinMax 1 -2147483648 2147483648
{RemeshSurface} {desiredSize} setValue 1 4024
{RemeshSurface} {desiredSize} setMinMax 2 1 100
{RemeshSurface} {desiredSize} setValue 2 1
{RemeshSurface} {errorThresholds} setMinMax 0 -3.40282346638529e+38 3.40282346638529e+38
{RemeshSurface} {errorThresholds} setValue 0 0
{RemeshSurface} {errorThresholds} setMinMax 1 -3.40282346638529e+38 3.40282346638529e+38
{RemeshSurface} {errorThresholds} setValue 1 0
{RemeshSurface} {densityContrast} setMinMax 0 -3.40282346638529e+38 3.40282346638529e+38
{RemeshSurface} {densityContrast} setValue 0 0
{RemeshSurface} {densityRange} setMinMax 0 -3.40282346638529e+38 3.40282346638529e+38
{RemeshSurface} {densityRange} setValue 0 145.904846191406
{RemeshSurface} {densityRange} setMinMax 1 -3.40282346638529e+38 3.40282346638529e+38
{RemeshSurface} {densityRange} setValue 1 8796055273472
{RemeshSurface} {interpolateOrigSurface} setValue 0
{RemeshSurface} {remeshOptions1} setValue 0 0
RemeshSurface remeshOptions1 setToggleVisible 0 1
{RemeshSurface} {remeshOptions1} setValue 1 1
RemeshSurface remeshOptions1 setToggleVisible 1 1
{RemeshSurface} {surfacePathOptions} setValue 0 0
RemeshSurface surfacePathOptions setToggleVisible 0 1
{RemeshSurface} {surfacePathOptions} setValue 1 1
RemeshSurface surfacePathOptions setToggleVisible 1 1
{RemeshSurface} {remeshOptions2} setValue 0
{RemeshSurface} {contourLayers} setMinMax 0 -2147483648 2147483648
{RemeshSurface} {contourLayers} setValue 0 4
{RemeshSurface} fire
RemeshSurface fire
RemeshSurface setViewerMask 16383
RemeshSurface setPickable 1

set hideNewModules 0
[ load ${SCRIPTDIR}/mito_branched-files/mito_branched.remeshed.surf ] setLabel mito_branched.remeshed.surf
{mito_branched.remeshed.surf} setIconPosition 18 531
{mito_branched.remeshed.surf} {master} connect RemeshSurface
{mito_branched.remeshed.surf} fire
{mito_branched.remeshed.surf} {LevelOfDetail} setMinMax -1 -1
{mito_branched.remeshed.surf} {LevelOfDetail} setButtons 1
{mito_branched.remeshed.surf} {LevelOfDetail} setIncrement 1
{mito_branched.remeshed.surf} {LevelOfDetail} setValue -1
{mito_branched.remeshed.surf} {LevelOfDetail} setSubMinMax -1 -1
mito_branched.remeshed.surf fire
mito_branched.remeshed.surf setViewerMask 16383

set hideNewModules 0
create {HxDisplaySurface} {SurfaceView}
{SurfaceView} setIconPosition 250 534
{SurfaceView} {data} connect mito_branched.remeshed.surf
{SurfaceView} {colormap} setDefaultColor 1 0.1 0.1
{SurfaceView} {colormap} setDefaultAlpha 0.500000
{SurfaceView} {colormap} setLocalRange 0
{SurfaceView} fire
{SurfaceView} {drawStyle} setValue 4
{SurfaceView} fire
{SurfaceView} {drawStyle} setSpecularLighting 1
{SurfaceView} {drawStyle} setTexture 1
{SurfaceView} {drawStyle} setAlphaMode 3
{SurfaceView} {drawStyle} setNormalBinding 0
{SurfaceView} {drawStyle} setSortingMode 1
{SurfaceView} {drawStyle} setLineWidth 0.000000
{SurfaceView} {drawStyle} setOutlineColor 0 0 0.2
{SurfaceView} {textureWrap} setIndex 0 1
{SurfaceView} {cullingMode} setValue 0
{SurfaceView} {selectionMode} setIndex 0 0
{SurfaceView} {Patch} setMinMax 0 4
{SurfaceView} {Patch} setButtons 1
{SurfaceView} {Patch} setIncrement 1
{SurfaceView} {Patch} setValue 0
{SurfaceView} {Patch} setSubMinMax 0 4
{SurfaceView} {BoundaryId} setIndex 0 -1
{SurfaceView} {materials} setIndex 0 1
{SurfaceView} {materials} setIndex 1 0
{SurfaceView} {colorMode} setIndex 0 0
{SurfaceView} {baseTrans} setMinMax 0 1
{SurfaceView} {baseTrans} setButtons 0
{SurfaceView} {baseTrans} setIncrement 0.1
{SurfaceView} {baseTrans} setValue 0.8
{SurfaceView} {baseTrans} setSubMinMax 0 1
{SurfaceView} {VRMode} setIndex 0 0
{SurfaceView} fire
{SurfaceView} hideBox 1
{SurfaceView} selectTriangles zab HIJMPLPPHPBEIMDEMAMAPPPPDPAAEDBBPECJ
SurfaceView fire
SurfaceView setViewerMask 16383
SurfaceView setShadowStyle 0
SurfaceView setPickable 1

set hideNewModules 0
create {HxSmoothLine} {Smooth}
{Smooth} setIconPosition 160 247
{Smooth} {lineSet} connect mito_branched.SpatialGraph.am
{Smooth} fire
{Smooth} {coefficients} setMinMax 0 -3.40282346638529e+38 3.40282346638529e+38
{Smooth} {coefficients} setValue 0 0.699999988079071
{Smooth} {coefficients} setMinMax 1 -3.40282346638529e+38 3.40282346638529e+38
{Smooth} {coefficients} setValue 1 0.200000002980232
{Smooth} {numberOfIterations} setMinMax 0 -2147483648 2147483648
{Smooth} {numberOfIterations} setValue 0 10
Smooth fire
Smooth setViewerMask 16383
Smooth setPickable 1

set hideNewModules 0
create {HxSpatialGraphView} {SpatialGraphView}
{SpatialGraphView} setIconPosition 277 282
{SpatialGraphView} {data} connect SmoothTree.spatialgraph.am
{SpatialGraphView} {nodeColormap} setDefaultColor 1 0.8 0.5
{SpatialGraphView} {nodeColormap} setDefaultAlpha 0.500000
{SpatialGraphView} {nodeColormap} setLocalRange 0
{SpatialGraphView} {nodeColormap} connect physics.icol
{SpatialGraphView} {segmentColormap} setDefaultColor 1 0.8 0.5
{SpatialGraphView} {segmentColormap} setDefaultAlpha 0.500000
{SpatialGraphView} {segmentColormap} setLocalRange 0
{SpatialGraphView} {segmentColormap} connect physics.icol
{SpatialGraphView} fire
{SpatialGraphView} {itemsToShow} setValue 0 1
SpatialGraphView itemsToShow setToggleVisible 0 1
{SpatialGraphView} {itemsToShow} setValue 1 1
SpatialGraphView itemsToShow setToggleVisible 1 1
{SpatialGraphView} {nodeScale} setIndex 0 0
{SpatialGraphView} {nodeScaleFactor} setMinMax 0 2883
{SpatialGraphView} {nodeScaleFactor} setButtons 0
{SpatialGraphView} {nodeScaleFactor} setIncrement 192.2
{SpatialGraphView} {nodeScaleFactor} setValue 340.23
{SpatialGraphView} {nodeScaleFactor} setSubMinMax 0 2883
{SpatialGraphView} {nodeColoring} setIndex 0 0
{SpatialGraphView} {nodeLabelColoringOptions} setValue 0
{SpatialGraphView} {nodeColor} setColor 0 0.304348 1 0
{SpatialGraphView} {nodeColor} setAlpha 0 -1
{SpatialGraphView} {segmentStyle} setValue 0 1
SpatialGraphView segmentStyle setToggleVisible 0 1
{SpatialGraphView} {segmentStyle} setValue 1 0
SpatialGraphView segmentStyle setToggleVisible 1 1
{SpatialGraphView} {segmentStyle} setValue 2 0
SpatialGraphView segmentStyle setToggleVisible 2 1
{SpatialGraphView} {tubeScale} setIndex 0 0
{SpatialGraphView} {tubeScaleFactor} setMinMax 0 10
{SpatialGraphView} {tubeScaleFactor} setButtons 0
{SpatialGraphView} {tubeScaleFactor} setIncrement 0.666667
{SpatialGraphView} {tubeScaleFactor} setValue 0.2
{SpatialGraphView} {tubeScaleFactor} setSubMinMax 0 10
{SpatialGraphView} {segmentWidth} setMinMax 0 10
{SpatialGraphView} {segmentWidth} setButtons 0
{SpatialGraphView} {segmentWidth} setIncrement 0.666667
{SpatialGraphView} {segmentWidth} setValue 1
{SpatialGraphView} {segmentWidth} setSubMinMax 0 10
{SpatialGraphView} {segmentColoring} setIndex 0 0
{SpatialGraphView} {segmentLabelColoringOptions} setValue 0
{SpatialGraphView} {segmentColor} setColor 0 1 0 0
{SpatialGraphView} {segmentColor} setAlpha 0 -1
{SpatialGraphView} {pointSize} setMinMax 0 15
{SpatialGraphView} {pointSize} setButtons 0
{SpatialGraphView} {pointSize} setIncrement 1
{SpatialGraphView} {pointSize} setValue 4
{SpatialGraphView} {pointSize} setSubMinMax 0 15
{SpatialGraphView} setVisibility HIJMPLPPPPPPHPAAAJPKADPN HIJMPLPPPPPPHPAAAJPKADPN
SpatialGraphView fire
SpatialGraphView setViewerMask 16383
SpatialGraphView setPickable 1

set hideNewModules 0
create {HxSpatialGraphStats} {SpatialGraphStatistics}
{SpatialGraphStatistics} setIconPosition 139 332
{SpatialGraphStatistics} {data} connect SmoothTree.spatialgraph.am
{SpatialGraphStatistics} fire
{SpatialGraphStatistics} {output} setValue 0 1
SpatialGraphStatistics output setToggleVisible 0 1
{SpatialGraphStatistics} {output} setValue 1 1
SpatialGraphStatistics output setToggleVisible 1 1
SpatialGraphStatistics fire
SpatialGraphStatistics setViewerMask 16383
SpatialGraphStatistics setPickable 1

set hideNewModules 0
[ load ${SCRIPTDIR}/SmoothTree.statistics.am ] setLabel SmoothTree.statistics.am
{SmoothTree.statistics.am} setIconPosition 147 369
{SmoothTree.statistics.am} {master} connect {SpatialGraphStatistics} 0
{SmoothTree.statistics.am} fire
SmoothTree.statistics.am fire
SmoothTree.statistics.am setViewerMask 16383
SmoothTree.statistics.am select

set hideNewModules 0


viewer 0 setCameraOrientation 0.996107 -0.0797549 0.0375605 4.54812
viewer 0 setCameraPosition 19788.5 57002 -605.403
viewer 0 setCameraFocalDistance 46274.4
viewer 0 setCameraNearDistance 31774.8
viewer 0 setCameraFarDistance 60754.5
viewer 0 setCameraType orthographic
viewer 0 setCameraHeight 26926.5
viewer 0 setAutoRedraw 1
viewer 0 redraw

