# Amira Script

proc getvsa {file} {
    # Create a label stack from the binary MRC stack
    create auto_threshold "Auto Thresholding"
    "Auto Thresholding" inputImage connect $file
    "Auto Thresholding" doIt hit
    "Auto Thresholding" fire

    # Create surface from the label stack
    create HxGMC "Generate Surface"
    "Generate Surface" data connect $file.labels
    "GenerateSurface" smoothing setValue 3 #Unconstrained smoothing
    "GenerateSurface" options setValue 0 1
    "GenerateSurface" options setValue 1 1
    "GenerateSurface" border setValue 0 1
    "Generate Surface" action snap
    "Generate Surface" fire

    # Remesh surface
    create HxRemeshSurface "Remesh Surface"
    "Remesh Surface" data connect $file.surf
    "Remesh Surface" objective setValue 1
    "Remesh Surface" desiredSize setValue 2 50
    "Remesh Surface" interpolateOrigSurface setValue 0
    "Remesh Surface" remesh snap
    "Remesh Surface" fire
    
    # Output statistics (volume, surface area)
    create HxSurfaceArea "Surface Area"
    "Surface Area" data connect $file.remeshed
    "Surface Area" action snap
    "Surface Area" fire
}

proc getskl {file} {
    # Create CenterlineTree skeleton object. Make sure the parameters are set 
    # to their default values.
    create HxTEASAR "Centerline Tree"
    "Centerline Tree" data connect $file
    "Centerline Tree" tubesParams setValue 0 2.5
    "Centerline Tree" tubesParams setValue 1 4
    "Centerline Tree" numParts setValue -1
    "Centerline Tree" options setValue 0 1
    "Centerline Tree" doIt snap
    "Centerline Tree" fire
    
    # Smooth the skeleton. Create a Smooth module and connect it to the 
    # skeleton. Set the smoothing parameters to 0.7 and 0.2. These seem to 
    # yield the best results for isotropic data.
    create HxSmoothLine "Smooth"
    "Smooth" lineSet connect $file.Spatial-Graph
    "Smooth" coefficients setValues 0.7 0.2
    "Smooth" numberOfIterations setValue 10
    "Smooth" doIt snap
    "Smooth" fire
   
    # Output statistics (branch length and number of nodes)
    create HxSpatialGraphStats "Spatial Graph Statistics"
    "Spatial Graph Statistics" data connect SmoothTree.spatialgraph
    "Spatial Graph Statistics" doIt snap
    "Spatial Graph Statistics" fire
}

proc saveimg {file} {
    # Make the surface transparent
    create HxDisplaySurface "Surface View"
    "Surface View" data connect $file.remeshed
    "Surface View" drawStyle setValue 4
    "Surface View" fire

    # Make the skeleton red and enlarge the node spheres a little
    create HxSpatialGraphView "Spatial Graph View"
    "Spatial Graph View" data connect SmoothTree.spatialgraph
    "Spatial Graph View" segmentColor setColor 0 1 0 0
    "Spatial Graph View" fire
    "Spatial Graph View" nodeScaleFactor setValue 200
    "Spatial Graph View" fire

    # Take the snapshot
    viewer 0 setSize 640 480
    viewer 0 snapshot wholeCellAnalytics/$file.png
}


###
### MAIN
###

set files_mrc [glob wholeCellAnalytics/*mitochondrion.mrc]

foreach file $files_mrc {
    set base [file tail $file]
    set base [string trimright $base ".mrc"]
    [ load $file ] setLabel $base
    getvsa $base
    getskl $base
    #saveimg $base
    $base.statistics save "CSV" wholeCellAnalytics/${base}_vsa.csv
    SmoothTree.statistics save "CSV" wholeCellAnalytics/${base}_skl.csv
    $base.remeshed save "HxSurface binary" wholeCellAnalytics/${base}_srf.surf
    SmoothTree.spatialgraph save "AmiraMesh ASCII SpatialGraph" wholeCellAnalytics/${base}_skl.am
    remove -all
}

