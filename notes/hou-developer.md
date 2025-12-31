# Developer Houdini Plugin 
### Version 0.1 
### Author: Lucas Galante
### Document Updated: December 2025

# Outline

Developer operators are combined in SOP solver and DOP contexts in Houdini. Creating lifelike elements in digital containers.


# Looking Ahead 

## Attributes Or Groups?
    
This question easily leads into the larger topic of how data is stored for dynamical operations. There are two main types of data in Shapeshifter:
### 1. Live data
Fluid data which runs like a stream through the simulation.

### 2. Derivative data
Data calculated anew every frame. It is calculated based on live data.

## Regions
    
After making the GEM mold operators, I am more experienced with treating a model as a composite of distinct parts and overlapping attributes. It has also helped me visualize what a developed form with distinct surface regions can look like and how the regions might evolve during the model's life. The idea of regions in a model reminds me of organs which fit together physically and programmatically.

It is interesting to consider how regions in a model are like programmatic elements in architecture and ecology. These are both structures where multiple functions are built into a one body. Disease may spread through a limb and leave a trail of evidence or destroy its host. Living models host mechanisms which influence their status. Viruses can travel within their host in directions informed by sense input and change the host's nature depending on where they travel. Morphogen gradients are interesting because they demonstrate how distribution of matter on one scale can influence form on another scale.

Another property of a living model is how definitively its boundaries are defined. Before they are really there, the boundary of a living model is predictable. It requires an environment which supplies the real elements of itself, but information about where those elements will go is present ahead of time.

## Operator Categorirs

### Pre-Simulation
The embryo or seed is created, initial selections and value assignments are made, attributes that will be used are introduced and initial conditions are set. Pre-simulation operators define the characteristics and landscape of a simulation before it runs. Attribute templates and starting geometry are supplied to be fed into the simulation network.

### Simulation Attribute Operators
Value operators operate on simulation attributes which are present for the entire simulation.Simulation attributes are persistent from the end of one frame to the beginning of another.

### Development Attribute Operators
During this stage of the simulation network, simulation attributes are composited into development attributes. Development attributes are cleared at the end of each frame and need to be constructed from the same corresponding simulation attributes for every frame. Development attributes tell the surface development operators how the surface will change.

### Surface Development Operators
Surface Development Operators read development attributes and use that information to transform the mesh or volume. Aside from position and normal, attributes are untouched. At this point, Value assignments remain the same until the next frame.

### Meshing Operators
Once the geometry has been deformed, meshing operators are the final step in the simulation process.Meshing operators adjust the topology of geometry. This ensures that the number of data points in a mesh is always proportional to ts surface area. The surface is remeshed to keep make primitives and points conform to some regular formation.

### Attributes
Most attributes are assigned to the geometry instance in the preparation phase.
Attributes belong to categories based on their function.

### Age
Values have ages which are affected by a few different criteria.
    
    Increment
      - 1
      - The value of the attribute\
      - Some factor of a scale / normalized value

      Reset 
		- 


## Larger Ideas

### Development
To effectively develop this package, categories need to be created which

### Topological Considerations
At this point in time, the Shapeshifter operator package is primarily concerned with the surface of digital models. Unlike many other approaches to similar design queries its operators involve direct analysis and development of closed forms, not an underlying network or structure to which is later assigned volume. 
    
### Operator Categorization
Nodes are distributed into categories based on their function. Nodes which operate on or output scalar or vector attributes are separated. The reason for this is simplifying the development of nodes. Nodes with more complex options are more difficult to modify, and because a holistic vision for the inerface hasn't materialized, it's easier to keep them separated, at least for now.

### Geometry Classes

#### Vertices
As of yet there aren't any well-defined use cases for vertex attributes.    

#### Points
The majority of nodes operate on point attributes. The keystone of shapeshifter is the develop and remesh node pair. The develop node requires point attributes to modify the topology of surfaces over time, so it makes sense to focuse primarily on point attributes.

#### Primitives
If a clear use-case for primitive attributes becomes clear.  

#### Detail
Global attributes are useful for storing statistics and analyses.

## Operator Categories

### Scalar
Scalar nodes which edit the values of scalar attributes.

### Vector
Vector sodes which edit the values of vector attributes.

### Surface
Surface nodes utilize input attributes to alter the topology of the geometry.

### Volume
Volume nodes modify volumes that exist in tandem with mesh geometry. Volume nodes are not fleshed out and need very basic development.

Looking ahead idea #1: Volumes can be reservoirs of value when a vector directs value to flow either inside of (Shapeshifter Core.) the geometry or away from the surface of the geometry (Shapeshifter Miasma.)


# Operators

## Scalar Analysis
Analyze poperties of scalar attributes.

Analysis attributes provide specific information about scalar attributes.

Analyses can be toggled on and off in the operator's parameter interface.

Some analyses are per-point, and others are operations involving sets of points.

## Scalar Composite
Combine attributes in different configurations.

Will likely be combined with "Scalar Combine".

## Scalar Combine
Combines attributes using different methods.

### Looking Ahead
A standard Attribute Combine operator is shipped with Houdini. It has several interesting options, so it is not clear if the Shapeshifter version should be kept in the package.

## Scalar Concentrate
Similar in function to "Scalar Diffuse", only in reverse.    

###  Looking Ahead
It's possible that this operator can be replaced by setting "Scalar Diffuse" to a negative number.

## Scalar Diffuse
Diffuses attribute values over a surface.

## Scalar Initialize
Pre-sim: Initializes attributes that will be used during simulation.

## Scalar Map

## Scalar Migrate 

##  Scalar Normalize 
    
## Scalar Ramp 

## Scalar Weight

## Submute Begin 

## Submute End 

## Lead 

## Vector Analysis

## Vector Composite 

## Vector Conform 

## Vector Diffuse 

## Vector Direct 

## Vector From Scalar 

## Vector Migrate 

## Vector Normalize 

## Vector Rotate 

## Vector Unify 

## Vector Weight 

## Surface Adapt

## Surface Open 

## Surface Suture 

## Subdivide 

## Remesh 

## Detangle 
      
## Develop 

## Time 

## Time Ramp 

## Time Switch

## Solver 

## Region (Tentative) 

## Analyze (Tentative) 

## Vitality 

## Edge Analysis 

## Analyze Change 

## Volume/Miasma

## Volume/Core

## Filter/Select

## Region/Region Center 

## Attribute/Promote 

## Visualize/Panel

## ID

## Age/Expire

## Energize 

## Create/Embryo

## Filter/Cull

## Combine

## Constant

## Measure 
      
## Metamax (Irrelevant?)
