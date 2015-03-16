# Amira Script

proc getvsa {file base} {
    # Create surface from the MRC stack of binary labels
    create {HxGMC} {SurfaceGen}
    SurfaceGen data connect $file
    SurfaceGen smoothing setValue 3
    SurfaceGen options setValue 0 1
    SurfaceGen options setValue 1 1
    SurfaceGen border setValue 0 1
    SurfaceGen action snap
    SurfaceGen fire

    # Remesh surface
    create {HxRemeshSurface} {RemeshSurface}
    RemeshSurface data connect $base.surf
    RemeshSurface objective setValue 1
    RemeshSurface desiredSize setValue 2 50
    RemeshSurface interpolateOrigSurface setValue 0
    RemeshSurface remesh snap
    RemeshSurface fire
    
    # Output statistics (volume, surface area)
    create {HxSurfaceArea} {SurfaceArea}
    SurfaceArea data connect $base.remeshed
    SurfaceArea action snap
    SurfaceArea fire
}

proc getskl {file base} {
    # Create CenterlineTree skeleton object. Make sure the parameters are set 
    # to their default values.
    create {HxTEASAR} {CenterlineTree}
    CenterlineTree data connect $file
    CenterlineTree tubesParams setValue 0 2.5
    CenterlineTree tubesParams setValue 1 4
    CenterlineTree numParts setValue -1
    CenterlineTree options setValue 0 1
    CenterlineTree doIt snap
    CenterlineTree fire
    
    # Smooth the skeleton. Create a Smooth module and connect it to the 
    # skeleton. Set the smoothing parameters to 0.7 and 0.2. These seem to 
    # yield the best results for isotropic data.
    create {HxSmoothLine} {Smooth}
    Smooth lineSet connect $base.SpatialGraph
    Smooth coefficients setValues 0.7 0.2
    Smooth numberOfIterations setValue 10
    Smooth doIt snap
    Smooth fire
   
    # Output statistics (branch length and number of nodes)
    create {HxSpatialGraphStats} {SpatialGraphStatistics}
    SpatialGraphStatistics data connect SmoothTree.spatialgraph
    SpatialGraphStatistics doIt snap
    SpatialGraphStatistics fire
}

proc saveimg {file base} {
    # Make the surface transparent
    SurfaceView drawStyle setValue 4
    SurfaceView fire

    # Make the skeleton red and enlarge the node spheres a little
    create {HxSpatialGraphView} {SpatialGraphView}
    SpatialGraphView data connect SmoothTree.spatialgraph
    SpatialGraphView segmentColor setColor 0 1 0 0
    SpatialGraphView fire
    SpatialGraphView nodeScaleFactor setValue 200	
    SpatialGraphView fire

    # Take the snapshot
    viewer 0 snapshot -offscreen 640 480 $base.png
}


###
### MAIN
###

set files_mrc [glob wholeCellAnalytics/*mitochondrion.mrc]

foreach file $files_mrc {
    set base [file tail $file]
    set base [string trimright $base ".mrc"]
    [ load $file ] setLabel $file
    getvsa $file $base
    getskl $file $base
    #saveimg $file $base
    $base.statistics save "CSV" wholeCellAnalytics/${base}_vsa.csv
    SmoothTree.statistics save "CSV" wholeCellAnalytics/${base}_skl.csv
    $base.remeshed save "HxSurface binary" wholeCellAnalytics/${base}_srf.surf
    #$base.remeshed save "Open Inventor" ${base}_surf.iv
    SmoothTree.spatialgraph save "AmiraMesh ASCII SpatialGraph" wholeCellAnalytics/${base}_skl.am
    remove -all
}

