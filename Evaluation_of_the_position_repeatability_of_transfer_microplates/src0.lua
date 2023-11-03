-- Version: Lua 5.3.5
j1 = 0
j2 = 0
j3 = 200
j4 = 0
local Option={CP=1, SpeedJ=100, AccJ=100}
--local P={joint = {j1, j2, j3, j4}}
local Plate_place_lowwer = {joint = {20.22, 102.97, 138.48, 56.54}}
local Plate_place_upper  = {joint = {20.22, 102.97, 172.22, 56.54}}
local Plate_place_measurement = {joint = {56.67, 20.12, 172.22, 102.794}}
local Plate_place_measurement_outer_limit = {joint = {62.77, 7.73, 173.13, -70.49}}
JointMovJ(Plate_place_upper, Option)

--MovL(P, Option)
while true
do
  DO(1, OFF)
  Wait(400)
  JointMovJ(Plate_place_lowwer, Option)
  Wait(50)
  DO(1, ON)
  Wait(400)
  JointMovJ(Plate_place_upper, Option)
 
  JointMovJ(Plate_place_measurement, Option)
  Wait(3000)
  JointMovJ(Plate_place_upper, Option)
  Wait(50)
  JointMovJ(Plate_place_lowwer, Option)
  Wait(50)
  DO(1, OFF)
 end
  
  
--[[  while true
do
    local Option={CP=1, SpeedJ=50, AccJ=20}
    local P1 ={joint ={0,50,30,0}}
    local P2 ={joint ={0,0,30,0}}
    local P3 ={joint ={0,0,10,0}}
    JointMovJ(P1, Option)
    JointMovJ(P2, Option)
    JointMovJ(P3, Option)
end
]]--