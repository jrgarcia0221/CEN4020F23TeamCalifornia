import menuSystem
import main
import databaseInterface
import csvDatabase

guestSetting = []

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

# actions for important links
def copyrightNotice():
  print("\n\u00A9 2023 InCollege")
  return True

def about():
  aboutP = "\nThe creators of InCollege were motivated to launch this important product for college students across America,"
  aboutP += " to give them the oportunity to connect with fellow college students and look for potential adventures outside"
  aboutP += " to gain real world experience. Our dedicated team is determined to improve this product to reach the future generation"
  aboutP += " of students to further improve our society."
  print(aboutP)
  return True

def accessibility():
  accessP = "\nAt InCollege, we are commited to creating an environment within our platform that "
  accessP += "will give an accessible environment for all of our customers. We strive to give equal access"
  accessP += " to individuals with disabilities and languages other than English. We hope that"
  accessP += " our dedication will give all customers equal satisfaction and access while using our platform."
  print(accessP)
  return True

def userAgreement():
  agreementP = "\nUser Agreement\n"
  agreementP += "This user agreement is an agreement between the consumer and InCollege.\n"
  agreementP +="Following the creation of an account, InCollege earns the right to make use\n"
  agreementP +="of any information you provide and agree to comply to the terms and conditions\n"
  agreementP +="in this user agreement. You agree to comply with the following additional policies\n"
  agreementP +="provided in the options below user agreement such as our Privacy Policy, \n"
  agreementP +="Cookie Policy, Copyright Policy, and our Brand Policy.\n"
  print (agreementP)
  return True

def privacyPolicy():
  privacyP = "\nPrivacy Policy:\n"
  privacyP += "\nEffective as of September 27th, 2023\n"
  privacyP += "Introduction:\n"
  privacyP += "-------------------------------------------------"
  privacyP += "\n\nInCollege is dedicated to our users of the platdorm and are commited to be extremely transparent\n"
  privacyP += "about the use of the data we collect, the use of the data we collect, and the choices we provide for you, the user. "
  privacyP += "\n\nHow Your Data is Collected and Used:\n"
  privacyP += "-------------------------------------------------"
  privacyP += "\nOnce you register, the information you provided will be stored in our databases including your\n"
  privacyP += "name, email, username, password, and any information you provide once inside our services.\n"
  privacyP += "Once your data is collected, we utilize the in a way personalize our services for you, and providing any\n"
  privacyP += "relevant information desired that will be useful for our clients using our platform.\n"
  privacyP += "We will not disclose any private information you provided to any third party organizations and will not use the\n"
  privacyP += "data we collect to share for any monetary gains."
  print(privacyP)
  return True

def cookiePolicy():
  cookieP = "\nCookie Policy\n"
  cookieP += "InCollege all understand that your privacy is the most important aspect while you are utilizing our platform.\n"
  cookieP += "As we explained in our previous policies, we are committed to keeping the data you share with us transparent with\n"
  cookieP += "how we use your data. Assuming you understand abour cookies, we use them to improve the service we provide for you\n"
  cookieP += "on our platform. The cookies will help our platfrom to collect information and make it more convenient and useful for you.\n"
  print(cookieP)
  return True

def copyrightPolicy():
  copyrightP = "\nCopyright Policy:\n"
  copyrightP += "\nAll Rights Reserved.\n\n"
  copyrightP += "All materials appearing on InCollege is protected by copyright under U.S. Copyright laws and is the property of InCollege\n"
  copyrightP += "or the party members credited as the creators of InCollege. You may not copy, reproduce, distribute, publish, display, perform,\n"
  copyrightP += "modify, create derivative works, transmit, or in any way exploit any such content, or distrubuting our product over any nerwork, sell\n"
  copyrightP += "or offer it for sale, or use our product to construct ant type of database. You may not alter or remove any copyright or notices\n"
  copyrightP += "of the content from InCollege."
  print(copyrightP)
  return True

