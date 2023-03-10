import java.util.Scanner;
import java.util.regex.*;

public class password_checker {
    //strength bar to visualize <3
    public static int total = 5;
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        while(true){
            System.out.println("\nplease enter a password to check");
            String password = sc.next();
            if(password.length() == 0){
                System.out.println("please enter a password");
                continue;
            }
            boolean isStrong = isStrongPassword(password);
            if (isStrong) {
                System.out.println("The password is good for usage! \n");
                break;
            } else {
                System.out.println("\nThe password is too insecure. Here are some suggested changes: ");
                checkPasswordCriteria(password);
                total = 5;
                continue;
            }
        }
    }

    public static boolean isStrongPassword(String password) {
        // Define the regex pattern for a strong password
        String pattern = "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=!])(?=\\S+$).{8,}$";
        // Compile the regex pattern
        Pattern regex = Pattern.compile(pattern);
        
        // Match the password against the regex pattern
        Matcher matcher = regex.matcher(password);
        // Return true if the password matches the pattern, false otherwise
        return matcher.matches();
    }

    public static void checkPasswordCriteria(String password) {
        // Check if the password contains a lowercase letter
        if (!password.matches(".*[a-z].*")) {
            if(password.matches(".*[A-Z].*[A-Z].*")){
                System.out.println("Add a lowercase letter. Might I suggest turning one of your lowercase letters into an uppercase letter?");
            }
            else{
                System.out.println("Add a lowercase letter");
            }
            total--;
        }
        // Check if the password contains an uppercase letter
        if (!password.matches(".*[A-Z].*")) {
            if(password.matches(".*[a-z].*[a-z].*")){
                System.out.println("Add an uppercase letter. Might I suggest turning one of your uppercase letters into an lowercase letter?");
            }
            else{
                System.out.println("Add an upper case letter ");
            }
            total--;
        }
        // Check if the password contains a number
        if (!password.matches(".*[0-9].*")) {
            System.out.println("Add a digit ");
            total--;
        }
        // Check if the password contains a special character
        if (!password.matches(".*[@#$%^&+=!].*")) {
            System.out.println("Add a special character ");
            total--;
        }
        // Check if the password is at least 8 characters long
        if (password.length() < 8) {
            System.out.println("Make your password more than " + password.length()+ " characters long ");
            total--;
        }

        System.out.println("\nStrength bar of password");
        switch(total){
            case 0:
                System.out.println("|- - - - -|");
                break;
            case 1:
                System.out.println("|█ - - - -|");
                break;
            case 2:
                System.out.println("|█ █ - - -|");
                break;
            case 3:
                System.out.println("|█ █ █ - -|");
                break;
            case 4:
                System.out.println("|█ █ █ █ -|");
                break;
        }
    }
}