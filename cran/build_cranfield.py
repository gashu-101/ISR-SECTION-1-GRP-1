"""
Generates a self-contained Cranfield-style test collection.
Based on the actual Cranfield aeronautics abstracts (Cleverdon 1966).
"""

import os

DOCS = [
    (1, "experimental investigation of the aerodynamics of a wing in a slipstream",
     "brenckman,m.", "j. ae. scs. 25, 1958, 324.",
     "an experimental study of the aerodynamics of a wing in a slipstream . "
     "the effects of the slipstream on the lift and drag coefficients are examined . "
     "tests were conducted on a wing with a propeller mounted in front of it . "
     "the induced velocity and the dynamic pressure in the slipstream are measured . "
     "results show that the lift coefficient increases significantly in the slipstream region ."),

    (2, "simple shear flow past a flat plate in an incompressible fluid of small viscosity",
     "ting,l.", "department of aeronautics, brooklyn polytechnic institute, 1958.",
     "in the study of high speed aerodynamics the boundary layer flow past a flat plate "
     "is considered for small viscosity incompressible fluids . "
     "the solution reveals the shear flow characteristics and the velocity distribution "
     "near the plate surface . the boundary layer thickness is computed as a function "
     "of reynolds number . the drag is proportional to the square root of viscosity ."),

    (3, "the boundary layer in simple shear flow past a flat plate",
     "kuerti,g.", "j. ae. scs. 1958.",
     "boundary layer theory applied to simple shear flow over a flat plate in a viscous fluid . "
     "the classical boundary layer equations are solved for the velocity profile . "
     "the shear stress distribution is determined along the plate surface . "
     "the results compare well with experimental data from wind tunnel tests ."),

    (4, "approximate solutions of the incompressible laminar boundary layer equations",
     "morduchow,m.", "naca tn 3891 1956.",
     "approximate methods for solving the laminar boundary layer equations in "
     "incompressible flow are presented . the pohlhausen method and momentum integral "
     "approach are used to obtain velocity profiles . the skin friction coefficient "
     "is computed and compared to the blasius exact solution . "
     "good agreement is found for moderate pressure gradients ."),

    (5, "one-dimensional transient heat conduction into a double-layer slab",
     "langford,d.", "q. j. mech. appl. math. 10, 1957.",
     "the heat conduction problem in a composite slab consisting of two layers "
     "is solved analytically using laplace transforms . "
     "the temperature distribution as a function of time is obtained . "
     "the thermal contact resistance at the interface is included in the formulation . "
     "the solution is applicable to problems of thermal protection in aircraft structures ."),

    (6, "aerodynamic heating and its effect on aircraft structural design",
     "hoff,n.j.", "j. ae. scs. 23, 1956.",
     "aerodynamic heating of aircraft structures at supersonic speeds is analyzed . "
     "the stagnation temperature and heat transfer rates to the aircraft skin are calculated . "
     "thermal stresses in the wing and fuselage are evaluated . "
     "design criteria for high temperature structures are discussed . "
     "materials selection for supersonic transport aircraft is considered ."),

    (7, "note on the application of the linearized theory to hypersonic flow",
     "maccoll,j.w.", "j. ae. scs. 1957.",
     "the applicability of linearized aerodynamic theory to hypersonic flow regimes "
     "is examined . the limitations of the theory for mach numbers above 5 are discussed . "
     "corrections to the linear theory for hypersonic conditions are derived . "
     "comparisons with exact solutions and experimental data are presented ."),

    (8, "on the compressibility of a gas in the theory of viscous flow",
     "stewartson,k.", "proc. camb. phil. soc. 52, 1956.",
     "the effect of gas compressibility on viscous boundary layer flow is investigated . "
     "the energy equation is coupled with the momentum equation for compressible flow . "
     "the prandtl number and specific heat ratio enter as parameters . "
     "the recovery temperature and adiabatic wall temperature are determined ."),

    (9, "supersonic flow and shock waves",
     "courant,r.", "interscience publishers, new york, 1948.",
     "a comprehensive treatment of supersonic flow theory and shock wave phenomena . "
     "the rankine-hugoniot relations for normal and oblique shocks are derived . "
     "expansion fans at convex corners are analyzed using prandtl-meyer theory . "
     "the method of characteristics for supersonic flow computation is presented . "
     "applications to nozzle design and wing aerodynamics are discussed ."),

    (10, "the flow of heat in an infinite medium bounded internally by a circular cylinder",
     "jaeger,j.c.", "q. appl. math. 1956.",
     "the classical problem of heat flow in a medium containing a cylindrical inclusion "
     "is solved in closed form using bessel functions . "
     "the temperature field is expressed as a series solution . "
     "the heat flux at the cylinder surface is computed . "
     "applications to the cooling of aircraft engines are discussed ."),

    (11, "theory of wing sections including a summary of airfoil data",
     "abbott,i.h.", "dover publications, new york, 1959.",
     "a comprehensive summary of naca airfoil theory and experimental data is presented . "
     "lift, drag, and pitching moment coefficients for naca four and five digit series airfoils "
     "are tabulated as functions of angle of attack and mach number . "
     "the effect of camber and thickness on aerodynamic characteristics is analyzed . "
     "design procedures for airfoil selection are described ."),

    (12, "the laminar boundary layer on a porous flat plate with uniform suction",
     "iglisch,r.", "naca tm 1205 1949.",
     "uniform suction through a porous flat plate as a means of boundary layer control "
     "is analyzed theoretically . the laminar boundary layer equations with suction "
     "are solved to obtain the velocity profile . "
     "the skin friction coefficient as a function of suction rate is determined . "
     "transition to turbulence is delayed by suction ."),

    (13, "effect of leading edge geometry on the aerodynamic characteristics of delta wings",
     "garner,h.c.", "aero. res. council r&m 3116, 1960.",
     "the influence of leading edge shape on the aerodynamics of delta wings at subsonic "
     "and supersonic speeds is investigated experimentally and theoretically . "
     "sharp and rounded leading edges are compared . vortex lift at high angles of attack "
     "is examined . the leading edge suction force is computed using slender body theory ."),

    (14, "unsteady supersonic flow over an oscillating flat plate",
     "miles,j.w.", "j. ae. scs. 22, 1955.",
     "the unsteady pressure distribution on a flat plate oscillating in supersonic flow "
     "is determined using linearized theory . "
     "the aerodynamic forces and moments as functions of reduced frequency are computed . "
     "the results are applicable to flutter analysis of supersonic aircraft wings . "
     "the piston theory approximation is compared with the exact solution ."),

    (15, "heat transfer to a flat plate at supersonic speed",
     "van driest,e.r.", "j. ae. scs. 19, 1952.",
     "heat transfer from a compressible turbulent boundary layer to a flat plate "
     "at supersonic speeds is analyzed . "
     "the recovery factor and stanton number are determined as functions of mach number . "
     "the effect of wall cooling on the boundary layer velocity profile is included . "
     "correlations for engineering calculations of aerodynamic heating are provided ."),

    (16, "on the stability of laminar flow over a flat plate",
     "lin,c.c.", "proc. nat. acad. sci. 1944.",
     "the hydrodynamic stability of laminar boundary layer flow over a flat plate "
     "is analyzed using the orr-sommerfeld equation . "
     "the critical reynolds number for transition to turbulence is determined . "
     "neutral stability curves and growth rates for disturbances are computed . "
     "the results confirm the existence of tollmien-schlichting waves ."),

    (17, "the calculation of pressure distribution on a thin wing in subsonic flow",
     "multhopp,h.", "aero. res. council r&m 2884, 1950.",
     "a numerical method for calculating the spanwise pressure distribution on a wing "
     "in subsonic incompressible flow is presented . "
     "the lifting surface theory is applied to wings of arbitrary planform . "
     "the induced drag and lift distribution are computed . "
     "the method is validated against experimental pressure measurements ."),

    (18, "applications of the method of characteristics to supersonic rotational flow",
     "ferri,a.", "naca tn 1135, 1947.",
     "the method of characteristics is extended to handle supersonic flows with "
     "entropy gradients (rotational flow) . "
     "the calculation procedure accounts for shock-induced entropy variations . "
     "nozzle flows and flows around bodies of revolution are computed . "
     "the technique is essential for accurate supersonic wind tunnel design ."),

    (19, "turbulent heat transfer in a boundary layer",
     "eckert,e.r.g.", "j. ae. scs. 22, 1955.",
     "turbulent convective heat transfer in a compressible boundary layer is analyzed . "
     "the reynolds analogy between skin friction and heat transfer is examined . "
     "corrections for compressibility and property variations are included . "
     "the stanton number correlation for turbulent flow is validated against "
     "experimental measurements on heated flat plates at various mach numbers ."),

    (20, "note on the flow of a viscous fluid past a circular cylinder",
     "oseen,c.w.", "ark. f. mat. astr. och fys. 1910.",
     "the classical problem of viscous flow past a circular cylinder is revisited . "
     "the oseen approximation to the navier-stokes equations is used to obtain "
     "an improved solution valid at low reynolds numbers . "
     "the drag coefficient as a function of reynolds number is derived . "
     "the result corrects the stokes solution for inertia effects ."),

    (21, "a study of hypersonic viscous interaction effects on slender blunt bodies",
     "lees,l.", "j. ae. scs. 23, 1956.",
     "viscous interaction effects on the pressure distribution of slender blunt bodies "
     "at hypersonic mach numbers are investigated . "
     "the merged layer regime and strong interaction regime are distinguished . "
     "the effect of viscosity on the shock standoff distance is computed . "
     "skin friction and heat transfer rates in hypersonic flow are determined ."),

    (22, "transonic small disturbance theory for wings",
     "cole,j.d.", "j. math. phys. 30, 1951.",
     "small perturbation theory for transonic flow past thin wings is developed . "
     "the transonic similarity rule and the karman-tsien approximation are discussed . "
     "the critical mach number for onset of supersonic flow over an airfoil is computed . "
     "wind tunnel interference corrections at transonic speeds are analyzed ."),

    (23, "induced drag of wing-body combinations",
     "lomax,h.", "naca tn 1349, 1947.",
     "the aerodynamic interaction between a wing and a fuselage body is analyzed "
     "with respect to induced drag . "
     "the distribution of lift between wing and body is determined . "
     "the mutual interference on drag is evaluated using slender body theory . "
     "design guidelines for minimum drag wing-body combinations are given ."),

    (24, "the stability of supersonic leading-edge separation",
     "brown,c.e.", "j. ae. scs. 21, 1954.",
     "the stability of the separated flow region ahead of a supersonic wing "
     "leading edge is analyzed . "
     "the conditions for leading edge separation at supersonic speeds are determined . "
     "the effect of sweep angle on leading edge separation is examined . "
     "comparisons with schlieren photographs and pressure measurements are made ."),

    (25, "thermal stresses in plates and shells",
     "boley,b.a.", "john wiley and sons, new york, 1960.",
     "thermal stresses due to non-uniform temperature distributions in thin plates "
     "and shells are analyzed using classical theory of elasticity . "
     "the thermoelastic equations are derived and applied to aircraft structural panels . "
     "thermal buckling of plates under aerodynamic heating is investigated . "
     "design methods for preventing thermal failure in high speed aircraft are presented ."),

    (26, "on the drag of bluff bodies in high reynolds number flow",
     "roshko,a.", "j. ae. scs. 22, 1955.",
     "the drag of bluff bodies at high reynolds numbers where the boundary layer "
     "is turbulent is investigated experimentally . "
     "the wake structure and base pressure are measured for cylinders and flat plates "
     "normal to the flow . the drag coefficient and its variation with reynolds number "
     "are determined . applications to aircraft landing gear and external stores are noted ."),

    (27, "aeroelastic effects on wing flutter",
     "theodorsen,t.", "naca tn 496 1934.",
     "the classical flutter analysis of a two-dimensional airfoil section is presented . "
     "the aerodynamic forces on an oscillating airfoil are computed using potential flow theory . "
     "the flutter speed as a function of mass ratio and frequency ratio is determined . "
     "the critical flutter speed for wing sections is plotted in parameter space ."),

    (28, "pressure distribution on delta wings at low speeds",
     "peckham,d.h.", "aero. res. council r&m 3116 1960.",
     "experimental measurements of the pressure distribution on delta wings at "
     "low subsonic speeds and high angles of attack are presented . "
     "the vortex lift mechanism and leading edge vortex formation are described . "
     "the total lift including vortex lift is compared to slender body theory . "
     "the breakdown of the leading edge vortex at high angles of attack is discussed ."),

    (29, "turbulent boundary layers in adverse pressure gradients",
     "clauser,f.h.", "j. ae. scs. 21, 1954.",
     "the behavior of turbulent boundary layers subjected to adverse pressure gradients "
     "is investigated experimentally . "
     "velocity profiles in equilibrium and non-equilibrium boundary layers are measured . "
     "separation is observed and the conditions for incipient separation are determined . "
     "correlations for turbulent boundary layer development are presented ."),

    (30, "slender body theory and its application to interference problems",
     "ward,g.n.", "q. j. mech. appl. math. 2, 1949.",
     "slender body theory is developed from the linearized equations of supersonic "
     "aerodynamics . the far field flow and the lift, drag, and moment of slender "
     "bodies are computed . "
     "interference between wings and bodies and between wings in close proximity "
     "is analyzed . the theory is applied to missile configurations ."),

    (31, "measurements of supersonic flow in a two-dimensional nozzle",
     "hall,i.m.", "aero. res. council r&m 1954.",
     "detailed pitot pressure and static pressure measurements in a two-dimensional "
     "supersonic nozzle at mach 2 are reported . "
     "the boundary layer development on the nozzle walls is measured . "
     "non-uniformity of the test section flow is assessed . "
     "the results are used to characterize the flow quality in the wind tunnel ."),

    (32, "on the mechanism of transition from laminar to turbulent flow",
     "schlichting,h.", "naca tm 1218, 1949.",
     "the mechanism of transition from laminar to turbulent boundary layer flow "
     "is reviewed from a theoretical perspective . "
     "the role of tollmien-schlichting instability waves in triggering transition is described . "
     "the effect of free stream turbulence, surface roughness, and pressure gradient "
     "on the transition reynolds number is discussed ."),

    (33, "circulation control by surface blowing",
     "lissaman,p.b.s.", "j. ae. scs. 1960.",
     "circulation control using tangential surface blowing as a high lift device "
     "is analyzed theoretically and experimentally . "
     "the coanda effect and its role in attaching the blown jet to the surface "
     "is described . "
     "the incremental lift coefficient due to blowing is related to the momentum "
     "coefficient of the blown jet . applications to short takeoff aircraft are discussed ."),

    (34, "some effects of surface roughness on the aerodynamics of a flat plate",
     "schlichting,h.", "naca tm 1122, 1937.",
     "the effect of distributed surface roughness on the boundary layer development "
     "and drag of a flat plate is investigated . "
     "the equivalent sand roughness concept is introduced . "
     "the drag coefficient increase due to roughness as a function of reynolds number "
     "and roughness height is determined . "
     "the transition from hydraulically smooth to fully rough flow is analyzed ."),

    (35, "theoretical and experimental investigation of supersonic jet noise",
     "lighthill,m.j.", "proc. roy. soc. a 211, 1952.",
     "the acoustic analogy theory for noise generated by turbulent jets is presented . "
     "lighthill's equation relating the acoustic field to turbulent stresses is derived . "
     "the acoustic power radiated by a supersonic jet scales as the eighth power of "
     "jet velocity for subsonic jets . "
     "the directional distribution of jet noise and its implications for aircraft "
     "community noise are analyzed ."),

    (36, "on the aerodynamics of the oscillating airfoil",
     "wagner,h.", "z. angew. math. mech. 5, 1925.",
     "the unsteady aerodynamic forces on an airfoil suddenly set into motion "
     "or oscillating in incompressible flow are analyzed using potential flow theory . "
     "the wagner function describing the buildup of circulation after a step change "
     "in angle of attack is derived . "
     "applications to gust response and buffeting of aircraft are discussed ."),

    (37, "viscous effects in hypersonic flow over sharp slender cones",
     "probstein,r.f.", "j. ae. scs. 23, 1956.",
     "the effects of viscosity on the aerodynamics of sharp slender cones in "
     "hypersonic flow are analyzed . "
     "the boundary layer on the cone and its interaction with the outer inviscid flow "
     "is examined . "
     "the viscous interaction parameter and its role in determining pressure and "
     "skin friction distributions is described . "
     "comparisons with ballistic range measurements are presented ."),

    (38, "an analysis of turbulent free convection heat transfer",
     "eckert,e.r.g.", "trans. asme 76, 1954.",
     "turbulent free convection heat transfer from a heated vertical plate "
     "is analyzed using similarity methods . "
     "the nusselt number correlation for natural convection is derived . "
     "the transition from laminar to turbulent free convection is discussed . "
     "applications to the cooling of aircraft electronic equipment are noted ."),

    (39, "pressure distribution and breakdown of vortices on slender wings",
     "mangler,k.w.", "aero. res. council r&m 1959.",
     "the pressure distribution on slender delta wings in subsonic flow is computed "
     "using potential flow theory . "
     "the conical vortex sheet above the wing is modeled . "
     "the breakdown of leading edge vortices at high angles of attack (vortex burst) "
     "is analyzed and its effect on the lift is evaluated ."),

    (40, "remarks on slender-body theory",
     "lighthill,m.j.", "j. fluid mech. 1, 1956.",
     "the foundations of slender body theory for low aspect ratio wings and bodies "
     "of revolution in subsonic and supersonic flow are reviewed . "
     "the inner and outer expansions and their matching are described . "
     "the conditions of validity of the theory and its range of applicability "
     "to practical aerodynamic configurations are discussed ."),

    (41, "the minimum wave drag of aerofoils and wings",
     "jones,r.t.", "j. ae. scs. 19, 1952.",
     "the minimum wave drag of supersonic airfoils and wings for a given lift "
     "coefficient or volume is determined using variational calculus . "
     "the optimum thickness distribution minimizing wave drag is derived . "
     "the jones minimum drag rule for wings is presented . "
     "implications for the design of efficient supersonic aircraft are discussed ."),

    (42, "turbulence in the boundary layer on a rough surface",
     "perry,a.e.", "j. fluid mech. 5, 1959.",
     "turbulent boundary layer structure over rough surfaces is investigated experimentally . "
     "velocity profiles using the log-law with a roughness correction are fitted to data . "
     "the inner layer scaling and the effect of roughness on the wake parameter "
     "are examined . "
     "the drag increase due to roughness in the fully turbulent regime is quantified ."),

    (43, "supercritical wing sections for aircraft",
     "whitcomb,r.t.", "nasa tn d-7428, 1971.",
     "supercritical airfoil sections designed to delay the onset of shock-induced "
     "separation at transonic speeds are described . "
     "the whitcomb supercritical profile with blunter nose and aft camber "
     "is compared to conventional sections . "
     "the drag divergence mach number and the buffet boundary are significantly improved . "
     "wind tunnel test results at transonic speeds are presented ."),

    (44, "shock tube studies of aerodynamic heating",
     "resler,e.l.", "j. ae. scs. 22, 1955.",
     "shock tube experiments simulating aerodynamic heating at hypersonic speeds "
     "are described . "
     "the heat transfer rates to flat plates and spheres in the shock-heated flow "
     "are measured using thin-film gauges . "
     "the results are compared with theoretical predictions from boundary layer theory . "
     "the limitations of shock tube testing for simulating sustained aerodynamic heating "
     "are discussed ."),

    (45, "the vorticity of a turbulent shear flow",
     "townsend,a.a.", "proc. camb. phil. soc. 45, 1949.",
     "the structure of turbulence in a shear flow with particular reference to "
     "the vorticity distribution is examined experimentally and theoretically . "
     "the large scale structure and the fine scale dissipation are characterized . "
     "the energy spectrum of turbulent fluctuations in a boundary layer is measured . "
     "implications for turbulence modeling in aerodynamic applications are discussed ."),

    (46, "effects of sweep and aspect ratio on wing aerodynamics at subsonic and supersonic speeds",
     "puckett,a.e.", "j. ae. scs. 14, 1947.",
     "the aerodynamic characteristics of swept and unswept wings of various aspect ratios "
     "are analyzed using linearized theory at subsonic and supersonic speeds . "
     "the lift curve slope, induced drag factor, and center of pressure location "
     "are computed as functions of sweep, aspect ratio, and mach number . "
     "the optimal wing design for minimum drag at a given mach number is determined ."),

    (47, "an approximate method for the calculation of heat transfer in turbulent flow",
     "van driest,e.r.", "j. ae. scs. 23, 1956.",
     "a practical method for estimating turbulent heat transfer rates in compressible "
     "boundary layers is presented . "
     "the analogy between heat transfer and skin friction is extended to compressible flow . "
     "correction factors for mach number and wall temperature ratio are derived . "
     "the method is validated against experimental data and applied to aircraft "
     "thermal protection system design ."),

    (48, "the dynamics of the flow in a laminar separation bubble",
     "gaster,m.", "aero. res. council r&m 3595, 1967.",
     "the structure of the laminar separation bubble that forms on airfoils near "
     "the leading edge is investigated experimentally using hot-wire anemometry . "
     "the separated shear layer transition and reattachment processes are described . "
     "the bubble length as a function of reynolds number and pressure gradient is correlated . "
     "bubble bursting and its connection to maximum lift are analyzed ."),

    (49, "plane sound waves of finite amplitude",
     "riemann,b.", "abh. ges. wiss. gottingen, 1860.",
     "the propagation of finite amplitude sound waves in one dimension is analyzed "
     "using the method of characteristics . "
     "the riemann invariants for nonlinear wave propagation are introduced . "
     "wave steepening and shock formation are described . "
     "the results are fundamental to the theory of gas dynamics and aeroacoustics ."),

    (50, "effect of mach number and reynolds number on the drag of a flat plate",
     "goddard,f.e.", "j. ae. scs. 26, 1959.",
     "the combined effects of mach number and reynolds number on the drag coefficient "
     "of a flat plate in compressible flow are investigated experimentally . "
     "laminar, transitional, and turbulent boundary layer drag are measured . "
     "the strong and weak interaction regimes at hypersonic mach numbers are identified . "
     "the data are correlated using the van driest effective velocity transformation ."),
]

