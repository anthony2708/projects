def main():
    operations_count = 0
    ask_again = True
    while (ask_again):
        a = input("Enter the numerator: ")
        b = input("Enter the denominator: ")
        result = perform_division(a, b)
        if (result is not None):
            operations_count += 1
            print(result)
            ask_again = input(
                "Do you want to perform another operation? Enter yes or no: ")
            if (ask_again == 'yes'):
                ask_again = True
            else:
                ask_again = False
                print("You performed " +
                      str(operations_count) + " operations, bye!")


def perform_division(a, b):
    try:
        return int(a)/int(b)
    except ZeroDivisionError as error:
        print("You can't divide by zero!")
    except Exception as error:
        print("Invalid input, please try again")


main()
