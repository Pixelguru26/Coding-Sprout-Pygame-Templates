
def abstract_equalize(atemp, amass, btemp, bmass):
  a_energy = atemp * amass
  b_energy = btemp * bmass
  total_energy = a_energy + b_energy
  # print(f"total energy: {total_energy}")
  total_mass = amass + bmass
  a_energy = amass / total_mass * total_energy
  b_energy = bmass / total_mass * total_energy
  atemp = a_energy / amass
  btemp = b_energy / bmass
  # a_energy = atemp * amass
  # b_energy = btemp * bmass
  # total_energy = a_energy + b_energy
  # print(f"output energy: {total_energy}")
  return (atemp, btemp)

class exchanger():
  def __init__(this):
    this.input_temps = [0, 0]
    this.input_mass = [0, 0]
    this.output_temps = [0, 0]
    this.output_mass = [0, 0]
  
  def total_temp(this):
    ret = 0
    for v in this.input_temps:
      ret += v
    return ret
  
  def total_mass(this):
    ret = 0
    for v in this.input_mass:
      ret += v
    return ret
  
  def total_energy(this):
    ret = 0
    energy = 0
    temp = 0
    mass = 0
    for i in range(0, len(this.input_mass)):
      (temp, mass) = this.get_input_tempmass(i)
      if mass != 0:
        energy = temp * mass
        ret += energy
    return ret

  def get_input_tempmass(this, i):
    return (this.input_temps[i], this.input_mass[i])
  
  def get_output_tempmass(this, i):
    return (this.output_temps[i], this.output_mass[i])
  
  def set_input_tempmass(this, i, temp, mass):
    this.input_temps[i] = temp
    this.input_mass[i] = mass
  
  def set_output_tempmass(this, i, temp, mass):
    this.output_temps[i] = temp
    this.output_mass[i] = mass

  def operate(this):
    total_mass = this.total_mass()
    if total_mass == 0: return
    total_energy = this.total_energy()
    temp = 0
    mass = 0
    energy = 0
    for i in range(0, len(this.input_temps)):
      mass = this.input_mass[i]
      if mass != 0:
        energy = (mass/total_mass) * total_energy
        temp = energy/mass
        this.output_temps[i] = temp
        this.output_mass[i] = mass
        this.input_temps[i] = 0
        this.input_mass[i] = 0
      else:
        this.input_temps[i] = 0
        this.output_temps[i] = 0
        this.output_mass[i] = 0
  def readout(this):
    return f"temp1: {this.output_temps[0]} mass1: {this.output_mass[0]} || temp2: {this.output_temps[1]} mass2: {this.output_mass[1]}"

exchangers = []
n = 200
for i in range(0, n):
  exchangers.append(exchanger())

def transfer(dir1 = -1, dir2 = 1):
  prev = None
  next = None
  this = None
  temp = 0
  mass = 0
  targetA = None
  targetB = None
  for i in range(0, len(exchangers)):
    this = exchangers[i]
    if i > 0:
      prev = exchangers[i-1]
    else:
      prev = None
    if i < len(exchangers)-1:
      next = exchangers[i+1]
    else:
      next = None
    targetA = None
    if dir1 < 0:
      targetA = prev
    else:
      targetA = next
    targetB = None
    if dir2 < 0:
      targetB = prev
    else:
      targetB = next
    if targetA != None:
      (temp, mass) = this.get_output_tempmass(0)
      targetA.set_input_tempmass(0, temp, mass)
    if targetB != None:
      (temp, mass) = this.get_output_tempmass(1)
      targetB.set_input_tempmass(1, temp, mass)
def operate():
  for exchanger in exchangers:
    exchanger.operate()

iterations = 1000
exchanger_a = exchangers[0]
exchanger_b = exchangers[len(exchangers)-1]
print(f"Exchanger A: {exchanger_a.readout()} || Exchanger B: {exchanger_b.readout()}")
for i in range(0, iterations):
  exchanger_a.set_input_tempmass(1, 0, 100)
  exchanger_b.set_input_tempmass(0, 100, 50)
  transfer()
  operate()
print(f"Exchanger A: {exchanger_a.readout()} || Exchanger B: {exchanger_b.readout()}")

# item = exchanger()
# item.set_input_tempmass(0, 100, 1)
# item.set_input_tempmass(1, 0, 1)
# print(f"temp1: {item.input_temps[0]} mass1: {item.input_mass[0]} || temp2: {item.input_temps[1]} mass2: {item.input_mass[1]}")
# item.operate()
# item.readout()