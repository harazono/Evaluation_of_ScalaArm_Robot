-- Version: Lua 5.3.5
local Option={CP=1, SpeedL=100, AccL=100}
local Lid_place_lower_carsian = {coordinate = {76.80, 236.51, 150.00, 180}, tool = 0, user = 2}
local Lid_place_upper_carsian = {coordinate = {76.80, 236.51, 170.00, 180}}
local Lid_place_lower_joint = {joint = {20.40, 103.08, 148.22, 56.86}}
local Lid_place_upper_joint = {joint = {20.40, 103.08, 184.00, 56.86}}
-- set delta_x and delta_y
local delta_x = 0
local delta_y = 1.95
print(GetPose())
DO(1, OFF)
MovL(P1)
while true
do
  MovL(P2)
  Wait(10)
  DO(1, ON)
  Wait(100)
  RelMovL({0, 0, 50, 0})
  Wait(10)
  RelMovL({delta_x, delta_y, 0, 0})
  Wait(10)
  RelMovL({0, 0, -48, 0})
  Wait(10)
  DO(1, OFF)
  Wait(100)
  RelMovL({0, 0, 50, 0})
  MovJ(P6)
  Wait(10)
  MovJ(P4)
  Wait(10)
  MovJ(P5)
  MovJ(P4)
  MovJ(P6)
  MovJ(P1)
  Wait(10)
end
