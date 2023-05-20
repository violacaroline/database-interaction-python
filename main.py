import menu
import register
import login
import subjectAdministrator
import authorAdministrator
import checkout

def main():

    runningMainMenu = True

    while runningMainMenu:        
        option = menu.printMainMenu()
        
        # MAIN MENU 
        if option == menu.MainMenuOption.LOGIN:
            runningMemberMenu = True
            if not login.loginMember():
                runningMemberMenu = False

            # MEMBER MENU
            while runningMemberMenu:
                memberOption = menu.printMemberMenu()

                if memberOption == menu.MemberMenuOption.BROWSESUBJECT:
                    subjectAdministrator.browseSubjects()
                elif memberOption == menu.MemberMenuOption.BROWSEAUHTORANDTITLE:
                    authorAdministrator.browseAuthorsAndTitles()
                elif memberOption == menu.MemberMenuOption.CHECKOUT:
                    userid = menu.printUserIdPrompt()
                    cartInfo = checkout.getCart(userid)
                    itemsInCart  = menu.printCartInfo(cartInfo)
                    if itemsInCart:
                        if menu.printCheckOutPrompt():
                            orderNumber = checkout.placeOrder(userid, cartInfo)
                            menu.printOrderInfo(orderNumber)
                elif memberOption == menu.MemberMenuOption.LOGOUT:
                    print("Logging out...")
                    runningMemberMenu = False
        # MAIN MENU
        elif option == menu.MainMenuOption.REGISTER:
            register.registerMember()
        # MAIN MENU
        elif option == menu.MainMenuOption.QUIT:
            runningMainMenu = False
            print("Goodbye!")
            exit()
        

if __name__ == "__main__":
    main()