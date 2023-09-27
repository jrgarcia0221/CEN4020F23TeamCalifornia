import menuSystem
import main

# actions for useful links
def browseInCollege():
  print("Under construction")
  return True

def businessSolutions():
  print("Under construction")
  return True

def directories():
  print("Under construction")
  return True

# actions for general links
# prints help center info
def helpCenter():
  print("We're here to help.")
  return True

# prints about info for general section
def about():
  print("InCollege:\nWelcome to InCollege, the world's largest college student network with many users in many countries and territories worldwide.")
  return True

# prints press info
def press():
  print("InCollege Pressroom:\nStay on top of the latest news, updates, and reports.")
  return True

def blog():
  print("Under construction")
  return True

def careers():
  print("Under construction")
  return True

def developers():
  print("Under construction")
  return True

# Build general menu
# Sign up option available only if user is not logged in
#   (redirects to main menu where create account and login are)
def buildGeneralMenu(log):
    generalMenuItems = [
        menuSystem.menuNode("Help Center", goBack=True, action=helpCenter),
        menuSystem.menuNode("About", goBack=True, action=about),
        menuSystem.menuNode("Press", goBack=True, action=press),
        menuSystem.menuNode("Blog", goBack=True, action=blog),
        menuSystem.menuNode("Careers", goBack=True, action=careers),
        menuSystem.menuNode("Developers", goBack=True, action=developers)
    ]
    # log is True if user is logged in
    # add sing up option if log is False
    if not log:
        generalMenuItems.insert(0, menuSystem.menuNode("Sign Up", action=main.buildMenuTree))

    return menuSystem.menuNode("General", goBack=True, children=generalMenuItems)

# build useful links menu
def buildUsefulLinksMenu(log):
    # build general menu
    generalMenu = buildGeneralMenu(log)

    return menuSystem.menuNode(
        "Useful Links",
        goBack=True,
        children=[
            generalMenu,
            menuSystem.menuNode("Browse InCollege", goBack=True, action=browseInCollege),
            menuSystem.menuNode("Business Solutions", goBack=True, action=businessSolutions),
            menuSystem.menuNode("Directories", goBack=True, action=directories)
        ]
    )
