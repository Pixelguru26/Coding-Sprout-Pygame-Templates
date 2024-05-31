
class testClass:
  def __init__(this):
    this.val = True

  def testfn(this, arg):
    if this.val:
      print("Success")
    print(arg)

class testClass2:
  def __init__(this, testfn):
    this.testfn = testfn
    this.val = False
  
  def test(this):
    this.testfn(0)
instance = testClass()
instance = testClass2(instance.testfn)

instance.test()
