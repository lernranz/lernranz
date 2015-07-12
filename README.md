
Description
===========

The LERNRaumANZeiger (-> Lernranz) aims to aid students at RWTH([RWTH Aachen University](https://www.rwth-aachen.de/))
in answering the question: “OMGWTF, all the study rooms are crowded, were are vacancies?” Based on wifi usage data,
it shows how crowded each room or building is.

The main site is at http://lernranz.de, while development testing takes place at http://dev.lernranz.de


Contribute
==========
You can have a look at the [open issues on Github](https://github.com/lernranz/lernranz/issues).

An easy way to improve Lernranz is to add more rooms (specified in rooms.json). Most fundamentally you have to find
out which access points (see web/aps) belong to the room you want to add. This does not require physically moving
yourself, you just need to know the buildings structure (the global access point list in web/aps is commented).
Group individual rooms if sensible, as the site becomes to cluttered otherwise.
