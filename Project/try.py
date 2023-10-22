import dataTypes

def createExperience(experience= None):
      experience = experience or dataTypes.createExperience()
      for k,v in experience.items():
            ans= input(f"Enter {k} or 0 to exit: ")
            if ans == '0':
                  return experience
            experience[k]= ans
      return experience

def createOrEditExperience(experiences):
      i = 1
      for experience in experiences:
            print(f"Type {str(i)} to edit experience {experience['title']}")
            i=i+1

      while True:
            ans = input("Enter the number of the experience you want to edit or 0 to exit: ")
            if ans =='0':
                  break
            if int(ans) > len(experiences):
                  print("Invalid input. please try again")
                  continue              
            createExperience(experiences[int(ans)-1])
            
      while len(experiences)<3:
            ans= input("\nEnter 1 to create experience or 0 to exit: ")
            if ans == '1':
                  experiences.append(createExperience())
            else:
                  break

createOrEditExperience([dataTypes.createExperience()])         