def brandPolicy():
  brandP = "Welcome to our Brand Policy\n"
  brandP += "---------------------------------"
  brandP += "The team here at InCollege are dedicated to growing this platform into a large community of college students trying to grow.\n"
  brandP += "We want to grow students to understand how life after college will look and to prepare them to take advantage of opportunities\n"
  brandP += "such as looking for internships, connecting with fellow college students, and even growing their portfolios and expressing them\n"
  brandP += "to college students in a social media way. Because our brand is reflected upon college students, we want to provide them with\n"
  brandP += "communities in terms of their college, majors, or anyone they prefer to connect with. We strive to have our platform to allow students\n"
  brandP += "communicate with eachother and provide feedback and responses to people who share interests and opportunities. We are continuosly\n"
  brandP += "improving our platform to better connect our communities and allow everyone to share their accomplishments and achievments to all.\n"
  return True

def initializeGuestArray(guestArr):   
    global guestSetting 
    guestSetting = guestArr

def guestControls():
  # global guestSettingArr
  # guestSettingArr = databaseInterface.lookForGuestSetting()
  print("Here are your current control settings")
  print("------------------------------------------------")
  print("E-Mail:", guestSetting[1])
  print("SMS:", guestSetting[2])
  print("Targeted Advertising:", guestSetting[3])
  print("\nPlease select option below to change setting (ON/OFF)")

  return True

def toggleEmail():
  # to do it without restarting, need to read back each time func called
  if guestSetting[1] == "On":
    toggle = "Off"
  else:
    toggle = "On"
  csvDatabase.changeRecord("guestSettings.csv", 1, guestSetting[0], toggle)
  print("Your changes will be reflected next time system boots up.")
  return True

def toggleSMS():
  if guestSetting[2] == "On":
     toggle = "Off"
  else:
     toggle = "On"
  csvDatabase.changeRecord("guestSettings.csv", 2, guestSetting[0], toggle)
  print("Your changes will be reflected next time system boots up.")
  return True

def toggleTargetedAudience():
  if guestSetting[3] == "On":
     toggle = "Off"
  else:
     toggle = "On"
  csvDatabase.changeRecord("guestSettings.csv", 3, guestSetting[0], toggle)
  print("Your changes will be reflected next time system boots up.")
  return True

def languages():
  print("Here are your current language settings")
  print("------------------------------------------------")
  print("Language:", guestSetting[4])
  print("\nPlease select option below to change setting (English/Spanish)")
  return True

def toggleLanguages():
  if guestSetting[4] == "English":
    toggle = "Spanish"
  else:
    toggle = "English"
  csvDatabase.changeRecord("guestSettings.csv", 4, guestSetting[0], toggle)
  return True


def buildPrivacyMenu(log):
    privacyPolicyMenu = []
    # log is True if user is logged in
    # add sing up option if log is False
    if log:
        privacyPolicyMenu.insert(0, menuSystem.menuNode("Guest Controls", goBack=True, action=guestControls, children=[
            menuSystem.menuNode(
              "Toggle Email",
              goBack=True,
              action=toggleEmail ),
            menuSystem.menuNode(
              "Toggle SMS",
              goBack=True,
              action=toggleSMS ),
            menuSystem.menuNode(
              "Toggle Targeted Audience",
              goBack=True,
              action=toggleTargetedAudience )
        ]))

    return menuSystem.menuNode("Privacy Policy", goBack=True, action=privacyPolicy, children=privacyPolicyMenu)


def buildImportantLinksMenu(log):
    privacyMenu = buildPrivacyMenu(log)

    importantLinkMenu = [
            menuSystem.menuNode("Copyright Notice",
                                goBack=True,
                                action=copyrightNotice),
            menuSystem.menuNode("About",
                                goBack=True,
                                action=about),
            menuSystem.menuNode("Accessibility",
                                goBack=True,
                                action=accessibility),
            menuSystem.menuNode("User Agreement",
                                goBack=True,
                                action=userAgreement),
            privacyMenu,
            menuSystem.menuNode("Cookie Policy",
                                goBack=True,
                                action=cookiePolicy),
            menuSystem.menuNode("Copyright Policy",
                                goBack=True,
                                action=copyrightPolicy),
            menuSystem.menuNode("Brand Policy",
                                goBack=True,
                                action=brandPolicy)
      ]
    if log:
        importantLinkMenu.insert(10, menuSystem.menuNode("Languages", goBack=True, action=languages, children=[
           menuSystem.menuNode(
              "Toggle Language",
              goBack=True,
              action=toggleLanguages)
        ]))
    return menuSystem.menuNode(
        "InCollege Important Links",
        goBack=True,
        children=importantLinkMenu
    )