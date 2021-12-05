# ibis

## ibis-server 

Contains the Bluetooth receiver and the the signal -> keystroke converter
`pip install -r requirements.txt`

### Microbit version and device addresses
. Version 1 - E4:37:80:63:49:2B:
. Version 2 - D6:D8:94:5E:21:03:

Update the device value in ibis.py to refer to the Microbit device address identified when executing discover.py


## Magnetic north correction

To work out the delta between when your head is neutral you store the neutral heading in compassOffset, and you calculate the new heading and determine the difference. We will allow a maximum 30 degrees off center (neutral) to the left and the right. So, negative values will indicate the amount to the left, and positive values will indicate the amount to the right.

This creates a problem however at magnetic north because of the 0->360->0 problem. Consider

* Neutral heading is 275 degrees (facing west)
** Turn left 20 degrees, heading will equal 255, delta will equal -20
** Turn right 20 degrees, heading will eqal 295, delta will equal +20

* Neutral heading is 350 degrees (facing almost north)
** Turn left 20 degrees, heading will equal 330, delta will equal -20
** Turn right 20 degrees, heading will equal 10, delta will equal 20

Problem - how do we calculate the delta?