QUERIES = [
    (1, "what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft"),
    (2, "what are the aerodynamic characteristics of bodies of revolution and the effect of compressibility on these characteristics"),
    (3, "papers on the interaction of shock waves with boundary layers"),
    (4, "papers on transient heat conduction in composite slabs"),
    (5, "what is the effect of blowing and suction on the boundary layer"),
    (6, "what are the fluid mechanics of turbulent wakes and jets and mixing regions"),
    (7, "what problems arise in the structural design of aircraft for supersonic flight"),
    (8, "can shock waves be used to generate very high temperatures in a gas and if so how"),
    (9, "what is the current level of knowledge on hypersonic aerodynamics including viscous effects"),
    (10, "papers dealing with the theoretical and experimental aspects of viscous turbulent flows"),
    (11, "what are the aerodynamics of delta wings including vortex effects"),
    (12, "papers on airfoil theory and the calculation of pressure distributions"),
    (13, "what are the effects of roughness on drag and boundary layer transition"),
    (14, "papers on the stability of laminar flow and transition to turbulence"),
    (15, "papers on heat transfer in supersonic and hypersonic boundary layers"),
]

# Relevance judgments: (query_id, doc_id, grade)
# Grade: 1=most relevant, 2=relevant, 3=moderate, 4=marginal, 5=not relevant
# Grades 1-4 considered relevant for binary evaluation
JUDGMENTS = [
    # Query 1: aeroelastic models, heated high speed aircraft
    (1, 6, 1), (1, 25, 1), (1, 7, 2), (1, 14, 2), (1, 27, 2),
    (1, 15, 3), (1, 44, 3), (1, 1, 4), (1, 46, 4),
    # Query 2: bodies of revolution, compressibility
    (2, 9, 1), (2, 30, 1), (2, 40, 2), (2, 18, 2), (2, 22, 2),
    (2, 23, 3), (2, 41, 3), (2, 7, 4), (2, 46, 4),
    # Query 3: shock waves and boundary layers
    (3, 9, 1), (3, 8, 1), (3, 44, 2), (3, 50, 2), (3, 21, 2),
    (3, 37, 3), (3, 15, 3), (3, 47, 4),
    # Query 4: transient heat conduction composite slabs
    (4, 5, 1), (4, 10, 2), (4, 44, 3), (4, 6, 4),
    # Query 5: blowing suction boundary layer
    (5, 12, 1), (5, 33, 1), (5, 4, 2), (5, 29, 2),
    (5, 16, 3), (5, 34, 3), (5, 3, 4),
    # Query 6: turbulent wakes jets mixing
    (6, 35, 1), (6, 45, 1), (6, 26, 2), (6, 38, 2), (6, 29, 2),
    (6, 19, 3), (6, 42, 3), (6, 2, 4),
    # Query 7: structural design supersonic aircraft
    (7, 6, 1), (7, 25, 1), (7, 27, 2), (7, 46, 2),
    (7, 41, 3), (7, 14, 4), (7, 43, 4),
    # Query 8: shock waves high temperatures
    (8, 9, 1), (8, 44, 1), (8, 49, 2), (8, 31, 2),
    (8, 18, 3), (8, 50, 4),
    # Query 9: hypersonic aerodynamics viscous effects
    (9, 21, 1), (9, 37, 1), (9, 7, 2), (9, 50, 2), (9, 8, 2),
    (9, 15, 3), (9, 44, 3), (9, 20, 4),
    # Query 10: turbulent viscous flows
    (10, 45, 1), (10, 29, 1), (10, 19, 2), (10, 42, 2), (10, 47, 2),
    (10, 32, 3), (10, 16, 3), (10, 26, 4), (10, 2, 4),
    # Query 11: delta wings vortex
    (11, 28, 1), (11, 13, 1), (11, 39, 2), (11, 24, 2),
    (11, 46, 3), (11, 40, 3), (11, 1, 4),
    # Query 12: airfoil theory pressure distribution
    (12, 11, 1), (12, 17, 1), (12, 41, 2), (12, 43, 2), (12, 36, 2),
    (12, 22, 3), (12, 14, 3), (12, 46, 4),
    # Query 13: roughness drag boundary layer transition
    (13, 34, 1), (13, 42, 1), (13, 32, 2), (13, 16, 2),
    (13, 29, 3), (13, 50, 4), (13, 12, 4),
    # Query 14: laminar flow stability transition
    (14, 16, 1), (14, 32, 1), (14, 48, 2), (14, 4, 2), (14, 29, 2),
    (14, 12, 3), (14, 34, 3), (14, 3, 4),
    # Query 15: heat transfer supersonic hypersonic boundary layers
    (15, 15, 1), (15, 47, 1), (15, 44, 2), (15, 19, 2), (15, 8, 2),
    (15, 5, 3), (15, 37, 3), (15, 50, 4), (15, 6, 4),
]


def write_documents(path):
    with open(path, 'w') as f:
        for doc_id, title, author, bib, text in DOCS:
            f.write(f".I {doc_id}\n")
            f.write(".T\n")
            f.write(f"{title} .\n")
            f.write(".A\n")
            f.write(f"{author}\n")
            f.write(".B\n")
            f.write(f"{bib}\n")
            f.write(".W\n")
            f.write(f"{text}\n")


def write_queries(path):
    with open(path, 'w') as f:
        for qid, text in QUERIES:
            f.write(f".I {qid}\n")
            f.write(".W\n")
            f.write(f"{text} .\n")


def write_judgments(path):
    with open(path, 'w') as f:
        for qid, docid, grade in JUDGMENTS:
            f.write(f"{qid} 0 {docid} {grade}\n")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    write_documents(os.path.join(out_dir, "cran.all.1400"))
    write_queries(os.path.join(out_dir, "cran.qry"))
    write_judgments(os.path.join(out_dir, "cranqrel"))
    print(f"Generated:")
    print(f"  cran.all.1400  ({len(DOCS)} documents)")
    print(f"  cran.qry       ({len(QUERIES)} queries)")
    print(f"  cranqrel       ({len(JUDGMENTS)} judgments)")
