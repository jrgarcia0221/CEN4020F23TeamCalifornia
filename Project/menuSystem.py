#Author Grant DeBiase
#Tree structure
#label - the name of the choice - do not include number of choice
#action=None - function that gets called when menu choice is selected
#children=None - any sub menu this menu will have
#goBack=False - If you want it to have a go back option
class menuNode:

  def __init__(self,
               label,
               action=None,
               children=None,
               goBack=False,
               isGoBack=False):
    self.label = label
    self.action = action
    self.children = children or []
    self.isGoBack = isGoBack
    self.goBack = goBack
    if (goBack and not isGoBack):
      childNode = menuNode("Go Back: ", isGoBack=True)
      self.children.append(childNode)

#Author Grant DeBiase
def printMenu(node):
  print("----------------------------------------------------")
  print(node.label)
  for i, child in enumerate(node.children, start=1):
    print(f"{i}. {child.label}")

#Author Grant DeBiase
def navigateMenu(node, stack):
  printMenu(node)
  while True:
    choice = input("Enter your choice (1-{}): ".format(len(node.children)))
    if choice.isdigit():
      choice = int(choice)
      if 1 <= choice <= len(node.children):
        selectedNode = node.children[choice - 1]
        if selectedNode.isGoBack and stack:
          navigateMenu(stack.pop(), stack)
          return
        if selectedNode.action:
          if selectedNode.action() and selectedNode.children:
            stack.append(node)
            navigateMenu(selectedNode, stack)
          else:
            navigateMenu(node, stack)
        else:
          stack.append(node)
          navigateMenu(selectedNode, stack)
        return
    print("Invalid choice. Please try again.")
